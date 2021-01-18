from datetime import datetime

from flask import Flask
from flask_restful import Api, Resource, reqparse
from src.credit_card import CreditCard

app = Flask(__name__)
api = Api(app)

credit_cards = [
    CreditCard("123456789012", "Sumanth", datetime(2021, 12, 31), "221", 1000),
    CreditCard("3456 7890 1234", "Rakesh", datetime(2024, 12, 31), "345", 2000),
    CreditCard("5678 9012 3456", "Tanmay", datetime(2021, 1, 1), "202", 5000)
]


class ProcessPayment(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("card_holder", type=str, required=True,
                        help="A valid credit card holder name")
    parser.add_argument("expiration_date", type=str, required=True,
                        help="An expiration date of the credit card")
    parser.add_argument("security_code", type=str, required=False,
                        help="A valid security code for payment processing")
    parser.add_argument("amount", type=float, required=True,
                        help="A positive amount")

    @classmethod
    def _validate(cls, data):
        if not all([
            len(data.get("security_code", "   ")) == 3,
            data["amount"] > 0
        ]):
            return {"message": "Invalid transaction details"}

    def get(self):
        pass

    def put(self, credit_card_number):
        data = ProcessPayment.parser.parse_args()
        data["expiration_date"] = datetime.strptime(data["expiration_date"],
                                                    "%Y-%m-%d")
        result = ProcessPayment._validate(data)
        if result:
            return result, 400

        credit_card = next(filter(
            lambda x: x.credit_card_number ==
            credit_card_number.replace(" ", ""),
            credit_cards
        ))
        if credit_card:
            result = credit_card.pay(data)
            if result:
                return result, 400

            return {"message": "The payment is processed successfully.\n"
                               f"Available balance{credit_card.balance}"}, 200

        return {"message": "Credit card not found"}, 404


api.add_resource(ProcessPayment, "/processpayment/<string:credit_card_number>")


if __name__ == "__main__":
    app.run(debug=True)
