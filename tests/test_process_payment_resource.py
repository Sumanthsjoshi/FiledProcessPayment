import subprocess
import unittest
import datetime as dt
from datetime import datetime

import requests


class TestProcessPaymentResource(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cmd = "python ../src/app.py"
        subprocess.Popen(cmd, shell=True)
        cls.sumanth_exp_date = str(datetime.today().date() +
                                   dt.timedelta(days=30))

    @classmethod
    def tearDownClass(cls) -> None:
        requests.get("http://127.0.0.1:5000/shutdown")

    def test_put_parse_args(self):
        data = {
            "card_holder": "Sumanth",
            "expiration_date": self.sumanth_exp_date,
            "security_code": "221"  # Missing amount argument
        }
        resp = requests.put(
            "http://127.0.0.1:5000/processpayment/123456789012",
            data
        )
        self.assertTrue(resp.json().get("message").get("amount"))
        self.assertEqual(400, resp.status_code)

    def test_put_validate_security_code_noteq_three_digits(self):
        data = {
            "card_holder": "Sumanth",
            "expiration_date": self.sumanth_exp_date,
            "security_code": "22",  # Not three digit
            "amount": 12.67
        }
        resp = requests.put(
            "http://127.0.0.1:5000/processpayment/123456789012",
            data
        )
        self.assertEqual("Invalid transaction details",
                         resp.json().get("message"))
        self.assertEqual(400, resp.status_code)

    def test_put_validate_non_positive_amount(self):
        data = {
            "card_holder": "Sumanth",
            "expiration_date": self.sumanth_exp_date,
            "security_code": "221",
            "amount": -12.67  # Non positive amount
        }
        resp = requests.put(
            "http://127.0.0.1:5000/processpayment/123456789012",
            data
        )
        self.assertEqual("Invalid transaction details",
                         resp.json().get("message"))
        self.assertEqual(400, resp.status_code)

    def test_put_credit_card_not_found(self):
        data = {
            "card_holder": "Sumanth",
            "expiration_date": self.sumanth_exp_date,
            "security_code": "221",
            "amount": 12.67
        }
        # Invalid credit card number
        resp = requests.put(
            "http://127.0.0.1:5000/processpayment/999999999999",
            data
        )
        self.assertEqual("Credit card not found", resp.json().get("message"))
        self.assertEqual(404, resp.status_code)

    def test_put_expired_credit_card(self):
        data = {
            "card_holder": "Tanmay",
            "expiration_date": "2021-01-01",  # Expired credit card
            "security_code": "202",
            "amount": 12.67
        }
        # Invalid credit card number
        resp = requests.put(
            "http://127.0.0.1:5000/processpayment/567890123456",
            data
        )
        self.assertEqual(f"Credit card expired on {datetime(2021, 1, 1)}",
                         resp.json().get("message"))
        self.assertEqual(400, resp.status_code)

    def test_put_insufficient_funds(self):
        data = {
            "card_holder": "Rakesh",
            "expiration_date": str(datetime.today().date()),
            "security_code": "345",
            "amount": 22122.0  # Amount > balance
        }
        resp = requests.put(
            "http://127.0.0.1:5000/processpayment/345678901234",
            data
        )
        self.assertEqual(f"Insufficient balance for the given amount "
                         f"{data['amount']}",
                         resp.json().get("message"))
        self.assertEqual(400, resp.status_code)

    def test_put_process_payment(self):
        data = {
            "card_holder": "Sumanth",
            "expiration_date": self.sumanth_exp_date,
            "security_code": "221",
            "amount": 12.67
        }
        resp = requests.put(
            "http://127.0.0.1:5000/processpayment/123456789012",
            data
        )
        self.assertEqual(200, resp.status_code)


if __name__ == "__main__":
    unittest.main()
