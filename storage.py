# storage.py
import json
import os
from typing import Dict

STORE_FILE = "files.json"

def load_store() -> Dict[str, Dict]:
    if not os.path.isfile(STORE_FILE):
        return {}
    try:
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_store(data: Dict[str, Dict]):
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_entry(basename: str, original_path: str, password_used: bool):
    s = load_store()
    s[basename] = {"original": original_path, "password_used": bool(password_used)}
    save_store(s)
