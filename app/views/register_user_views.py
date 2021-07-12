from flask import Blueprint, request, current_app
from app.models.user_model import User
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from datetime import timedelta

user = Blueprint("user", __name__, url_prefix="/api")

@user.route("/register", methods=["POST"])
def create_user():
    body = request.get_json()
    session = current_app.db.session

    name = body.get("name")
    last_name = body.get("last_name")
    email = body.get("email")
    password = body.get("password")

    new_user = User(name=name, last_name=last_name, email=email)
    new_user.password = password

    session.add(new_user)
    session.commit()

    access_token = create_access_token(identity=new_user.id, expires_delta=timedelta(days=7))

    return {
        "token": access_token
    }, HTTPStatus.CREATED

@user.route("/login", methods=["POST"])
def login_user():
    body = request.get_json()

    email = body.get("email")
    password = body.get("password")

    user_data = User.query.filter_by(email=email).first()

    if not user_data or not user_data.verify_password(password):
        return { "message": "User not found" }, HTTPStatus.NOT_FOUND

    access_token = create_access_token(identity=user_data.id, expires_delta=timedelta(days=7))

    return {
        "token": access_token
    }, HTTPStatus.OK
