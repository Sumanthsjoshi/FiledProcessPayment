import datetime as dt
from datetime import datetime

from src.credit_card import CreditCard


def credit_cards():
    cards = [
        CreditCard("123456789012", "Sumanth",
                   datetime.today() + dt.timedelta(days=30), "221", 1000),
        CreditCard("3456 7890 1234", "Rakesh", datetime.today(), "345", 2000),
        CreditCard("5678 90123456", "Tanmay", datetime(2021, 1, 1), "202", 5000)
    ]
    return cards
