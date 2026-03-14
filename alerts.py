import time
from database import get_assets
from market_data import get_price,TICKERS


LAST_PRICE={}


def check_alerts(bot):

    from database import sqlite3

    conn=sqlite3.connect("market.db")
    cursor=conn.cursor()

    cursor.execute("SELECT user_id FROM users")

    users=cursor.fetchall()

    for u in users:

        user=u[0]

        assets=get_assets(user)

        for a in assets:

            if a not in TICKERS:
                continue

            price,_=get_price(TICKERS[a])

            key=f"{user}_{a}"

            last=LAST_PRICE.get(key)

            if last is None:

                LAST_PRICE[key]=price
                continue

            move=abs((price-last)/last)*100

            if move>1:

                bot.send_message(

                user,

                f"🚨 {a} ALERT\nMove: {round(move,2)}%\nPrice: {price}"

                )

                LAST_PRICE[key]=price


def start_alert_engine(bot):

    while True:

        try:

            check_alerts(bot)

        except Exception as e:

            print("ALERT ERROR:",e)

        time.sleep(300)
