from datetime import datetime, timezone

def event(event_type: str, data: dict) -> dict:
    return {
        "type": event_type,
        "time": datetime.now(timezone.utc).isoformat(),
        "data": data
    }
