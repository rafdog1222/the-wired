import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432)
}


def get_connections():
    conn = psycopg2.connect(**DB_CONFIG)
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
            id SERIAL PRIMARY KEY,
            origin_address TEXT NOT NULL,
            author_email TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS library (
            id SERIAL PRIMARY KEY,
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

    conn.commit()
    cursor.close()
    conn.close()

setup_database()
