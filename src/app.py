from flask import Flask
from flask_restful import Api
from src.resources.process_payment import ProcessPayment
from src.resources.server_shutdown import ServerShutdown

app = Flask(__name__)
api = Api(app)

api.add_resource(ProcessPayment, "/processpayment/<string:credit_card_number>")
api.add_resource(ServerShutdown, "/shutdown")


if __name__ == "__main__":
    app.run(debug=True)
