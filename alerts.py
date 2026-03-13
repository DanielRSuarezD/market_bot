import time
from market_data import get_assets_data
from database import get_assets
from telegram import Bot
from config import TOKEN


bot = Bot(token=TOKEN)


def check_alerts():

    from database import cursor

    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    for u in users:

        user_id = u[0]

        assets = get_assets(user_id)

        if not assets:
            continue

        data = get_assets_data(assets)

        for asset in data:

            change = data[asset]["change"]
            price = data[asset]["price"]

            if abs(change) > 1:

                message = f"""
🚨 MARKET ALERT

{asset}

Price: {price}
Change: {change}%
"""

                try:

                    bot.send_message(
                        chat_id=user_id,
                        text=message
                    )

                except:
                    pass


def start_alert_engine():

    while True:

        check_alerts()

        time.sleep(300)