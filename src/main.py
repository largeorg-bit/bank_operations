import json
import os

from src.utils import load_transactions_dataframe
from src.views import events_page_info, main_page_info

DATA_PATH = "data/operations.xlsx"


def main() -> None:
    """Демонстрация работы модулей курсового проекта."""
    os.makedirs("reports", exist_ok=True)
    transactions = load_transactions_dataframe(DATA_PATH)

    date_string = "2021-12-20 15:30:00"
    main_data = main_page_info(date_string, transactions)
    events_data = events_page_info(date_string, transactions)

    print("=== Главная страница ===")
    print(json.dumps(main_data, ensure_ascii=False, indent=2))
    print("\n=== Страница событий ===")
    print(json.dumps(events_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
