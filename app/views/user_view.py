from flask_restful import Resource
from app.services.user_service import register, login
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError


class UserResourse(Resource):
    def post(self):
        try:
            register(), HTTPStatus.CREATED
        except IntegrityError as _:
            return {"error": "pessoa já existe"}, HTTPStatus.UNPROCESSABLE_ENTITY


class UserLoginResource(Resource):
    def post(self):

        try:
            login(), HTTPStatus.OK
        except:
            ...


# class UserIdResource(Resource):
#     def get(self, pessoa_id: int):
#         return pegar_pessoa(pessoa_id), HTTPStatus.OK
