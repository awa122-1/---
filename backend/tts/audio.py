from pathlib import Path
import uuid

def output_path(root: Path):
    directory = root / "audio" / "output"
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{uuid.uuid4().hex}.wav"
