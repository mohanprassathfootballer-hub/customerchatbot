import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE = DATA_DIR / "chatbot.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            created_at TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (conversation_id)
                REFERENCES conversations(id)
        )
    """)

    connection.commit()
    connection.close()


def create_conversation(customer_name="Guest"):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO conversations (customer_name, created_at)
        VALUES (?, ?)
        """,
        (customer_name, datetime.now().isoformat())
    )

    conversation_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return conversation_id


def save_message(conversation_id, role, message):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO messages
        (conversation_id, role, message, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            conversation_id,
            role,
            message,
            datetime.now().isoformat()
        )
    )

    connection.commit()
    connection.close()


def get_messages(conversation_id):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT role, message, created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY id ASC
        """,
        (conversation_id,)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]