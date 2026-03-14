import threading

from telegram import Update,InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
CallbackQueryHandler,
ContextTypes
)

from config import TOKEN
from database import init_db,add_user,add_asset,get_assets
from market_data import get_market
from alerts import start_alert_engine


FX_LATAM=[
"MXN","BRL","COP","PEN","CLP","ARS","UYU","CRC","GTQ","BOB","PYG"
]

FX_GLOBAL=[
"EUR","GBP","CHF","JPY","RUB","AED"
]

ENERGY=["BRENT","WTI"]

METALS=["GOLD","SILVER"]

INDICES=["SP500","NASDAQ"]


def keyboard(items):

    kb=[]

    for i in items:

        kb.append([InlineKeyboardButton(i,callback_data=f"asset_{i}")])

    kb.append([InlineKeyboardButton("DONE",callback_data="done")])
    kb.append([InlineKeyboardButton("BACK",callback_data="back")])

    return InlineKeyboardMarkup(kb)


async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user=update.effective_user.id

    add_user(user)

    kb=[

    [InlineKeyboardButton("FX LATAM",callback_data="latam")],
    [InlineKeyboardButton("FX GLOBAL",callback_data="global")],
    [InlineKeyboardButton("ENERGY",callback_data="energy")],
    [InlineKeyboardButton("METALS",callback_data="metals")],
    [InlineKeyboardButton("INDICES",callback_data="indices")],
    [InlineKeyboardButton("WATCHLIST",callback_data="watch")]

    ]

    await update.message.reply_text(

    "🌍 Global Market Monitor\n\nChoose category",

    reply_markup=InlineKeyboardMarkup(kb)

    )


async def market(update:Update,context:ContextTypes.DEFAULT_TYPE):

    text=get_market()

    await update.message.reply_text(text)


async def router(update:Update,context:ContextTypes.DEFAULT_TYPE):

    query=update.callback_query
    await query.answer()

    data=query.data

    if data=="latam":

        await query.edit_message_text(

        "Select LATAM FX",

        reply_markup=keyboard(FX_LATAM)

        )

    elif data=="global":

        await query.edit_message_text(

        "Select GLOBAL FX",

        reply_markup=keyboard(FX_GLOBAL)

        )

    elif data=="energy":

        await query.edit_message_text(

        "Select ENERGY",

        reply_markup=keyboard(ENERGY)

        )

    elif data=="metals":

        await query.edit_message_text(

        "Select METALS",

        reply_markup=keyboard(METALS)

        )

    elif data=="indices":

        await query.edit_message_text(

        "Select INDICES",

        reply_markup=keyboard(INDICES)

        )

    elif data.startswith("asset_"):

        asset=data.replace("asset_","")

        add_asset(query.from_user.id,asset)

        await query.answer(f"{asset} added")

    elif data=="watch":

        assets=get_assets(query.from_user.id)

        text="📊 YOUR WATCHLIST\n\n"

        for a in assets:
            text+=f"{a}\n"

        await query.edit_message_text(text)

    elif data=="done":

        await query.edit_message_text(

        "Selection saved.\nUse /market"

        )


init_db()

app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CommandHandler("market",market))
app.add_handler(CallbackQueryHandler(router))

threading.Thread(target=start_alert_engine,args=(app.bot,),daemon=True).start()

print("BOT RUNNING")

app.run_polling(drop_pending_updates=True)
