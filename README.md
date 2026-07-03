# Банковские операции

Курсовой проект для анализа банковских транзакций.

## Установка

```bash
pip install -r requirements.txt
copy .env_template .env
```

## Структура

- `src/views.py` — JSON для веб-страниц
- `src/services.py` — сервисы поиска
- `src/reports.py` — отчеты
- `src/utils.py` — загрузка данных
- `data/operations.xlsx` — транзакции
- `user_settings.json` — валюты и акции

## Запуск

```bash
python -m src.main
```

## Тестирование

```bash
pytest
```
