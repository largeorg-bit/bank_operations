from src.masks import get_mask_account, get_mask_card_number
from src.widget import mask_account_card, get_date
if __name__ == "__main__":
    card_number = int(input("Введите номер карты"))
    account = int(input("Введите номер карты"))

    print(get_mask_card_number(card_number))
    print(get_mask_account(account))

    print( mask_account_card("Visa Platinum 7000792289606361"))
    print(get_date("2024-03-11T02:26:18.671407"))
#  изменения