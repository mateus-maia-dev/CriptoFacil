from flask import Blueprint, request, current_app
from app.models.user_model import User
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from app.services.user_service import create, login
from app.services.helper import (
    verify_received_keys_from_create_user,
    verify_received_keys_from_login,
)


user = Blueprint("user", __name__, url_prefix="/api")


@user.route("/register", methods=["POST"])
def create_user():
    body = request.get_json()
    session = current_app.db.session

    try:
        verify_received_keys_from_create_user(body)
        return create(body, session), HTTPStatus.CREATED
    except KeyError as e:
        return e.args[0]


@user.route("/login", methods=["POST"])
def login_user():
    body = request.get_json()

    try:
        verify_received_keys_from_login(body)
        return login, HTTPStatus.OK
    except KeyError as e:
        return e.args[0]
