from unittest.mock import patch

from main import main


@patch("main._print_operation")
@patch("builtins.input", side_effect=[
    "1",
    "EXECUTED",
    "no",
    "no",
    "no",
])
def test_main_выводит_операции(mock_input, mock_print, capsys):
    main()
    captured = capsys.readouterr()
    assert "JSON" in captured.out
    assert "Всего банковских операций в выборке:" in captured.out
    assert mock_print.called


@patch("builtins.input", side_effect=[
    "1",
    "test",
    "EXECUTED",
    "no",
    "no",
    "no",
])
def test_main_неверный_статус(mock_input, capsys):
    main()
    captured = capsys.readouterr()
    assert 'Статус операции "TEST" недоступен.' in captured.out


@patch("builtins.input", side_effect=[
    "1",
    "PENDING",
    "no",
    "no",
    "no",
])
def test_main_пустая_выборка(mock_input, capsys):
    main()
    captured = capsys.readouterr()
    assert "Не найдено ни одной транзакции" in captured.out
