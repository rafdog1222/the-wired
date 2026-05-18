import sqlite3

DB_FILE = "wired.db"

def get_connections():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_connections()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            email TEXT PRIMARY KEY,
            password_hash TEXT,
            address TEXT NOT NULL,
            joined_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin_address TEXT NOT NULL,
            author_email TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS library (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin_address TEXT NOT NULL,
            author_email TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS travel (
            email TEXT PRIMARY KEY,
            current_level INTEGER NOT NULL DEFAULT 3,
            travel_started TEXT,
            destination_level INTEGER
        )
    """)

    try:
        cursor.execute("ALTER TABLE members ADD COLUMN password_hash TEXT")
    except:
        pass

    conn.commit()
    conn.close()

setup_database()
