from typing import Any

from src.bank_analysis import process_bank_search
from src.file_reader import read_csv_transactions, read_excel_transactions
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.utils import load_operations
from src.widget import get_date, mask_account_card

JSON_PATH = "data/operations.json"
CSV_PATH = "data/transactions.csv"
XLSX_PATH = "data/transactions_excel.xlsx"
VALID_STATUSES = ("EXECUTED", "CANCELED", "PENDING")


def _is_yes(answer: str) -> bool:
    """Проверяет, является ли ответ положительным."""
    return answer.strip().lower() in ("да", "yes")


def _get_currency_code(operation: dict[str, Any]) -> str:
    """Возвращает код валюты операции."""
    if "currency_code" in operation:
        return str(operation.get("currency_code", ""))
    return str(operation.get("operationAmount", {}).get("currency", {}).get("code", ""))


def _get_amount(operation: dict[str, Any]) -> str:
    """Возвращает сумму операции."""
    if "operationAmount" in operation:
        return str(operation["operationAmount"].get("amount", ""))
    return str(operation.get("amount", ""))


def _format_amount(operation: dict[str, Any]) -> str:
    """Форматирует сумму операции для вывода."""
    currency = _get_currency_code(operation)
    amount = _get_amount(operation)
    if currency == "RUB":
        return f"Сумма: {amount} руб."
    return f"Сумма: {amount} {currency}"


def _print_operation(operation: dict[str, Any]) -> None:
    """Выводит одну операцию в консоль."""
    date = get_date(operation.get("date", ""))
    description = operation.get("description", "")
    print(f"{date} {description}")

    from_account = str(operation.get("from", "") or "")
    to_account = str(operation.get("to", "") or "")
    if from_account and from_account.lower() != "nan":
        print(f"{mask_account_card(from_account)} -> {mask_account_card(to_account)}")
    else:
        print(mask_account_card(to_account))

    print(_format_amount(operation))
    print()


def _ask_status() -> str:
    """Запрашивает у пользователя статус операции."""
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию.\n"
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        ).strip().upper()

        if status in VALID_STATUSES:
            return status

        print(f'Статус операции "{status}" недоступен.')


def _load_transactions(choice: str) -> list[dict[str, Any]]:
    """Загружает транзакции из выбранного источника."""
    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        return load_operations(JSON_PATH)
    if choice == "2":
        print("Для обработки выбран CSV-файл.")
        return read_csv_transactions(CSV_PATH)
    print("Для обработки выбран XLSX-файл.")
    return read_excel_transactions(XLSX_PATH)


def main() -> None:
    """Основная логика программы работы с банковскими транзакциями."""
    print(
        "Привет! Добро пожаловать в программу работы "
        "с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )

    choice = input().strip()
    transactions = _load_transactions(choice)

    status = _ask_status()
    print(f'Операции отфильтрованы по статусу "{status}"')
    filtered = filter_by_state(transactions, status)

    if _is_yes(input("Отсортировать операции по дате? Да/Нет\n")):
        order = input("Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        reverse = order.startswith("по убыванию")
        filtered = sort_by_date(filtered, reverse=reverse)

    if _is_yes(input("Выводить только рублевые транзакции? Да/Нет\n")):
        filtered = list(filter_by_currency(filtered, "RUB"))

    if _is_yes(input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n")):
        search_word = input("Введите слово для поиска:\n")
        filtered = process_bank_search(filtered, search_word)

    print("Распечатываю итоговый список транзакций...")
    print()

    if not filtered:
        print(
            "Не найдено ни одной транзакции, подходящей под ваши "
            "условия фильтрации"
        )
        return

    print(f"Всего банковских операций в выборке: {len(filtered)}\n")
    for operation in filtered:
        _print_operation(operation)


if __name__ == "__main__":
    main()
