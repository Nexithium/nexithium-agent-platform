import json
import os
from typing import List, Dict

MEMORY_DIR = "memory_logs"
os.makedirs(MEMORY_DIR, exist_ok=True)

class ShortTermMemory:
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.memory: List[Dict[str, str]] = []

    def add(self, role: str, content: str):
        self.memory.append({"role": role, "content": content})
        self.memory = self.memory[-self.window_size * 2:]  # user+assistant

    def get(self) -> List[Dict[str, str]]:
        return self.memory

    def clear(self):
        self.memory = []

class PersistentMemory:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.file_path = os.path.join(MEMORY_DIR, f"{user_id}.json")
        self.memory: List[Dict[str, str]] = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2)

    def add(self, role: str, content: str):
        self.memory.append({"role": role, "content": content})
        self.memory = self.memory[-50:]  # limit log size
        self.save()

    def get(self) -> List[Dict[str, str]]:
        return self.memory

    def clear(self):
        self.memory = []
        self.save()

class MemoryManager:
    def __init__(self):
        self.sessions = {}

    def get_memory(self, user_id: str) -> PersistentMemory:
        if user_id not in self.sessions:
            self.sessions[user_id] = PersistentMemory(user_id)
        return self.sessions[user_id]
