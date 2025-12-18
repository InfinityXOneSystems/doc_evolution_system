from datetime import datetime
def detect_changes():
    return {"generated_at": datetime.utcnow().isoformat(), "changes": []}
