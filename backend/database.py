import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database", "agribrain.db")

os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        image_name TEXT NOT NULL,
        result TEXT NOT NULL,
        confidence TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

    conn.commit()
    conn.close()


def create_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
    """, (name, email, password))

    conn.commit()
    conn.close()

def get_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM users
        WHERE email = ? AND password = ?
    """, (email, password))

    user = cursor.fetchone()

    conn.close()

    return user

def save_analysis(user_email, image_name, result, confidence):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO analyses (user_email, image_name, result, confidence)
        VALUES (?, ?, ?, ?)
    """, (user_email, image_name, result, confidence))

    conn.commit()
    conn.close()


def get_user_analyses(user_email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM analyses
        WHERE user_email = ?
        ORDER BY created_at DESC
    """, (user_email,))

    analyses = cursor.fetchall()

    conn.close()

    return analyses