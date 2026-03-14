[InlineKeyboardButton("FX GLOBAL", callback_data="fx_global")],
            [InlineKeyboardButton("ENERGY", callback_data="energy")],
            [InlineKeyboardButton("GLOBAL INDICES", callback_data="indices")],
            [InlineKeyboardButton("WATCHLIST", callback_data="portfolio")]

        ]

        await query.edit_message_text(

            "Choose category:",

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


# ALERT ENGINE
threading.Thread(target=start_alert_engine, daemon=True).start()


print("BOT RUNNING...")


app.run_polling(drop_pending_updates=True)
