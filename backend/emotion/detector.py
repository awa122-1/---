import json
from pathlib import Path

class EmotionDetector:
    def __init__(self, path: Path):
        with path.open("r", encoding="utf-8") as f:
            self.words = json.load(f)

    def detect(self, text: str) -> str:
        scores = {e: sum(w in text for w in words) for e, words in self.words.items()}
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else "neutral"
