from pathlib import Path
import httpx

from backend.ai.personality import load_personality
from backend.ai.prompt import build_system_prompt
from backend.ai.response import clean_response
from backend.memory.manager import MemoryManager
from backend.utils.logger import get_logger

class AIBrain:
    def __init__(self, root: Path, config: dict):
        self.root = root
        self.config = config
        self.personality = load_personality(root / "config" / "personality.json")
        self.memory = MemoryManager(root, config)
        self.logger = get_logger("ai", root)

    async def chat(self, user_text: str) -> dict:
        self.memory.add_message("user", user_text)
        memories = self.memory.retrieve(user_text)
        recent = self.memory.recent_messages(
            int(self.config["memory"].get("recent_messages", 12))
        )

        messages = [{"role": "system",
                     "content": build_system_prompt(self.personality, memories)}]
        messages.extend({"role": m["role"], "content": m["content"]} for m in recent)

        provider = self.config["llm"]["provider"].lower()
        if provider == "ollama":
            text = await self._ollama(messages)
        elif provider == "openai_compatible":
            text = await self._openai_compatible(messages)
        else:
            raise RuntimeError(f"未知 LLM provider: {provider}")

        text = clean_response(text)
        self.memory.add_message("assistant", text)
        return {"text": text, "memory_saved": self.memory.maybe_save_fact(user_text)}

    async def _ollama(self, messages: list[dict]) -> str:
        cfg = self.config["llm"]
        url = cfg["base_url"].rstrip("/") + "/api/chat"
        payload = {
            "model": cfg["model"], "messages": messages, "stream": False,
            "options": {"temperature": cfg.get("temperature", 0.8)}
        }
        async with httpx.AsyncClient(timeout=float(cfg.get("timeout_seconds", 120))) as c:
            r = await c.post(url, json=payload)
            r.raise_for_status()
            return r.json()["message"]["content"]

    async def _openai_compatible(self, messages: list[dict]) -> str:
        cfg = self.config["llm"]
        url = cfg["base_url"].rstrip("/") + "/v1/chat/completions"
        headers = {}
        if cfg.get("api_key"):
            headers["Authorization"] = f"Bearer {cfg['api_key']}"
        payload = {
            "model": cfg["model"], "messages": messages,
            "temperature": cfg.get("temperature", 0.8),
            "max_tokens": cfg.get("max_tokens", 300)
        }
        async with httpx.AsyncClient(timeout=float(cfg.get("timeout_seconds", 120))) as c:
            r = await c.post(url, json=payload, headers=headers)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
