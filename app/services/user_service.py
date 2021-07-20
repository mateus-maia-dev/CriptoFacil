from app.models.user_model import User
from flask_jwt_extended import create_access_token
from datetime import timedelta
from http import HTTPStatus


def create(body: dict, session):

    name = body.get("name")
    last_name = body.get("last_name")
    email = body.get("email")
    password = body.get("password")

    new_user = User(name=name, last_name=last_name, email=email)
    new_user.password = password

    session.add(new_user)
    session.commit()

    access_token = create_access_token(
        identity=new_user.id, expires_delta=timedelta(days=7)
    )

    return {"token": access_token}


def login(body: dict):
    email = body.get("email")
    password = body.get("password")

    user_data = User.query.filter_by(email=email).first()

    if not user_data or not user_data.verify_password(password):
        return {"message": "User not found"}, HTTPStatus.NOT_FOUND

    access_token = create_access_token(
        identity=user_data.id, expires_delta=timedelta(days=7)
    )

    return {"token": access_token}
