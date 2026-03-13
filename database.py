import sqlite3
import os

DB_NAME = "market.db"

# eliminar base vieja (evita conflictos de schema)
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY
    )
    """)

    cursor.execute("""
    CREATE TABLE assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        asset TEXT
    )
    """)

    conn.commit()
    conn.close()


def add_user(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,)
    )

    conn.commit()
    conn.close()


def add_asset(user_id, asset):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO assets (user_id, asset) VALUES (?, ?)",
        (user_id, asset)
    )

    conn.commit()
    conn.close()


def get_assets(user_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT asset FROM assets WHERE user_id = ?",
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    return [r[0] for r in rows]