from typing import Any

import pandas as pd

from src.utils import (PeriodType, filter_transactions_by_period, format_date,
                       get_card_digits, get_currency_rates, get_greeting,
                       get_stock_prices, load_user_settings,
                       parse_input_datetime)


def _build_cards_info(dataframe: pd.DataFrame) -> list[dict[str, float]]:
    """Формирует информацию по картам."""
    expenses = dataframe[dataframe["payment_amount"] < 0].copy()
    cards: list[dict[str, float]] = []

    for card_number, group in expenses.groupby("card_number"):
        total_spent = round(abs(group["payment_amount"].sum()), 2)
        cards.append({
            "last_digits": get_card_digits(card_number),
            "total_spent": total_spent,
            "cashback": round(total_spent / 100, 2),
        })

    return cards


def _build_top_transactions(dataframe: pd.DataFrame) -> list[dict[str, Any]]:
    """Формирует топ-5 транзакций по сумме платежа."""
    top = dataframe.sort_values("payment_amount", ascending=False).head(5)
    result: list[dict[str, Any]] = []

    for _, row in top.iterrows():
        result.append({
            "date": format_date(row["payment_date"]),
            "amount": round(float(row["payment_amount"]), 2),
            "category": str(row["category"]),
            "description": str(row["description"]),
        })

    return result


def _group_by_category(
    dataframe: pd.DataFrame,
    top_count: int = 7,
    other_label: str = "Остальное",
) -> list[dict[str, int]]:
    """Группирует суммы по категориям с выделением топ-N."""
    grouped = (
        dataframe.groupby("category")["payment_amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )
    main_categories: list[dict[str, int]] = []

    for index, (category, amount) in enumerate(grouped.items()):
        if index < top_count:
            main_categories.append({
                "category": str(category),
                "amount": int(round(amount)),
            })
        else:
            other_amount = int(round(grouped.iloc[top_count:].sum()))
            if other_amount > 0:
                main_categories.append({
                    "category": other_label,
                    "amount": other_amount,
                })
            break

    return main_categories


def main_page_info(
    date_string: str,
    transactions: pd.DataFrame,
) -> dict[str, Any]:
    """Возвращает JSON для главной страницы."""
    target_date = parse_input_datetime(date_string)
    period_data = filter_transactions_by_period(transactions, target_date, "M")
    settings = load_user_settings()

    return {
        "greeting": get_greeting(target_date),
        "cards": _build_cards_info(period_data),
        "top_transactions": _build_top_transactions(period_data),
        "currency_rates": get_currency_rates(settings.get("user_currencies", [])),
        "stock_prices": get_stock_prices(settings.get("user_stocks", [])),
    }


def events_page_info(
    date_string: str,
    transactions: pd.DataFrame,
    period: PeriodType = "M",
) -> dict[str, Any]:
    """Возвращает JSON для страницы событий."""
    target_date = parse_input_datetime(date_string)
    period_data = filter_transactions_by_period(transactions, target_date, period)
    settings = load_user_settings()

    expenses = period_data[period_data["payment_amount"] < 0].copy()
    income = period_data[period_data["payment_amount"] > 0].copy()

    expenses["payment_amount"] = expenses["payment_amount"].abs()
    transfer_categories = ["Наличные", "Переводы"]

    return {
        "expenses": {
            "total_amount": int(round(expenses["payment_amount"].sum())),
            "main": _group_by_category(expenses),
            "transfers_and_cash": sorted(
                [
                    {
                        "category": category,
                        "amount": int(round(
                            expenses.loc[
                                expenses["category"] == category, "payment_amount"
                            ].sum()
                        )),
                    }
                    for category in transfer_categories
                    if category in expenses["category"].values
                ],
                key=lambda item: item["amount"],
                reverse=True,
            ),
        },
        "income": {
            "total_amount": int(round(income["payment_amount"].sum())),
            "main": _group_by_category(income),
        },
        "currency_rates": get_currency_rates(settings.get("user_currencies", [])),
        "stock_prices": get_stock_prices(settings.get("user_stocks", [])),
    }
