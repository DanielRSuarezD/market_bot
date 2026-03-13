from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import threading

from config import TOKEN
from database import add_user, add_asset, get_assets
from market_data import get_assets_data, get_top_movers
from alerts import start_alert_engine


FX_LATAM = [
"MXN","BRL","COP","PEN","CLP","ARS","UYU","CRC","GTQ","BOB","PYG","DOP","HNL","NIO","VES"
]

FX_GLOBAL = [
"EUR","GBP","CHF","JPY","CNY","RUB","AED","TRY","ZAR","AUD","CAD","NZD","INR","KRW","SGD","HKD"
]

ENERGY = [
"BRENT","WTI","NATGAS","GASOLINE","HEATING_OIL","TTF_GAS","COAL","URANIUM"
]

GLOBAL = [
"SP500","NASDAQ","DOW","DAX","CAC40","FTSE","EUROSTOXX","NIKKEI","HANGSENG","SHANGHAI"
]

COMMODITIES = [
"GOLD","SILVER","COPPER","PLATINUM","PALLADIUM","WHEAT","CORN","SOYBEAN","COCOA","COFFEE","SUGAR"
]

CRYPTO = [
"BITCOIN","ETHEREUM","SOLANA","BNB","XRP"
]

MACRO = [
"DXY","VIX","US10Y","US2Y","GER10Y","JGB10Y"
]


def build_keyboard(items):

    keyboard = []

    for i in items:

        keyboard.append(
            [InlineKeyboardButton(i, callback_data=f"add_{i}")]
        )

    keyboard.append(
        [InlineKeyboardButton("⬅ BACK", callback_data="back")]
    )

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    add_user(user_id)

    keyboard = [

        [InlineKeyboardButton("💱 FX LATAM", callback_data="fx_latam")],
        [InlineKeyboardButton("🌍 FX GLOBAL", callback_data="fx_global")],
        [InlineKeyboardButton("🛢 ENERGY", callback_data="energy")],
        [InlineKeyboardButton("📊 GLOBAL MARKETS", callback_data="global")],
        [InlineKeyboardButton("🪙 COMMODITIES", callback_data="commodities")],
        [InlineKeyboardButton("💰 CRYPTO", callback_data="crypto")],
        [InlineKeyboardButton("📈 MACRO", callback_data="macro")],
        [InlineKeyboardButton("📊 WATCHLIST", callback_data="portfolio")]

    ]

    await update.message.reply_text(
        "🌍 GLOBAL MARKET TERMINAL\n\nSelect category:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "fx_latam":

        await query.edit_message_text(
            "💱 FX LATAM",
            reply_markup=build_keyboard(FX_LATAM)
        )

    elif data == "fx_global":

        await query.edit_message_text(
            "🌍 FX GLOBAL",
            reply_markup=build_keyboard(FX_GLOBAL)
        )

    elif data == "energy":

        await query.edit_message_text(
            "🛢 ENERGY",
            reply_markup=build_keyboard(ENERGY)
        )

    elif data == "global":

        await query.edit_message_text(
            "📊 GLOBAL MARKETS",
            reply_markup=build_keyboard(GLOBAL)
        )

    elif data == "commodities":

        await query.edit_message_text(
            "🪙 COMMODITIES",
            reply_markup=build_keyboard(COMMODITIES)
        )

    elif data == "crypto":

        await query.edit_message_text(
            "💰 CRYPTO",
            reply_markup=build_keyboard(CRYPTO)
        )

    elif data == "macro":

        await query.edit_message_text(
            "📈 MACRO INDICATORS",
            reply_markup=build_keyboard(MACRO)
        )

    elif data.startswith("add_"):

        asset = data.replace("add_","")
        add_asset(query.from_user.id, asset)

        await query.answer(f"{asset} added")

    elif data == "portfolio":

        assets = get_assets(query.from_user.id)

        if not assets:

            text = "No assets selected"

        else:

            data = get_assets_data(assets)

            text = "📊 YOUR WATCHLIST\n\n"

            for a in data:

                price = data[a]["price"]
                change = data[a]["change"]

                arrow = "⬆️" if change > 0 else "⬇️"

                text += f"{a} {price} {arrow} ({change}%)\n"

        keyboard = [[InlineKeyboardButton("⬅ BACK", callback_data="back")]]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "back":

        await start(query, context)


async def movers(update: Update, context: ContextTypes.DEFAULT_TYPE):

    movers = get_top_movers()

    text = "🔥 TOP MARKET MOVERS\n\n"

    for m in movers:

        text += f"{m[0]} {m[1]}%\n"

    await update.message.reply_text(text)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("movers", movers))
app.add_handler(CallbackQueryHandler(router))

threading.Thread(target=start_alert_engine).start()

print("BOT RUNNING...")

app.run_polling()