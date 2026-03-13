import sqlite3
import time
from market_data import get_assets_data

DB_NAME = "market.db"


def check_alerts():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # verificar si tabla existe
    cursor.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table' AND name='assets'
    """)

    if not cursor.fetchone():
        conn.close()
        return

    cursor.execute("SELECT DISTINCT asset FROM assets")
    rows = cursor.fetchall()

    assets = [r[0] for r in rows]

    conn.close()

    if not assets:
        return

    data = get_assets_data(assets)

    for asset in data:

        price = data[asset]["price"]
        change = data[asset]["change"]

        if abs(change) > 1:

            print(
                f"🚨 ALERT {asset} price={price} change={change}%"
            )


def start_alert_engine():

    while True:

        try:

            check_alerts()

        except Exception as e:

            print("ALERT ENGINE ERROR:", e)

        time.sleep(60)