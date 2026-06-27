from typing import Any


def filter_by_state(
    operations: list[dict[str, Any]],
    state: str = "EXECUTED",
) -> list[dict[str, Any]]:
    """Возвращает операции с заданным статусом."""
    target_state = state.strip().upper()
    return [
        operation for operation in operations
        if str(operation.get("state", "")).strip().upper() == target_state
    ]


def sort_by_date(
    operations: list[dict[str, Any]],
    reverse: bool = True,
) -> list[dict[str, Any]]:
    """Сортирует операции по дате."""
    return sorted(
        operations,
        key=lambda op: op.get("date", ""),
        reverse=reverse,
    )
