import sqlite3
from pathlib import Path

class Database:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """)
        self.conn.commit()

    def add_message(self, role, content):
        self.conn.execute("INSERT INTO messages(role,content) VALUES (?,?)", (role, content))
        self.conn.commit()

    def recent_messages(self, limit):
        rows = self.conn.execute(
            "SELECT role,content FROM messages ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return list(reversed([dict(r) for r in rows]))

    def add_memory(self, content):
        self.conn.execute("INSERT INTO memories(content) VALUES (?)", (content,))
        self.conn.commit()

    def search_memories(self, keyword, limit=8):
        rows = self.conn.execute(
            "SELECT id,content FROM memories WHERE content LIKE ? ORDER BY id DESC LIMIT ?",
            (f"%{keyword}%", limit)
        ).fetchall()
        return [dict(r) for r in rows]

    def all_memories(self, limit=8):
        rows = self.conn.execute(
            "SELECT id,content FROM memories ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
