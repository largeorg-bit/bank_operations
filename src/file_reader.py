import math
from typing import Any

import pandas as pd


def _normalize_value(value: Any) -> Any:
    """Приводит значение из pandas к формату, удобному для обработки."""
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return value


def _normalize_record(record: dict[str, Any]) -> dict[str, Any]:
    """Приводит запись из CSV или Excel к единому формату."""
    normalized = {key: _normalize_value(value) for key, value in record.items()}

    if "state" in normalized and normalized["state"] != "":
        normalized["state"] = str(normalized["state"]).strip().upper()

    for field in ("date", "description", "from", "to", "amount", "currency_name", "currency_code"):
        if field in normalized and normalized[field] != "":
            normalized[field] = str(normalized[field])

    if "operationAmount" not in normalized and "amount" in normalized:
        normalized["operationAmount"] = {
            "amount": str(normalized.get("amount", "")),
            "currency": {
                "name": str(normalized.get("currency_name", "")),
                "code": str(normalized.get("currency_code", "")),
            },
        }

    return normalized


def read_csv_transactions(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей."""
    transactions = pd.read_csv(
        file_path,
        encoding="utf-8-sig",
        sep=None,
        engine="python",
    )
    return [_normalize_record(record) for record in transactions.to_dict(orient="records")]


def read_excel_transactions(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла и возвращает список словарей."""
    transactions = pd.read_excel(file_path)
    return [_normalize_record(record) for record in transactions.to_dict(orient="records")]
