from src.services import (analyze_cashback_categories, investment_bank,
                          search_by_phone, search_person_transfers,
                          simple_search)


def test_simple_search():
    data = [
        {"description": "Лента", "category": "Супермаркеты"},
        {"description": "Ozon.ru", "category": "Различные товары"},
    ]
    result = simple_search(data, "ozon")
    assert len(result) == 1


def test_investment_bank():
    data = [
        {"operation_date": "2021-12-01", "payment_amount": -1712.0},
        {"operation_date": "2021-11-01", "payment_amount": -100.0},
    ]
    assert investment_bank("2021-12", data, 50) == 38.0


def test_search_by_phone():
    data = [
        {"description": "МТС +7 900 000-00-00"},
        {"description": "Покупка в магазине"},
    ]
    result = search_by_phone(data, "+7 (900) 000-00-00")
    assert len(result) == 1


def test_search_person_transfers():
    data = [
        {"category": "Переводы", "description": "Сергей З."},
        {"category": "Переводы", "description": "Компания ООО"},
    ]
    assert len(search_person_transfers(data)) == 1


def test_analyze_cashback_categories():
    data = [
        {
            "operation_date": "2021-12-01",
            "payment_amount": -5000.0,
            "category": "Фастфуд",
        },
    ]
    result = analyze_cashback_categories(data, 2021, 12)
    assert result["Фастфуд"] == 50
