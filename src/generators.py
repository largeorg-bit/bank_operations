from collections.abc import Generator, Iterator
from typing import Any


def _get_currency_code(transaction: dict[str, Any]) -> str:
    """Возвращает код валюты из транзакции."""
    currency = transaction.get("operationAmount", {}).get("currency", {})
    if isinstance(currency, dict):
        return str(currency.get("code", ""))
    return str(currency)


def filter_by_currency(
    transactions: list[dict[str, Any]],
    currency: str,
) -> Iterator[dict[str, Any]]:
    """Возвращает итератор транзакций с заданной валютой."""
    for transaction in transactions:
        if _get_currency_code(transaction) == currency:
            yield transaction


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Generator[str, None, None]:
    """Возвращает описания транзакций по одному."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(
    start: int,
    stop: int,
) -> Generator[str, None, None]:
    """Генерирует номера банковских карт в заданном диапазоне."""
    for number in range(start, stop + 1):
        card = str(number).zfill(16)
        yield f"{card[:4]} {card[4:8]} {card[8:12]} {card[12:16]}"
