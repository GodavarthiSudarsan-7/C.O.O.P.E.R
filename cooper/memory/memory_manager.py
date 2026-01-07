import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "memory.db")

class MemoryManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            key TEXT,
            value TEXT,
            timestamp TEXT
        )
        """)
        self.conn.commit()

    def remember(self, category, key, value):
        self.cursor.execute(
            "INSERT INTO memory VALUES (NULL, ?, ?, ?, ?)",
            (category, key, value, datetime.now().isoformat())
        )
        self.conn.commit()

    def recall(self, key):
        self.cursor.execute(
            "SELECT value FROM memory WHERE key=? ORDER BY id DESC LIMIT 1",
            (key,)
        )
        row = self.cursor.fetchone()
        return row[0] if row else None

    def recent_interactions(self, limit=5):
        self.cursor.execute(
            "SELECT value FROM memory WHERE category='interaction' ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return [r[0] for r in self.cursor.fetchall()]
