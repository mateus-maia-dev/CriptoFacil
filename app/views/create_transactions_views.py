from app.models.accounting_model import Accounting
from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
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
    return "", 201


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
        return "Essa Transação não existe", HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(data_to_update, key, value)

    data_to_update.net_quantity = data["quantity"]
    session.add(data_to_update)
    session.commit()

    date_dollar = str(data_to_update.date)
    get_ptax = get_data(date_dollar)
    ptax = float(get_ptax['sell_rate'])

    fiat = data_to_update.fiat
    price_per_coin = data_to_update.price_per_coin

    price_usd = price_per_coin if fiat == 'usd' else price_per_coin / ptax
    price_brl = price_per_coin if fiat == 'brl' else price_per_coin * ptax

    transactions: Transaction = (
        Transaction.query.filter_by(coin=data["coin"], user_id=user_id)
        .order_by(Transaction.date.asc(), Transaction.id.asc())
        .all()
    )

    for item in transactions:
        if item.id >= data_to_update.id:
            if data["type"] == 'buy' or data["type"] == 'output':
                net_quantity = data_to_update.net_quantity
                avg_price_brl = data_to_update.avg_price_brl
                avg_price_usd = data_to_update.avg_price_usd

                item.net_quantity += data_to_update.quantity

                avg_price_brl = (
                    price_brl * data_to_update.quantity
                    + avg_price_brl * (net_quantity - data_to_update.quantity)
                ) / item.net_quantity
                avg_price_usd = (
                    price_usd * data_to_update.quantity
                    + avg_price_usd * (item.net_quantity - data_to_update.quantity)
                ) / item.net_quantity

                item.avg_price_brl = avg_price_brl
                item.avg_price_usd = avg_price_usd

            if data["type"] == 'sell' or data["type"] == 'input':
                # item.net_quantity = data_to_update.net_quantity
                # item.avg_price_brl = data_to_update.avg_price_brl
                # item.avg_price_usd = data_to_update.avg_price_usd
                item.net_quantity -= data_to_update.quantity

            session.add(item)
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
