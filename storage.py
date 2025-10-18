# storage.py
import json
import os
from typing import Dict

STORE = "files.json"

def load_store() -> Dict[str, dict]:
    if not os.path.isfile(STORE):
        return {}
    try:
        with open(STORE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_store(data: Dict[str, dict]) -> None:
    with open(STORE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_entry(basename: str, original: str, passworded: bool) -> None:
    s = load_store()
    s[basename] = {"original": original, "passworded": bool(passworded)}
    save_store(s)
