import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "статус, количество",
    [
        ("EXECUTED", 3),
        ("CANCELED", 1),
        ("PENDING", 0),
    ],
)
def test_фильтрация_по_статусу(операции, статус, количество):
    результат = filter_by_state(операции, статус)
    assert len(результат) == количество
    for операция in результат:
        assert операция["state"] == статус


def test_фильтрация_пустого_списка():
    assert filter_by_state([], "EXECUTED") == []


def test_фильтрация_без_совпадений(операции):
    assert filter_by_state(операции, "UNKNOWN") == []


def test_сортировка_по_убыванию(операции):
    результат = sort_by_date(операции, reverse=True)
    даты = [операция["date"] for операция in результат]
    assert даты == sorted(даты, reverse=True)


def test_сортировка_по_возрастанию(операции):
    результат = sort_by_date(операции, reverse=False)
    даты = [операция["date"] for операция in результат]
    assert даты == sorted(даты)


def test_сортировка_одинаковых_дат():
    данные = [
        {"id": 1, "date": "2024-01-01T10:00:00.000000"},
        {"id": 2, "date": "2024-01-01T10:00:00.000000"},
    ]
    результат = sort_by_date(данные)
    assert len(результат) == 2


def test_сортировка_пустого_списка():
    assert sort_by_date([]) == []
