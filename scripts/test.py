from pathlib import Path
from backend.emotion.detector import EmotionDetector
from backend.memory.database import Database

ROOT=Path(__file__).resolve().parents[1]
detector=EmotionDetector(ROOT/"config"/"emotions.json")
print("emotion:",detector.detect("哇！太好了，真的很开心！"))
db=Database(ROOT/"data"/"test.db")
db.add_message("user","你好")
print("messages:",db.recent_messages(5))
