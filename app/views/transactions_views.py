from app.models.accounting_model import Accounting
from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.transactions_service import get_transations
from app.models.transactions_model import Transaction


from http import HTTPStatus
from app.services.helper import (
    verify_received_keys_from_create_transactions,
    validated_values_for_register_transaction,
)
from app.services.transactions_service import create, get_transations
import ipdb


transactions = Blueprint("transactions", __name__, url_prefix="/api")


@transactions.route("/transactions/register", methods=["POST"])
@jwt_required()
def create_transaction():

    body = request.get_json()
    user_id = get_jwt_identity()

    try:
        verify_received_keys_from_create_transactions(body)
        validated_values_for_register_transaction(body)

        return create(body, user_id), HTTPStatus.CREATED

    except KeyError as e:
        return e.args[0], HTTPStatus.BAD_REQUEST
    except Exception as e:
        return e.args[0], HTTPStatus.BAD_REQUEST


@transactions.route("/transactions", methods=["GET"])
@jwt_required()
def get_transaction():
    user_id = get_jwt_identity()

    transactions = (
        Transaction.query.filter_by(user_id=user_id)
        .order_by(Transaction.date.asc())
        .all()
    )

    transations_all = get_transations(transactions)

    return jsonify(transations_all), HTTPStatus.CREATED


@transactions.route("/transactions/<coin_transaction>", methods=["GET"])
@jwt_required()
def get_transaction_by_coin(coin_transaction):
    user_id = get_jwt_identity()

    transactions = (
        Transaction.query.filter_by(user_id=user_id, coin=coin_transaction)
        .order_by(Transaction.date.asc())
        .all()
    )

    if transactions == []:
        return "Coin not found", HTTPStatus.NOT_FOUND

    transations_all = get_transations(transactions)

    return jsonify(transations_all), HTTPStatus.OK


@transactions.route("/transactions/<int:transaction_id>", methods=["PUT"])
@jwt_required()
def update_transaction(transaction_id):
    user_id = get_jwt_identity()
    session = current_app.db.session
    data = request.get_json()

    data_to_update: Transaction = Transaction.query.filter_by(
        user_id=user_id, id=transaction_id
    ).first()

    if data_to_update == None:
        return "Transaction not found", HTTPStatus.BAD_REQUEST

    for key, value in data.items():
        setattr(data_to_update, key, value)

    session.add(data_to_update)
    session.commit()

    return data_to_update.serialized(), HTTPStatus.OK


@transactions.route("/transactions/<int:transaction_id>", methods=["DELETE"])
@jwt_required()
def delete_transaction(transaction_id):
    user_id = get_jwt_identity()
    session = current_app.db.session

    data_to_delete: Transaction = Transaction.query.filter_by(
        user_id=user_id, id=transaction_id
    ).first()

    if data_to_delete == None:
        return "Transaction not found", HTTPStatus.BAD_REQUEST

    session.delete(data_to_delete)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
