# Банковские операции

Проект для маскирования данных и обработки банковских операций.

## Модули

- `src/masks.py` — маскирование карт и счетов
- `src/widget.py` — подготовка данных для виджета
- `src/processing.py` — фильтрация и сортировка операций
- `src/bank_analysis.py` — поиск и подсчет категорий
- `src/utils.py`, `src/file_reader.py`, `src/external_api.py` — работа с данными
- `main.py` — интерфейс программы

## bank_analysis

### process_bank_search

```python
from src.bank_analysis import process_bank_search

result = process_bank_search(transactions, "Перевод")
```

### process_bank_operations

```python
from src.bank_analysis import process_bank_operations

categories = ["Перевод организации"]
stats = process_bank_operations(transactions, categories)
```

## Запуск программы

```bash
python main.py
```

## Тестирование

```bash
pytest
```
