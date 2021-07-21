from os import set_inheritable
from flask import Blueprint, current_app
from flask.json import jsonify
from app.models.transactions_model import Transaction

from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.accounting_service import create_accounting
from app.services.transactions_service import get_transations
from http import HTTPStatus

from ipdb import set_trace

accounting = Blueprint('accounting', __name__, url_prefix="/api")


@accounting.route('/accounting')
@jwt_required()
def retrieve_accounting():
    try:
        user_id = get_jwt_identity()

        transactions = (
            Transaction.query.filter_by(user_id=user_id)
            .order_by(Transaction.date.asc())
            .all()
        )

        transaction = get_transations(transactions)
        accounting = create_accounting(transaction)

        return accounting, HTTPStatus.OK
    except:
        ...
