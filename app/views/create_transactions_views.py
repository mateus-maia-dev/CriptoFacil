from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transactions_model import Transaction
from http import HTTPStatus

transactions = Blueprint("transactions", __name__, url_prefix="/api")

@transactions.route("/transactions/register", methods=["POST"])
@jwt_required()
def create_user():
    body = request.get_json()
    session = current_app.db.session
    user_id = get_jwt_identity()

    print(body, user_id)

    date = body.get("date")
    type = body.get("type")
    coin = body.get("coin")
    fiat = body.get("fiat")
    price_per_coin = body.get("price_per_coin")
    avg_price_brl = body.get("avg_price_brl")
    avg_price_usd = body.get("avg_price_usd")
    net_quantity = body.get("net_quantity")
    quantity = body.get("quantity")
    foreign_exch = body.get("foreign_exch")

    new_transaction = Transaction(date=date, type=type, coin=coin, fiat=fiat, price_per_coin=price_per_coin, avg_price_brl=avg_price_brl, avg_price_usd=avg_price_usd, net_quantity=net_quantity, quantity=quantity, foreign_exch=foreign_exch, user_id=user_id)

    session.add(new_transaction)
    session.commit()

    return new_transaction.serialized(), HTTPStatus.CREATED
