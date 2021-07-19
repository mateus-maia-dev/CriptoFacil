from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transactions_model import Transaction
from app.services import populate_accounting, get_data
from http import HTTPStatus


transactions = Blueprint("transactions", __name__, url_prefix="/api")


@transactions.route("/transactions/register", methods=["POST"])
@jwt_required()
def create_transaction():
    session = current_app.db.session
    body = request.get_json()
    user_id = get_jwt_identity()

    date = body.get("date")
    type = body.get("type")
    coin = body.get("coin")
    fiat = body.get("fiat")
    price_per_coin = body.get("price_per_coin")
    quantity = body.get("quantity")
    foreign_exch = body.get("foreign_exch")

    get_ptax = get_data(date)
    ptax = float(get_ptax['sell_rate'])

    price_usd = price_per_coin if fiat == 'usd' else price_per_coin / ptax
    price_brl = price_per_coin if fiat == 'brl' else price_per_coin * ptax

    transactions = (
        Transaction.query.filter_by(coin=body["coin"], user_id=user_id)
        .order_by(Transaction.date.asc(), Transaction.id.asc())
        .all()
    )

    if not transactions:
        avg_price_brl = price_brl
        avg_price_usd = price_usd
        net_quantity = quantity

    for _ in transactions:

        if type == 'buy' or type == 'output':

            net_quantity = transactions[-1].net_quantity
            avg_price_brl = transactions[-1].avg_price_brl
            avg_price_usd = transactions[-1].avg_price_usd

            net_quantity += quantity

            avg_price_brl = (
                price_brl * quantity + avg_price_brl *
                (net_quantity - quantity)
            ) / net_quantity
            avg_price_usd = (
                price_usd * quantity + avg_price_usd *
                (net_quantity - quantity)
            ) / net_quantity

        if type == 'sell' or type == 'input':
            net_quantity = transactions[-1].net_quantity
            avg_price_brl = transactions[-1].avg_price_brl
            avg_price_usd = transactions[-1].avg_price_usd

            net_quantity -= quantity

    new_transaction = Transaction(
        date=date,
        type=type,
        coin=coin,
        fiat=fiat,
        price_per_coin=price_per_coin,
        avg_price_brl=avg_price_brl,
        avg_price_usd=avg_price_usd,
        net_quantity=net_quantity,
        quantity=quantity,
        foreign_exch=foreign_exch,
        user_id=user_id,
    )

    session.add(new_transaction)
    session.commit()

    populate_accounting(user_id, ptax)

    return new_transaction.serialized(), HTTPStatus.CREATED


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

    date_dollar = str(data_to_update.date)
    get_ptax = get_data(date_dollar)
    ptax = float(get_ptax['sell_rate'])

    fiat = data_to_update.fiat
    price_per_coin = data_to_update.price_per_coin

    price_usd = price_per_coin if fiat == 'usd' else price_per_coin / ptax
    price_brl = price_per_coin if fiat == 'brl' else price_per_coin * ptax

    transactions: Transaction = (
        Transaction.query.filter_by(coin=data["coin"], user_id=user_id)
        .order_by(Transaction.date.asc())
        .all()
    )

    for item in transactions:
        if item.id != data_to_update.id:
            if item.type == 'buy' or item.type == 'output':
                net_quantity = data_to_update.net_quantity
                avg_price_brl = data_to_update.avg_price_brl
                avg_price_usd = data_to_update.avg_price_usd

                item.net_quantity += data_to_update.quantity

                avg_price_brl = (
                    price_brl * data_to_update.quantity + avg_price_brl *
                    (net_quantity - data_to_update.quantity)
                ) / item.net_quantity
                avg_price_usd = (
                    price_usd * data_to_update.quantity + avg_price_usd *
                    (item.net_quantity - data_to_update.quantity)
                ) / item.net_quantity

                item.avg_price_brl = avg_price_brl
                item.avg_price_usd = avg_price_usd
            
            if item.type == 'sell' or item.type == 'input':
                #item.net_quantity = data_to_update.net_quantity
                # item.avg_price_brl = data_to_update.avg_price_brl
                # item.avg_price_usd = data_to_update.avg_price_usd
                item.net_quantity -= data_to_update.quantity

            session.add(item)

    data_to_update.net_quantity = data["quantity"]

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

