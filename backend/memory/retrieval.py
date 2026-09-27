import re

def keywords(text: str) -> list[str]:
    parts = re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z0-9_]{3,}", text)
    return list(dict.fromkeys(parts[:8]))
