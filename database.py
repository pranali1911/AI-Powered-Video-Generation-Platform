import sqlite3
from datetime import datetime

# Define the database file name
DATABASE = "history.db"

# Function to create the database and history table
def create_database():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            video_path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()

# Function to save a new record in the history table
def save_history(prompt, video_path):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO history (prompt, video_path, created_at)
        VALUES (?, ?, ?)
    """, (
        prompt,
        video_path,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    connection.commit()

    cursor.execute("""
        DELETE FROM history
        WHERE id NOT IN (
            SELECT id
            FROM history
            ORDER BY id DESC
            LIMIT 5
        )
    """)

    connection.commit()
    connection.close()

# Function to retrieve the last 5 records from the history table
def get_history():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, prompt, video_path, created_at
        FROM history
        ORDER BY id DESC
        LIMIT 5
    """)

    records = cursor.fetchall()
    connection.close()

    return records