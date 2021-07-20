from flask import Blueprint, current_app

from flask_jwt_extended import jwt_required
from app.services.accounting_service import get_accounting
from http import HTTPStatus


accounting = Blueprint('accounting', __name__, url_prefix='/api')


@accounting.route('/accounting')
@jwt_required()
def retrieve_accounting():
    try:
        return get_accounting(), HTTPStatus.OK
    except:
        ...
