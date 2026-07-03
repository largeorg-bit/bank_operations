import json
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Literal

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

TRANSACTION_COLUMNS = [
    "operation_date",
    "payment_date",
    "card_number",
    "status",
    "operation_amount",
    "operation_currency",
    "payment_amount",
    "payment_currency",
    "cashback",
    "category",
    "mcc",
    "description",
    "bonuses",
    "invest_rounding",
    "rounded_amount",
]

PeriodType = Literal["W", "M", "Y", "ALL"]

CURRENCY_API_URL = "https://api.apilayer.com/exchangerates_data/convert"
STOCK_API_URL = "https://finnhub.io/api/v1/quote"

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "utils.log")

os.makedirs(LOG_DIR, exist_ok=True)

file_formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s"
)
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def load_operations(path: str) -> list[dict[str, Any]]:
    """Загружает список банковских операций из JSON-файла."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        logger.error("Файл не найден: %s. %s", path, error)
        return []
    except json.JSONDecodeError as error:
        logger.error("Некорректный JSON в файле %s: %s", path, error)
        return []
    except OSError as error:
        logger.error("Ошибка чтения файла %s: %s", path, error)
        return []

    if not isinstance(data, list):
        logger.error("Файл %s не содержит список операций", path)
        return []

    logger.info("Загружено %s операций из файла %s", len(data), path)
    return data


def load_transactions_dataframe(path: str) -> pd.DataFrame:
    """Загружает транзакции из Excel-файла в DataFrame."""
    try:
        if path.endswith(".xls"):
            dataframe = pd.read_excel(path, engine="xlrd")
        else:
            dataframe = pd.read_excel(path)
    except FileNotFoundError:
        logger.error("Файл не найден: %s", path)
        return pd.DataFrame(columns=TRANSACTION_COLUMNS)
    except ImportError as error:
        logger.error("Не установлена библиотека для чтения Excel: %s", error)
        return pd.DataFrame(columns=TRANSACTION_COLUMNS)

    if len(dataframe.columns) >= len(TRANSACTION_COLUMNS):
        dataframe.columns = TRANSACTION_COLUMNS[: len(dataframe.columns)]

    dataframe["operation_date"] = pd.to_datetime(
        dataframe["operation_date"], dayfirst=True, errors="coerce"
    )
    dataframe["payment_date"] = pd.to_datetime(
        dataframe["payment_date"], dayfirst=True, errors="coerce"
    )
    logger.info("Загружено %s транзакций из %s", len(dataframe), path)
    return dataframe


def load_user_settings(path: str = "user_settings.json") -> dict[str, Any]:
    """Загружает пользовательские настройки."""
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        logger.error("Ошибка чтения настроек: %s", error)
        return {"user_currencies": [], "user_stocks": []}


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = current_time.hour
    if 6 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 18:
        return "Добрый день"
    if 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def parse_input_datetime(date_string: str) -> datetime:
    """Преобразует строку даты и времени в datetime."""
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")


def format_date(value: Any) -> str:
    """Форматирует дату в dd.mm.yyyy."""
    if pd.isna(value):
        return ""
    if isinstance(value, datetime):
        return value.strftime("%d.%m.%Y")
    parsed = pd.to_datetime(value, dayfirst=True, errors="coerce")
    if pd.isna(parsed):
        return str(value)
    return parsed.strftime("%d.%m.%Y")


def get_date_range(
    target_date: datetime,
    period: PeriodType = "M",
) -> tuple[datetime, datetime]:
    """Возвращает диапазон дат для анализа."""
    end_date = target_date.replace(hour=23, minute=59, second=59)

    if period == "W":
        start_date = (target_date - timedelta(days=target_date.weekday())).replace(
            hour=0, minute=0, second=0
        )
    elif period == "Y":
        start_date = target_date.replace(
            month=1, day=1, hour=0, minute=0, second=0
        )
    elif period == "ALL":
        start_date = datetime(1900, 1, 1)
    else:
        start_date = target_date.replace(day=1, hour=0, minute=0, second=0)

    return start_date, end_date


def filter_transactions_by_period(
    dataframe: pd.DataFrame,
    target_date: datetime,
    period: PeriodType = "M",
) -> pd.DataFrame:
    """Фильтрует транзакции по диапазону дат и статусу OK."""
    start_date, end_date = get_date_range(target_date, period)
    mask = (
        (dataframe["operation_date"] >= start_date)
        & (dataframe["operation_date"] <= end_date)
        & (dataframe["status"] == "OK")
    )
    return dataframe.loc[mask].copy()


def get_card_digits(card_number: Any) -> str:
    """Возвращает последние 4 цифры номера карты."""
    digits = "".join(char for char in str(card_number) if char.isdigit())
    return digits[-4:] if digits else ""


def get_currency_rates(currencies: list[str]) -> list[dict[str, float]]:
    """Возвращает курсы валют к RUB через внешний API."""
    api_key = os.getenv("API_KEY")
    rates: list[dict[str, float]] = []

    for currency in currencies:
        try:
            response = requests.get(
                CURRENCY_API_URL,
                params={"from": currency, "to": "RUB", "amount": 1},
                headers={"apikey": api_key},
                timeout=10,
            )
            response.raise_for_status()
            rate = float(response.json()["result"])
            if rate > 0:
                rates.append({"currency": currency, "rate": round(rate, 2)})
        except (requests.RequestException, KeyError, ValueError, TypeError) as error:
            logger.error("Ошибка получения курса %s: %s", currency, error)

    return rates


def get_stock_prices(stocks: list[str]) -> list[dict[str, float]]:
    """Возвращает текущие цены акций через Finnhub API."""
    api_key = os.getenv("FINNHUB_API_KEY")
    prices: list[dict[str, float]] = []

    for stock in stocks:
        try:
            response = requests.get(
                STOCK_API_URL,
                params={"symbol": stock, "token": api_key},
                timeout=10,
            )
            response.raise_for_status()
            price = float(response.json()["c"])
            if price > 0:
                prices.append({"stock": stock, "price": round(price, 2)})
        except (requests.RequestException, KeyError, ValueError, TypeError) as error:
            logger.error("Ошибка получения цены %s: %s", stock, error)

    return prices
