import sqlite3

conn = sqlite3.connect("market.db", check_same_thread=False)
cursor = conn.cursor()

# =========================
# USERS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")

# =========================
# USER ASSETS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_assets (
    user_id INTEGER,
    asset TEXT
)
""")

conn.commit()


# =========================
# ADD USER
# =========================

def add_user(user_id):

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,)
    )

    conn.commit()


# =========================
# ADD ASSET
# =========================

def add_asset(user_id, asset):

    cursor.execute(
        "INSERT INTO user_assets (user_id, asset) VALUES (?, ?)",
        (user_id, asset)
    )

    conn.commit()


# =========================
# GET USER ASSETS
# =========================

def get_assets(user_id):

    cursor.execute(
        "SELECT asset FROM user_assets WHERE user_id=?",
        (user_id,)
    )

    rows = cursor.fetchall()

    return [r[0] for r in rows]


# =========================
# REMOVE ASSET
# =========================

def remove_asset(user_id, asset):

    cursor.execute(
        "DELETE FROM user_assets WHERE user_id=? AND asset=?",
        (user_id, asset)
    )

    conn.commit()