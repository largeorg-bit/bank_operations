import pytest

from src.bank_analysis import process_bank_operations, process_bank_search


def test_process_bank_search(транзакции):
    результат = process_bank_search(транзакции, "Перевод")
    assert len(результат) == 5


def test_process_bank_search_без_совпадений(транзакции):
    assert process_bank_search(транзакции, "вклад") == []


def test_process_bank_search_регулярка(транзакции):
    результат = process_bank_search(транзакции, r"карт")
    assert len(результат) == 1
    assert результат[0]["description"] == "Перевод с карты на карту"


@pytest.mark.parametrize(
    "поиск, количество",
    [
        ("организации", 2),
        ("счета", 2),
    ],
)
def test_process_bank_search_параметры(транзакции, поиск, количество):
    assert len(process_bank_search(транзакции, поиск)) == количество


def test_process_bank_operations(транзакции):
    категории = ["Перевод организации", "Перевод с карты на карту", "Открытие вклада"]
    результат = process_bank_operations(транзакции, категории)

    assert результат["Перевод организации"] == 2
    assert результат["Перевод с карты на карту"] == 1
    assert результат["Открытие вклада"] == 0


def test_process_bank_operations_пустой_список():
    категории = ["Перевод"]
    assert process_bank_operations([], категории) == {"Перевод": 0}
