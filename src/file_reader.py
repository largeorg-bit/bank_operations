from typing import Any

import pandas as pd


def read_csv_transactions(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла и возвращает список словарей."""
    transactions = pd.read_csv(file_path)
    return transactions.to_dict(orient="records")


def read_excel_transactions(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла и возвращает список словарей."""
    transactions = pd.read_excel(file_path)
    return transactions.to_dict(orient="records")
