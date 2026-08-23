import os
import json
from datetime import datetime

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "memory.json")

def _load():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data[-200:], f, ensure_ascii=False, indent=2)

def remember(text):
    text = str(text).strip()
    if not text:
        return
    data = _load()
    data.append({"time": datetime.now().isoformat(timespec="seconds"), "text": text})
    _save(data)

def recall(limit=8):
    return _load()[-limit:]

def clear():
    _save([])

def context(limit=8):
    items = recall(limit)
    return "\n".join(f"- {x['text']}" for x in items)

def conversation_context(limit=12):
    items = recall(limit)
    if not items:
        return ""
    return "\n".join(f"{x['time']}: {x['text']}" for x in items)
