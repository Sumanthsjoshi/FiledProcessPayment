from flask import request
from flask_restful import Resource


class ServerShutdown(Resource):

    def get(self):
        func = request.environ.get("werkzeug.server.shutdown")
        func()
        return {"message": "Shutting down server..."}
