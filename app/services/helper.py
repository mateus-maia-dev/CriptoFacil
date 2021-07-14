from flask import Flask, current_app
import jwt
from ipdb import set_trace


def init_app(model) -> None:
    current_app.db.session.add(model)
    current_app.db.session.commit()


def get_user(token):

    decoded = jwt.decode(token, "super secret key", algorithms=["HS256"])

    return decoded['sub']
