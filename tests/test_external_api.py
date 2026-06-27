from unittest.mock import MagicMock, patch

from src.external_api import get_amount_transaction_in_rub


def test_get_amount_transaction_in_rub_рубли(транзакции):
    рублевая = транзакции[2]
    assert get_amount_transaction_in_rub(рублевая) == 43318.34


@patch("src.external_api.requests.get")
def test_get_amount_transaction_in_rub_usd(mock_get, транзакции):
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 900000.0}
    mock_get.return_value = mock_response

    usd = транзакции[0]
    результат = get_amount_transaction_in_rub(usd)

    assert результат == 900000.0
    mock_get.assert_called_once()
    params = mock_get.call_args.kwargs["params"]
    assert params["from"] == "USD"
    assert params["to"] == "RUB"
    assert params["amount"] == 9824.07


@patch("src.external_api.requests.get")
def test_get_amount_transaction_in_rub_eur(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 9500.0}
    mock_get.return_value = mock_response

    eur_транзакция = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {"code": "EUR"},
        }
    }
    assert get_amount_transaction_in_rub(eur_транзакция) == 9500.0
    assert mock_get.call_args.kwargs["params"]["from"] == "EUR"
