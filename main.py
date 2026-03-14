import threading

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from config import TOKEN
from database import init_db, add_user, add_asset, get_assets
from market_data import get_assets_data, get_top_movers
from alerts import start_alert_engine


# =========================
# LISTAS DE ACTIVOS
# =========================

FX_LATAM = [
    "MXN","BRL","COP","PEN","CLP","ARS","UYU","CRC","GTQ","BOB","PYG","DOP","HNL","NIO","VES"
]

FX_GLOBAL = [
    "EUR","GBP","CHF","JPY","CNY","RUB","AED","TRY","ZAR","AUD","CAD","NZD","INR","KRW","SGD","HKD"
]

ENERGY = [
    "BRENT","WTI","NATGAS","GASOLINE","HEATING_OIL","TTF_GAS","COAL","URANIUM"
]

GLOBAL_INDICES = [
    "SP500","NASDAQ","DOW","DAX","CAC40","FTSE","EUROSTOXX","NIKKEI","HANGSENG","SHANGHAI"
]


# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    add_user(user_id)

    keyboard = [
        [InlineKeyboardButton("FX LATAM", callback_data="fx_latam")],
        [InlineKeyboardButton("FX GLOBAL", callback_data="fx_global")],
        [InlineKeyboardButton("ENERGY", callback_data="energy")],
        [InlineKeyboardButton("GLOBAL INDICES", callback_data="indices")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Choose asset category:",
        reply_markup=reply_markup
    )


# =========================
# MOVERS COMMAND
# =========================

async def movers(update: Update, context: ContextTypes.DEFAULT_TYPE):

    movers = get_top_movers()

    text = "Top Movers:\n\n"

    for m in movers:
        text += f"{m['asset']} {m['change']}%\n"

    await update.message.reply_text(text)


# =========================
# BUTTON ROUTER
# =========================

async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "fx_latam":
        assets = FX_LATAM

    elif data == "fx_global":
        assets = FX_GLOBAL

    elif data == "energy":
        assets = ENERGY

    elif data == "indices":
        assets = GLOBAL_INDICES

    else:
        return

    keyboard = []

    for asset in assets:
        keyboard.append(
            [InlineKeyboardButton(asset, callback_data=f"asset_{asset}")]
        )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "Select asset to follow:",
        reply_markup=reply_markup
    )


# =========================
# ERROR HANDLER
# =========================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("ERROR:", context.error)


# =========================
# INIT DATABASE
# =========================

init_db()


# =========================
# START BOT
# =========================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("movers", movers))
app.add_handler(CallbackQueryHandler(router))

app.add_error_handler(error_handler)

# iniciar alert engine
threading.Thread(target=start_alert_engine, daemon=True).start()

print("BOT RUNNING...")

app.run_polling()
