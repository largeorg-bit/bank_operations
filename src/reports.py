import json
import os
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

import pandas as pd

REPORTS_DIR = "reports"


def report_writer(filename: Optional[str] = None) -> Callable:
    """Декоратор для сохранения результата отчета в файл."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            os.makedirs(REPORTS_DIR, exist_ok=True)
            result = func(*args, **kwargs)
            report_name = filename or f"{func.__name__}.json"
            report_path = f"{REPORTS_DIR}/{report_name}"

            with open(report_path, "w", encoding="utf-8") as file:
                if isinstance(result, pd.DataFrame):
                    file.write(result.to_json(orient="records", force_ascii=False, indent=2))
                else:
                    json.dump(result, file, ensure_ascii=False, indent=2, default=str)

            return result
        return wrapper
    return decorator


def _get_expenses_dataframe(
    transactions: pd.DataFrame,
    reference_date: Optional[str] = None,
) -> pd.DataFrame:
    """Возвращает траты за последние три месяца."""
    end_date = (
        datetime.strptime(reference_date, "%Y-%m-%d")
        if reference_date
        else datetime.now()
    )
    start_date = end_date - pd.DateOffset(months=3)
    expenses = transactions[
        (transactions["operation_date"] >= start_date)
        & (transactions["operation_date"] <= end_date)
        & (transactions["payment_amount"] < 0)
        & (transactions["status"] == "OK")
    ].copy()
    expenses["payment_amount"] = expenses["payment_amount"].abs()
    return expenses


@report_writer()
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """Возвращает траты по категории за последние три месяца."""
    expenses = _get_expenses_dataframe(transactions, date)
    filtered = expenses[expenses["category"] == category]
    grouped = (
        filtered.groupby(filtered["operation_date"].dt.to_period("M"))["payment_amount"]
        .sum()
        .reset_index()
    )
    grouped["operation_date"] = grouped["operation_date"].astype(str)
    grouped.columns = ["month", "amount"]
    return grouped


@report_writer("spending_by_weekday.json")
def spending_by_weekday(
    transactions: pd.DataFrame,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """Возвращает средние траты по дням недели за три месяца."""
    expenses = _get_expenses_dataframe(transactions, date)
    weekday_names = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье",
    }
    expenses["weekday"] = expenses["operation_date"].dt.weekday.map(weekday_names)
    grouped = (
        expenses.groupby("weekday")["payment_amount"]
        .mean()
        .reset_index()
        .rename(columns={"payment_amount": "average_amount"})
    )
    return grouped


@report_writer("spending_by_workday.json")
def spending_by_workday(
    transactions: pd.DataFrame,
    date: Optional[str] = None,
) -> pd.DataFrame:
    """Возвращает средние траты в рабочий и выходной день."""
    expenses = _get_expenses_dataframe(transactions, date)
    expenses["day_type"] = expenses["operation_date"].dt.weekday.apply(
        lambda value: "Рабочий" if value < 5 else "Выходной"
    )
    grouped = (
        expenses.groupby("day_type")["payment_amount"]
        .mean()
        .reset_index()
        .rename(columns={"payment_amount": "average_amount"})
    )
    return grouped
