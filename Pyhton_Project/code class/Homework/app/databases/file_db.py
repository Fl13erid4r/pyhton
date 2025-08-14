import json
import threading
from typing import Any

_lock = threading.Lock()


def read_json(path: str) -> Any:
    with _lock:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # if corrupted, return empty but caller may decide
            return []


def write_json(path: str, data: Any) -> None:
    with _lock:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)