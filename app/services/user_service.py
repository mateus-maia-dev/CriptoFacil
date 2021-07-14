from app.models.user_model import User
from app.models.user_model import User
from flask_restful import reqparse
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.services.helper import init_app, get_user
from ipdb import set_trace
import jwt


def register() -> dict:
    parser = reqparse.RequestParser()

    parser.add_argument("name", type=str, required=True)
    parser.add_argument("last_name", type=str, required=True)
    parser.add_argument("email", type=str, required=True)
    parser.add_argument("password", type=str, required=True)

    new_user: User = User(**parser.parse_args())

    init_app(new_user)

    return {
        "name": new_user.name,
        "last_name": new_user.last_name,
        "email": new_user.email,
    }


def login():
    parser = reqparse.RequestParser()
    # username = request.json.get("email", None)
    # password = request.json.get("password", None)

    parser.add_argument("email", type=str, required=True)
    parser.add_argument("password", type=str, required=True)

    username = parser.parse_args()['email']
    password = parser.parse_args()['password']

    user = User.query.filter_by(email=username).first()
    if User.verify_password(user, password):
        access_token = create_access_token(identity=username)
        print(access_token)

        # get_user(access_token)
        # TODO PRECISO SALVAR ESSE TOKEN EM ALGUM LUGAR PARA CHAMA-LO NO REGISTRO DE TRANSAÇÃO\
        # e decodifica-lo para o user
        # set_trace()

        return jsonify(access_token=access_token)

    return jsonify({"msg": "Bad username or password"}), 401
