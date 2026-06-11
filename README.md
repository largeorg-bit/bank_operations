# Банковские операции

Проект для маскирования данных и обработки банковских операций.

## Модули

- `src/masks.py` — маскирование карт и счетов
- `src/widget.py` — подготовка данных для виджета
- `src/processing.py` — фильтрация и сортировка операций
- `src/generators.py` — генераторы для работы с транзакциями

## generators

### filter_by_currency

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
print(next(usd_transactions))
```

### transaction_descriptions

```python
from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
print(next(descriptions))
```

### card_number_generator

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
```

## Тестирование

```bash
pip install pytest pytest-cov
pytest
```

Отчет о покрытии сохраняется в папке `htmlcov/`.