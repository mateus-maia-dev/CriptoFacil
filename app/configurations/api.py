from flask import Flask
from flask_restful import Api


def init_app(app: Flask):
    api = Api(app)

    from app.views.transaction_view import TransactionResource
    from app.views.user_view import UserResourse
    from app.views.user_view import UserLoginResource

    api.add_resource(TransactionResource, '/transaction', endpoint='/post')
    api.add_resource(UserResourse, '/user', endpoint='/register')
    api.add_resource(UserLoginResource, '/auth', endpoint='/login')
