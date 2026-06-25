from unittest.mock import MagicMock, patch

from src.file_reader import read_csv_transactions, read_excel_transactions


@patch("src.file_reader.pd.read_csv")
def test_read_csv_transactions(mock_read_csv):
    mock_df = MagicMock()
    mock_df.to_dict.return_value = [
        {"id": 939719570, "state": "EXECUTED", "description": "Перевод организации"},
    ]
    mock_read_csv.return_value = mock_df

    результат = read_csv_transactions("data/transactions.csv")

    mock_read_csv.assert_called_once_with("data/transactions.csv")
    assert len(результат) == 1
    assert результат[0]["id"] == 939719570


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
        {"id": 873106923, "state": "EXECUTED", "description": "Перевод со счета на счет"},
    ]
    mock_read_excel.return_value = mock_df

    результат = read_excel_transactions("data/transactions_excel.xlsx")

    mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx")
    assert len(результат) == 1
    assert результат[0]["id"] == 873106923


@patch("src.file_reader.pd.read_excel")
def test_read_excel_transactions_пустой_файл(mock_read_excel):
    mock_df = MagicMock()
    mock_df.to_dict.return_value = []
    mock_read_excel.return_value = mock_df

    assert read_excel_transactions("data/empty.xlsx") == []
