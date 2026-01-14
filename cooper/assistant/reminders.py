import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "memory", "memory.db")

class ReminderManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                created_at TEXT
            )
        """)
        self.conn.commit()

    def add(self, text: str):
        self.cursor.execute(
            "INSERT INTO reminders VALUES (NULL, ?, ?)",
            (text, datetime.now().isoformat())
        )
        self.conn.commit()

    def list_all(self):
        self.cursor.execute(
            "SELECT text FROM reminders ORDER BY id DESC"
        )
        return [row[0] for row in self.cursor.fetchall()]
