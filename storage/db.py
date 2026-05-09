import json

from pathlib import Path
from datetime import datetime

DB_FILE = Path("storage/history.json")


def save_analysis(data: dict):
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "ticker": data["ticker"],
        "sentiment": data["sentiment"]["sentiment"],
        "confidence": data["sentiment"]["confidence"],
        "report": data["report"],
    }

    if DB_FILE.exists():
        history = json.loads(DB_FILE.read_text())
    else:
        history = []

    history.append(record)

    DB_FILE.write_text(json.dumps(history, indent=2))


def get_history():
    if not DB_FILE.exists():
        return []
    return json.loads(DB_FILE.read_text())