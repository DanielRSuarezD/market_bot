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


# =========================
# ASSETS
# =========================

FX_LATAM = ["MXN","BRL","COP","PEN","CLP","ARS","UYU","CRC"]

FX_GLOBAL = ["EUR","GBP","CHF","JPY","RUB","AED","AUD","CAD"]

ENERGY = ["BRENT","WTI","NATGAS"]

GLOBAL_INDICES = ["SP500","NASDAQ","DAX","FTSE","NIKKEI"]


# =========================
# KEYBOARD BUILDER
# =========================

def build_keyboard(items):

    keyboard = []

    for asset in items:
        keyboard.append(
            [InlineKeyboardButton(asset, callback_data=f"asset_{asset}")]
        )

    keyboard.append([InlineKeyboardButton("DONE", callback_data="done")])
    keyboard.append([InlineKeyboardButton("BACK", callback_data="back")])

    return InlineKeyboardMarkup(keyboard)


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    add_user(user_id)

    keyboard = [

        [InlineKeyboardButton("FX LATAM", callback_data="fx_latam")],
        [InlineKeyboardButton("FX GLOBAL", callback_data="fx_global")],
        [InlineKeyboardButton("ENERGY", callback_data="energy")],
        [InlineKeyboardButton("GLOBAL INDICES", callback_data="indices")],
        [InlineKeyboardButton("WATCHLIST", callback_data="portfolio")]

    ]

    await update.message.reply_text(

        "🌍 GLOBAL MARKET TERMINAL\n\nSelect category:",

        reply_markup=InlineKeyboardMarkup(keyboard)

    )


# =========================
# ROUTER
# =========================

async def router(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data


# FX LATAM
    if data == "fx_latam":

        await query.edit_message_text(

            "Select LATAM FX",

            reply_markup=build_keyboard(FX_LATAM)

        )


# FX GLOBAL
    elif data == "fx_global":

        await query.edit_message_text(

            "Select GLOBAL FX",

            reply_markup=build_keyboard(FX_GLOBAL)

        )


# ENERGY
    elif data == "energy":

        await query.edit_message_text(

            "Select ENERGY",

            reply_markup=build_keyboard(ENERGY)

        )


# INDICES
    elif data == "indices":

        await query.edit_message_text(

            "Select GLOBAL INDICES",

            reply_markup=build_keyboard(GLOBAL_INDICES)

        )


# ADD ASSET
    elif data.startswith("asset_"):

        asset = data.replace("asset_", "")

        add_asset(query.from_user.id, asset)

        await query.answer(f"{asset} added")


# WATCHLIST
    elif data == "portfolio":

        assets = get_assets(query.from_user.id)

        if not assets:

            text = "No assets selected"

        else:

            text = "📊 YOUR WATCHLIST\n\n"

            for a in assets:

                text += f"{a}\n"

        await query.edit_message_text(text)


# DONE
    elif data == "done":

        await query.edit_message_text(

            "Selection saved.\nUse /start to add more."

        )


# BACK
    elif data == "back":

        keyboard = [

            [InlineKeyboardButton("FX LATAM", callback_data="fx_latam")],
            [InlineKeyboardButton("FX GLOBAL", callback_data="fx_global")],
            [InlineKeyboardButton("ENERGY", callback_data="energy")],
            [InlineKeyboardButton("GLOBAL INDICES", callback_data="indices")],
            [InlineKeyboardButton("WATCHLIST", callback_data="portfolio")]

        ]

        await query.edit_message_text(

            "Select category:",

            reply_markup=InlineKeyboardMarkup(keyboard)

        )


# =========================
# ERROR HANDLER
# =========================

async def error_handler(update, context):

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
app.add_handler(CallbackQueryHandler(router))

app.add_error_handler(error_handler)

print("BOT RUNNING...")

app.run_polling(drop_pending_updates=True)
