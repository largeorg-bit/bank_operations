# Банковские операции

Проект для маскирования данных и обработки банковских операций.

## Модули

- `src/masks.py` — маскирование карт и счетов
- `src/widget.py` — подготовка данных для виджета
- `src/processing.py` — фильтрация и сортировка операций
- `src/generators.py` — генераторы для работы с транзакциями
- `src/decorators.py` — декораторы
- `src/utils.py` — чтение JSON-файла с операциями
- `src/external_api.py` — конвертация валют
- `src/file_reader.py` — чтение CSV и Excel

## file_reader

### read_csv_transactions

```python
from src.file_reader import read_csv_transactions

transactions = read_csv_transactions("data/transactions.csv")
print(len(transactions))
```

### read_excel_transactions

```python
from src.file_reader import read_excel_transactions

transactions = read_excel_transactions("data/transactions_excel.xlsx")
print(len(transactions))
```

## Логирование

Логи модулей `masks` и `utils` записываются в папку `logs/`.

## Тестирование

```bash
pip install pytest pytest-cov requests python-dotenv pandas openpyxl
pytest
```

Отчет о покрытии сохраняется в папке `htmlcov/`.
