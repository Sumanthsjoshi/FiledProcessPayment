from datetime import datetime

from flask_restful import Resource, reqparse
from data.credit_cards_data import credit_cards

credit_cards = credit_cards()


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
                                                    "%Y-%m-%d").date()
        result = ProcessPayment._validate(data)
        if result:
            return result, 400

        credit_card = next(filter(
            lambda x: x.credit_card_number ==
            credit_card_number.replace(" ", ""),
            credit_cards
        ), None)
        if credit_card:
            result = credit_card.pay(data)
            if result:
                return result, 400

            return {"message": f"The payment is processed successfully. "
                               f"Available balance: {credit_card.balance}"}, 200

        return {"message": "Credit card not found"}, 404
