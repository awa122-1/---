import asyncio
from pathlib import Path

class TTSEngine:
    def __init__(self, root: Path, config: dict):
        self.root = root
        self.config = config.get("tts", {})

    async def speak(self, text):
        if not self.config.get("enabled", False):
            return None
        if self.config.get("engine") != "pyttsx3":
            raise RuntimeError("V1 当前只支持 pyttsx3")
        return await asyncio.to_thread(self._pyttsx3, text)

    def _pyttsx3(self, text):
        import pyttsx3
        from backend.tts.audio import output_path
        path = output_path(self.root)
        engine = pyttsx3.init()
        engine.setProperty("rate", self.config.get("rate", 180))
        engine.setProperty("volume", self.config.get("volume", 1.0))
        engine.save_to_file(text, str(path))
        engine.runAndWait()
        return "/audio/" + path.name if path.exists() else None
