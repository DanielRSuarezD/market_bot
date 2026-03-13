import sqlite3

DB_NAME = "market.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # crear tabla usuarios
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
    """)

    # crear tabla activos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        asset TEXT
    )
    """)

    conn.commit()

    # verificar columnas de users
    cursor.execute("PRAGMA table_info(users)")
    cols = [c[1] for c in cursor.fetchall()]

    if "user_id" not in cols:
        cursor.execute("DROP TABLE users")
        cursor.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY
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