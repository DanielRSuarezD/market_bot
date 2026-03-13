from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from config import TOKEN
from market_data import get_fx, get_oil, get_dxy, get_global
from database import save_price, get_last_price, add_user
from news import get_news
from calendar_data import get_calendar


def trend_arrow(change):

    if change > 0:
        return "▲"
    elif change < 0:
        return "▼"
    else:
        return "●"


def calculate_change(asset, price):

    last = get_last_price(asset)

    change = 0

    if last:
        change = round((price - last) / last * 100, 2)

    save_price(asset, price)

    return change


def inline_menu():

    keyboard = [
        [
            InlineKeyboardButton("📊 Market", callback_data="market"),
            InlineKeyboardButton("🔥 Movers", callback_data="movers")
        ],
        [
            InlineKeyboardButton("🌍 Flows", callback_data="flows"),
            InlineKeyboardButton("📰 News", callback_data="news")
        ],
        [
            InlineKeyboardButton("📅 Calendar", callback_data="calendar")
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


async def send(update, text):

    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=inline_menu()
        )

    elif update.callback_query:
        await update.callback_query.message.reply_text(
            text,
            reply_markup=inline_menu()
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    add_user(update.effective_user.id)

    keyboard = [
        ["📊 Market", "🔥 Movers"],
        ["🌍 Flows", "📰 News"],
        ["📅 Calendar"]
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "🌍 Global Market Monitor\n\nChoose an option 👇",
        reply_markup=reply_markup
    )


async def market(update: Update, context: ContextTypes.DEFAULT_TYPE):

    fx = get_fx()
    oil = get_oil()
    dxy = get_dxy()
    global_data = get_global()

    assets = {
        "Brent": oil["Brent"],
        "WTI": oil["WTI"],
        "EUR": fx["EUR"],
        "MXN": fx["MXN"],
        "COP": fx["COP"],
        "PEN": fx["PEN"],
        "CRC": fx["CRC"],
        "RUB": fx["RUB"],
        "AED": fx["AED"],
        "DXY": dxy,
        "Gold": global_data["Gold"],
        "Silver": global_data["Silver"],
        "BTC": global_data["BTC"],
        "SP500": global_data["SP500"]
    }

    changes = {}

    for asset, price in assets.items():
        changes[asset] = calculate_change(asset, price)

    message = f"""
🌍 MARKET MONITOR

🛢 ENERGY
Brent: {oil["Brent"]} {trend_arrow(changes["Brent"])} ({changes["Brent"]}%)
WTI: {oil["WTI"]} {trend_arrow(changes["WTI"])} ({changes["WTI"]}%)

Spread Brent-Urals: {oil["Spread"]}

💱 FX MARKETS

🇪🇺 EUR: {fx["EUR"]} {trend_arrow(changes["EUR"])} ({changes["EUR"]}%)
🇲🇽 MXN: {fx["MXN"]} {trend_arrow(changes["MXN"])} ({changes["MXN"]}%)
🇨🇴 COP: {fx["COP"]} {trend_arrow(changes["COP"])} ({changes["COP"]}%)
🇵🇪 PEN: {fx["PEN"]} {trend_arrow(changes["PEN"])} ({changes["PEN"]}%)
🇨🇷 CRC: {fx["CRC"]} {trend_arrow(changes["CRC"])} ({changes["CRC"]}%)
🇷🇺 RUB: {fx["RUB"]} {trend_arrow(changes["RUB"])} ({changes["RUB"]}%)
🇦🇪 AED: {fx["AED"]} {trend_arrow(changes["AED"])} ({changes["AED"]}%)

💵 DOLLAR INDEX
DXY: {dxy} {trend_arrow(changes["DXY"])} ({changes["DXY"]}%)

🌎 GLOBAL MARKETS
📈 S&P500: {global_data["SP500"]} {trend_arrow(changes["SP500"])} ({changes["SP500"]}%)
🥇 Gold: {global_data["Gold"]} {trend_arrow(changes["Gold"])} ({changes["Gold"]}%)
🥈 Silver: {global_data["Silver"]} {trend_arrow(changes["Silver"])} ({changes["Silver"]}%)
₿ Bitcoin: {global_data["BTC"]} {trend_arrow(changes["BTC"])} ({changes["BTC"]}%)
"""

    await send(update, message)


async def movers(update: Update, context: ContextTypes.DEFAULT_TYPE):

    fx = get_fx()
    global_data = get_global()

    assets = {
        "Gold": global_data["Gold"],
        "Silver": global_data["Silver"],
        "BTC": global_data["BTC"],
        "MXN": fx["MXN"],
        "COP": fx["COP"],
        "RUB": fx["RUB"]
    }

    movers = []

    for asset, price in assets.items():

        last = get_last_price(asset)

        if last:
            change = (price - last) / last * 100
        else:
            change = 0

        movers.append((asset, round(change,2)))

    movers.sort(key=lambda x: abs(x[1]), reverse=True)

    message = "🔥 TOP MARKET MOVERS\n\n"

    for m in movers[:5]:

        arrow = "▲" if m[1] > 0 else "▼"

        message += f"{m[0]} {arrow} {m[1]}%\n"

    await send(update, message)


async def flows(update: Update, context: ContextTypes.DEFAULT_TYPE):

    fx = get_fx()
    global_data = get_global()

    assets = {
        "Gold": global_data["Gold"],
        "Silver": global_data["Silver"],
        "Bitcoin": global_data["BTC"],
        "EUR": fx["EUR"],
        "MXN": fx["MXN"],
        "COP": fx["COP"],
        "RUB": fx["RUB"]
    }

    flows = []

    for asset, price in assets.items():

        last = get_last_price(asset)

        if last:
            change = (price - last) / last * 100
        else:
            change = 0

        flows.append((asset, round(change,2)))

    flows.sort(key=lambda x: abs(x[1]), reverse=True)

    message = "🌍 CAPITAL FLOWS\n\n"

    for f in flows[:6]:

        arrow = "▲" if f[1] > 0 else "▼"

        message += f"{f[0]} {arrow} {f[1]}%\n"

    await send(update, message)


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):

    news_list = get_news()

    message = "📰 MARKET NEWS\n\n"

    for title, link in news_list:
        message += f"{title}\n{link}\n\n"

    await send(update, message)


async def calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):

    events = get_calendar()

    message = "📅 MACRO CALENDAR\n\n"

    message += "🔴 High impact\n🟠 Medium\n🟢 Low\n\n"

    for impact, date, title in events:
        message += f"{impact} {date}\n{title}\n\n"

    await send(update, message)


async def keyboard_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📊 Market":
        await market(update, context)

    elif text == "🔥 Movers":
        await movers(update, context)

    elif text == "🌍 Flows":
        await flows(update, context)

    elif text == "📰 News":
        await news(update, context)

    elif text == "📅 Calendar":
        await calendar(update, context)


async def inline_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    if data == "market":
        await market(update, context)

    elif data == "movers":
        await movers(update, context)

    elif data == "flows":
        await flows(update, context)

    elif data == "news":
        await news(update, context)

    elif data == "calendar":
        await calendar(update, context)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("market", market))
app.add_handler(CommandHandler("movers", movers))
app.add_handler(CommandHandler("flows", flows))
app.add_handler(CommandHandler("news", news))
app.add_handler(CommandHandler("calendar", calendar))

app.add_handler(MessageHandler(filters.TEXT, keyboard_handler))
app.add_handler(CallbackQueryHandler(inline_callback))

print("BOT RUNNING...")

app.run_polling()