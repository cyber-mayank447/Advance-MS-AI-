import os, json, threading, re

MEMORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ms_memory.json")
_lock = threading.Lock()

def _load():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"facts": {}, "preferences": {}}

def _save(data):
    tmp = MEMORY_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, MEMORY_FILE)

def remember(key, value, category="facts"):
    with _lock:
        data = _load()
        data.setdefault(category, {})[key.strip().lower()] = value.strip()
        _save(data)
    return True

def recall(key=None, category=None):
    data = _load()
    if category:
        return data.get(category, {})
    if key:
        k = key.strip().lower()
        for group in ("facts", "preferences"):
            if k in data.get(group, {}):
                return data[group][k]
    return data

def forget(key):
    with _lock:
        data = _load()
        k = key.strip().lower()
        removed = False
        for group in ("facts", "preferences"):
            if k in data.get(group, {}):
                del data[group][k]
                removed = True
        _save(data)
        return removed

def summary():
    data = _load()
    items = []
    for group in ("facts", "preferences"):
        for k, v in data.get(group, {}).items():
            items.append(f"{k}: {v}")
    return items
