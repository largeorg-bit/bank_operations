import math
import re
from typing import Any

import pandas as pd

PHONE_PATTERN = re.compile(
    r"(?:\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"
)
PERSON_TRANSFER_PATTERN = re.compile(
    r"^[А-ЯЁ][а-яё]+\s[А-ЯЁ]\.$"
)


def simple_search(
    transactions: list[dict[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    """Ищет транзакции по подстроке в описании или категории."""
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    return [
        transaction for transaction in transactions
        if pattern.search(str(transaction.get("description", "")))
        or pattern.search(str(transaction.get("category", "")))
    ]


def search_by_phone(
    transactions: list[dict[str, Any]],
    phone_template: str,
) -> list[dict[str, Any]]:
    """Ищет транзакции по шаблону телефонного номера."""
    template_digits = re.sub(r"\D", "", phone_template)
    if template_digits.startswith("8"):
        template_digits = "7" + template_digits[1:]
    search_digits = template_digits[-10:]

    result: list[dict[str, Any]] = []
    for transaction in transactions:
        description = str(transaction.get("description", ""))
        for phone in PHONE_PATTERN.findall(description):
            phone_digits = re.sub(r"\D", "", phone)
            if phone_digits.startswith("8"):
                phone_digits = "7" + phone_digits[1:]
            if phone_digits.endswith(search_digits):
                result.append(transaction)
                break
    return result


def search_person_transfers(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Возвращает переводы физическим лицам."""
    return [
        transaction for transaction in transactions
        if str(transaction.get("category", "")) == "Переводы"
        and PERSON_TRANSFER_PATTERN.match(str(transaction.get("description", "")).strip())
    ]


def investment_bank(
    month: str,
    transactions: list[dict[str, Any]],
    limit: int,
) -> float:
    """Считает сумму, которую можно отложить в Инвесткопилку."""
    total = 0.0
    for transaction in transactions:
        operation_date = str(transaction.get("operation_date", ""))[:7]
        payment_amount = float(transaction.get("payment_amount", 0))
        if operation_date == month and payment_amount < 0:
            amount = abs(payment_amount)
            rounded = math.ceil(amount / limit) * limit
            total += rounded - amount
    return round(total, 2)


def analyze_cashback_categories(
    data: list[dict[str, Any]],
    year: int,
    month: int,
) -> dict[str, int]:
    """Анализирует потенциальный кешбэк по категориям за месяц."""
    month_prefix = f"{year:04d}-{month:02d}"
    categories: dict[str, float] = {}

    for transaction in data:
        operation_date = str(transaction.get("operation_date", ""))
        payment_amount = float(transaction.get("payment_amount", 0))
        if operation_date.startswith(month_prefix) and payment_amount < 0:
            category = str(transaction.get("category", "Без категории"))
            categories[category] = categories.get(category, 0) + abs(payment_amount) / 100

    return {
        category: int(round(amount))
        for category, amount in sorted(
            categories.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    }


def transactions_to_records(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    """Преобразует DataFrame в список словарей для сервисов."""
    records = dataframe.copy()
    records["operation_date"] = records["operation_date"].dt.strftime("%Y-%m-%d")
    records["payment_date"] = records["payment_date"].dt.strftime("%Y-%m-%d")
    return records.to_dict(orient="records")
