import logging
import os

logger = logging.getLogger(__name__)

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "masks.log")

os.makedirs(LOG_DIR, exist_ok=True)

file_formatter = logging.Formatter(
    "%(asctime)s %(name)s %(levelname)s %(message)s"
)
file_handler = logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8")
file_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: int) -> str:
    """Функция принимает номер карты в виде числа и возвращает маску по правилу XXXX XX** **** XXXX"""
    try:
        card_number_str = str(card_number)
        mask = (
            f"{card_number_str[:4]} {card_number_str[4:6]}** **** "
            f"{card_number_str[-4:]}"
        )
        logger.info("Успешное маскирование номера карты")
        return mask
    except (TypeError, ValueError) as error:
        logger.error("Ошибка при маскировании номера карты: %s", error)
        raise


def get_mask_account(number_account: int) -> str:
    """Функция принимает номер счета и возвращает его маску по правилу **XXXX (последние 4 цифры)"""
    try:
        number_account_str = str(number_account)
        mask = f"**{number_account_str[-4:]}"
        logger.info("Успешное маскирование номера счета")
        return mask
    except (TypeError, ValueError) as error:
        logger.error("Ошибка при маскировании номера счета: %s", error)
        raise
