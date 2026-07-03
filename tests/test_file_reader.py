from unittest.mock import MagicMock, patch

from src.file_reader import read_csv_transactions, read_excel_transactions
from src.processing import filter_by_state


@patch("src.file_reader.pd.read_csv")
def test_read_csv_transactions(mock_read_csv):
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [
        {
            "id": 939719570,
            "state": "executed",
            "description": "Перевод организации",
            "amount": 9824.07,
            "currency_name": "USD",
            "currency_code": "USD",
        },
    ]
    mock_read_csv.return_value = mock_df

    результат = read_csv_transactions("data/transactions.csv")

    mock_read_csv.assert_called_once_with(
        "data/transactions.csv",
        encoding="utf-8-sig",
        sep=None,
        engine="python",
    )
    assert len(результат) == 1
    assert результат[0]["state"] == "EXECUTED"
    assert "operationAmount" in результат[0]


@patch("src.file_reader.pd.read_csv")
def test_read_csv_transactions_пустой_файл(mock_read_csv):
    mock_df = MagicMock()
    mock_df.to_dict.return_value = []
    mock_read_csv.return_value = mock_df

    assert read_csv_transactions("data/empty.csv") == []


@patch("src.file_reader.pd.read_excel")
def test_read_excel_transactions(mock_read_excel):
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [
        {
            "id": 873106923,
            "state": "EXECUTED",
            "description": "Перевод со счета на счет",
            "from": float("nan"),
            "to": "Счет 74489636417521191160",
            "amount": 43318.34,
            "currency_name": "руб.",
            "currency_code": "RUB",
        },
    ]
    mock_read_excel.return_value = mock_df

    результат = read_excel_transactions("data/transactions_excel.xlsx")

    mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx")
    assert len(результат) == 1
    assert результат[0]["from"] == ""


@patch("src.file_reader.pd.read_excel")
def test_read_excel_transactions_пустой_файл(mock_read_excel):
    mock_df = MagicMock()
    mock_df.to_dict.return_value = []
    mock_read_excel.return_value = mock_df

    assert read_excel_transactions("data/empty.xlsx") == []


def test_read_csv_transactions_фильтрация_по_статусу():
    данные = read_csv_transactions("data/transactions.csv")
    executed = filter_by_state(данные, "EXECUTED")
    assert len(executed) >= 1
