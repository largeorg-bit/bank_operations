import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/convert"
API_KEY = os.getenv("API_KEY")


def get_amount_transaction_in_rub(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях."""
    amount = float(transaction["operationAmount"]["amount"])
    currency = transaction["operationAmount"]["currency"]["code"]

    if currency == "RUB":
        return amount

    if currency in ("USD", "EUR"):
        return _convert_to_rub(amount, currency)

    return amount


def _convert_to_rub(amount: float, currency: str) -> float:
    """Конвертирует сумму из USD или EUR в рубли через внешний API."""
    response = requests.get(
        API_URL,
        params={"to": "RUB", "from": currency, "amount": amount},
        headers={"apikey": API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    return float(response.json()["result"])
