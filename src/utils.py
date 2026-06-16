import json
from typing import Any


def load_operations(path: str) -> list[dict[str, Any]]:
    """Загружает список банковских операций из JSON-файла."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return data
