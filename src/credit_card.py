from datetime import datetime


class CreditCard:
    def __init__(self, credit_card_number, card_holder, expiration_date,
                 security_code, credit_limit):
        self.credit_card_number = credit_card_number.replace(" ", "")
        self.card_holder = card_holder
        self.expiration_date = expiration_date  # DateTime not in past
        self.security_code = security_code  # 3 digits
        self.credit_limit = credit_limit  # decimal positive value
        self.balance = self.credit_limit  # decimal positive value

    def pay(self, data):
        if not data["expiration_date"] >= datetime.today().date():
            return {"message": f"Credit card expired on {self.expiration_date}"}
        print(data["amount"], self.balance)
        if data["amount"] > self.balance:
            return {"message": f"Insufficient balance for the given amount "
                               f"{data['amount']}"}
        self.balance -= data["amount"]
