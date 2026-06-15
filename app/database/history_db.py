import os
import sqlite3
from datetime import datetime


class HistoryDB:
    def __init__(self, db_path="downloads/history.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def create_table(self):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            url TEXT,
            title TEXT,
            filename TEXT,
            quality TEXT,
            status TEXT,
            created_at TEXT
        )
        """)

        conn.commit()
        conn.close()

    def add_download(self, platform, url, title, filename, quality, status):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO downloads
        (platform, url, title, filename, quality, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            platform,
            url,
            title,
            filename,
            quality,
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

    def get_history(self, limit=100):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
        SELECT id, platform, url, title, filename, quality, status, created_at
        FROM downloads
        ORDER BY id DESC
        LIMIT ?
        """, (limit,))

        rows = cur.fetchall()
        conn.close()
        return rows

    def clear_history(self):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM downloads")
        conn.commit()
        conn.close()
