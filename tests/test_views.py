from datetime import datetime
from unittest.mock import patch

import pytest

from src.utils import get_greeting, load_transactions_dataframe
from src.views import events_page_info, main_page_info


@pytest.fixture
def транзакции_df():
    return load_transactions_dataframe("data/operations.xlsx")


@pytest.mark.parametrize(
    "hour, ожидание",
    [
        (8, "Доброе утро"),
        (14, "Добрый день"),
        (20, "Добрый вечер"),
        (2, "Доброй ночи"),
    ],
)
def test_get_greeting(hour, ожидание):
    assert get_greeting(datetime(2021, 12, 20, hour, 0, 0)) == ожидание


@patch("src.views.get_stock_prices")
@patch("src.views.get_currency_rates")
def test_main_page_info(mock_rates, mock_stocks, транзакции_df):
    mock_rates.return_value = [{"currency": "USD", "rate": 73.21}]
    mock_stocks.return_value = [{"stock": "AAPL", "price": 150.12}]

    result = main_page_info("2021-12-20 15:30:00", транзакции_df)

    assert result["greeting"] == "Добрый день"
    assert len(result["cards"]) >= 1
    assert len(result["top_transactions"]) == 5
    assert result["top_transactions"][0]["date"]
    assert "currency" in result["currency_rates"][0]
    assert "rate" in result["currency_rates"][0]


@patch("src.views.get_stock_prices")
@patch("src.views.get_currency_rates")
def test_events_page_info(mock_rates, mock_stocks, транзакции_df):
    mock_rates.return_value = [{"currency": "EUR", "rate": 87.08}]
    mock_stocks.return_value = [{"stock": "TSLA", "price": 1007.08}]

    result = events_page_info("2021-12-20 15:30:00", транзакции_df)

    assert "expenses" in result
    assert "income" in result
    assert isinstance(result["expenses"]["total_amount"], int)
    assert len(result["expenses"]["main"]) >= 1
