import re
from pathlib import Path
from backend.memory.database import Database
from backend.memory.retrieval import keywords

class MemoryManager:
    def __init__(self, root: Path, config: dict):
        self.config = config
        self.db = Database(root / "data" / "fjai.db")

    def add_message(self, role, content):
        self.db.add_message(role, content)

    def recent_messages(self, limit):
        return self.db.recent_messages(limit)

    def retrieve(self, query):
        found = []
        for key in keywords(query):
            found.extend(self.db.search_memories(key, 3))
        if not found:
            found = self.db.all_memories(
                int(self.config["memory"].get("max_memories", 8))
            )
        unique = {x["id"]: x for x in found}
        return list(unique.values())[:int(self.config["memory"].get("max_memories", 8))]

    def maybe_save_fact(self, text):
        patterns = [r"我叫(.+)", r"我的名字是(.+)", r"我喜欢(.+)",
                    r"我不喜欢(.+)", r"我是(.+)"]
        for pattern in patterns:
            if re.search(pattern, text):
                self.db.add_memory(f"用户说：{text.strip()}")
                return True
        return False
