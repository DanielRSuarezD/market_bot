import sqlite3

conn = sqlite3.connect("market.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS prices(
asset TEXT,
price REAL,
timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


def save_price(asset, price):

    cursor.execute(
        "INSERT INTO prices(asset,price) VALUES (?,?)",
        (asset,price)
    )

    conn.commit()


def get_last_price(asset):

    cursor.execute(
        "SELECT price FROM prices WHERE asset=? ORDER BY timestamp DESC LIMIT 1",
        (asset,)
    )

    row = cursor.fetchone()

    if row:
        return row[0]

    return None
import sqlite3

conn = sqlite3.connect("market.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY
)
""")

conn.commit()


def add_user(user_id):

    cursor.execute(
        "INSERT OR IGNORE INTO users(id) VALUES (?)",
        (user_id,)
    )

    conn.commit()


def get_users():

    cursor.execute("SELECT id FROM users")

    rows = cursor.fetchall()

    return [r[0] for r in rows]