import json
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "utils.log")

os.makedirs(LOG_DIR, exist_ok=True)

file_formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s"
)
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def load_operations(path: str) -> list[dict[str, Any]]:
    """Загружает список банковских операций из JSON-файла."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        logger.error("Файл не найден: %s. %s", path, error)
        return []
    except json.JSONDecodeError as error:
        logger.error("Некорректный JSON в файле %s: %s", path, error)
        return []
    except OSError as error:
        logger.error("Ошибка чтения файла %s: %s", path, error)
        return []

    if not isinstance(data, list):
        logger.error("Файл %s не содержит список операций", path)
        return []

    logger.info("Загружено %s операций из файла %s", len(data), path)
    return data
