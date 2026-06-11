import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


@pytest.mark.parametrize(
    "валюта, количество",
    [
        ("USD", 3),
        ("RUB", 2),
        ("EUR", 0),
    ],
)
def test_filter_by_currency(транзакции, валюта, количество):
    результат = list(filter_by_currency(транзакции, валюта))
    assert len(результат) == количество
    for транзакция in результат:
        код = транзакция["operationAmount"]["currency"]["code"]
        assert код == валюта


def test_filter_by_currency_итератор(транзакции):
    usd = filter_by_currency(транзакции, "USD")
    assert next(usd)["id"] == 939719570
    assert next(usd)["id"] == 142264268


def test_filter_by_currency_пустой_список():
    assert list(filter_by_currency([], "USD")) == []


def test_filter_by_currency_строковая_валюта():
    данные = [{"operationAmount": {"currency": "USD"}, "id": 1}]
    assert list(filter_by_currency(данные, "USD"))[0]["id"] == 1


def test_transaction_descriptions(транзакции):
    описания = transaction_descriptions(транзакции)
    assert next(описания) == "Перевод организации"
    assert next(описания) == "Перевод со счета на счет"


def test_transaction_descriptions_все(транзакции):
    описания = list(transaction_descriptions(транзакции))
    assert len(описания) == 5
    assert описания[3] == "Перевод с карты на карту"


def test_transaction_descriptions_пустой_список():
    assert list(transaction_descriptions([])) == []


@pytest.mark.parametrize(
    "start, stop, ожидаемые",
    [
        (1, 3, [
            "0000 0000 0000 0001",
            "0000 0000 0000 0002",
            "0000 0000 0000 0003",
        ]),
        (5, 5, ["0000 0000 0000 0005"]),
    ],
)
def test_card_number_generator(start, stop, ожидаемые):
    assert list(card_number_generator(start, stop)) == ожидаемые


def test_card_number_generator_формат():
    номер = next(card_number_generator(1234567890123456, 1234567890123456))
    assert номер == "1234 5678 9012 3456"
    assert len(номер) == 19


def test_card_number_generator_пустой_диапазон():
    assert list(card_number_generator(5, 4)) == []
