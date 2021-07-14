from flask_restful import Resource
from app.services.transaction_service import create_transaction
from flask_jwt_extended import jwt_required


class TransactionResource(Resource):
    # @jwt_required()
    def post(self):
        try:
            return create_transaction()
        except:
            ...
