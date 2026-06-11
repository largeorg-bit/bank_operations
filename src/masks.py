def get_mask_card_number(card_number: int) -> str:
    """Функция принимает номер карты в виде числа и возвращает маску по правилу XXXX XX** **** XXXX"""
    card_number_str = str(card_number)

    return f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"


def get_mask_account(number_account: int) -> str:
    """Функция принимает номер счета и возвращает его маску по правилу **XXXX (последние 4 цифры)"""
    number_account_str = str(number_account)

    return f"**{number_account_str[-4:]}"

