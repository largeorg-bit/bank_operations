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

## utils

### load_operations

```python
from src.utils import load_operations

operations = load_operations("data/operations.json")
print(len(operations))
```

## external_api

### get_amount_transaction_in_rub

```python
from src.external_api import get_amount_transaction_in_rub

amount_rub = get_amount_transaction_in_rub(transaction)
print(amount_rub)
```

Для работы с API скопируйте `.env.example` в `.env` и укажите ключ `API_KEY`.

## Тестирование

```bash
pip install pytest pytest-cov requests python-dotenv
pytest
```

Отчет о покрытии сохраняется в папке `htmlcov/`.
