# FiledProcessPayment
A Flask Web API for payment processing

## Clone the repository
* ```$ git clone https://github.com/Sumanthsjoshi/FiledProcessPayment.git```

## Run the app
* ```$ cd src```
* ```$ python app.py```

## Using the app
* Login to the Postman tool or web interface
* Alternatively you can access the respective Postman collection with this link `https://www.getpostman.com/collections/ab48ae2927eb0b1062bb`
* Send request with the end-point - http://127.0.0.1:5000/processpayment/<string:credit_card_number>
* Send proper request data in json format as below:
  ```
  {
    "card_holder": <name>,
    "expiration_date": <expiration-date>,
    "security_code": <code>,
    "amount": <amount>
  }
  ```
* For initial testing only below Credit Card data is used by the application
  ```
  CreditCard("123456789012", "Sumanth", datetime.today() + dt.timedelta(days=30), "221", 1000),
  CreditCard("3456 7890 1234", "Rakesh", datetime.today(), "345", 2000),
  CreditCard("5678 90123456", "Tanmay", datetime(2021, 1, 1), "202", 5000)
  ```
* Access the unittests written in ./tests/test_process_payment_resource.py
