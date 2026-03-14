async def flows(update, context):

    text = (
    "💰 GLOBAL FLOWS\n\n"
    "USD strength\n"
    "Oil bid\n"
    "Equities risk-on\n"
    )

    await update.message.reply_text(text)
