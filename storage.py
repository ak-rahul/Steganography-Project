# storage.py
import json
import os
from typing import Dict

STORE_FILENAME = "files.json"

def load_store() -> Dict[str, dict]:
    if not os.path.isfile(STORE_FILENAME):
        return {}
    try:
        with open(STORE_FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_store(data: Dict[str, dict]) -> None:
    with open(STORE_FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_entry(basename: str, original_path: str, password_provided: bool):
    store = load_store()
    store[basename] = {
        "original": original_path,
        "password_provided": bool(password_provided)
    }
    save_store(store)
