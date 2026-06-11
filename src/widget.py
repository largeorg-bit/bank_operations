from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account: str) -> str:
    """Возвращает строку с замаскированным номером карты и счета"""
    name_of_card_or_check = ""
    digits_of_card_or_check = ""
    for i in range(len(card_or_account)):
        if card_or_account[i].isdigit():
            name_of_card_or_check = card_or_account[:i]
            digits_of_card_or_check = card_or_account[i:]
            break

    if "счет " in name_of_card_or_check.lower() and len(digits_of_card_or_check) == 20:
        return f"{name_of_card_or_check}{get_mask_account(int(digits_of_card_or_check))}"

    elif (
            "maestro " in name_of_card_or_check.lower()
            or "mastercard " in name_of_card_or_check.lower()
            or "visa " in name_of_card_or_check.lower()
            and len(digits_of_card_or_check) == 16
    ):
        return f"{name_of_card_or_check}{get_mask_card_number(int(digits_of_card_or_check))}"

    else:
        return "Неправильно введен номер счёта"


def get_date(date_and_time: str) -> str:
    """ "возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")"""

    if date_and_time[:4].isdigit():
        return f"{date_and_time[8:10]}.{date_and_time[5:7]}.{date_and_time[:4]}"
    return "Неправильно введена дата"
