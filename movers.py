async def movers(update, context):

    text = (
    "🚀 TOP MOVERS\n\n"
    "WTI +2.1%\n"
    "NASDAQ +1.3%\n"
    "MXN -0.7%\n"
    )

    await update.message.reply_text(text)
