from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transactions_model import Transaction


from http import HTTPStatus
from app.services.helper import (
    verify_received_keys_from_create_transactions,
    validated_values_for_register_transaction,
)
from app.services.transactions_service import create


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


@transactions.route("/transactions/<int:transaction_id>", methods=["PUT"])
@jwt_required()
def update_transaction(transaction_id):
    user_id = get_jwt_identity()
    session = current_app.db.session
    data = request.get_json()

    data_to_update: Transaction = Transaction.query.filter_by(
        user_id=user_id, id=transaction_id
    ).first()

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

    session.delete(data_to_delete)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
