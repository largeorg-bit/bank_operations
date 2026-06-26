import re
from collections import Counter
from typing import Any


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Возвращает операции, в описании которых найдена искомая строка."""
    pattern = re.compile(search, re.IGNORECASE)
    return [
        operation for operation in data
        if pattern.search(operation.get("description", ""))
    ]


def process_bank_operations(data: list[dict[str, Any]], categories: list) -> dict:
    """Подсчитывает количество операций по категориям в поле description."""
    counter = Counter({category: 0 for category in categories})

    for operation in data:
        description = operation.get("description", "")
        for category in categories:
            if re.search(re.escape(category), description, re.IGNORECASE):
                counter[category] += 1

    return dict(counter)
