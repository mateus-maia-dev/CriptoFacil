from flask import Blueprint, jsonify
from app.services.coingecko_service import get_price
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transactions_model import Transaction
from app.services.transactions_service import get_transations
from http import HTTPStatus

portfolio = Blueprint("portfolio", __name__, url_prefix="/api")

@portfolio.route("/portfolio/list", methods=["GET"])
@jwt_required()
def list_portfolio():
    user_id = get_jwt_identity()

    data_coingecko = get_price()

    transaction_user = Transaction.query.filter_by(user_id=user_id).all()
    fix_transactions = get_transations(transaction_user)
    user_coins = list(fix_transactions.keys())

    list_coin_data_user = list()

    for _, name in enumerate(data_coingecko):
        for coin in user_coins:
            if name.lower() == coin:
                data_final = data_coingecko[name]
                data_final["coin"] = name.lower()
                data_final["avg_price_brl"] = fix_transactions[coin][-1]["avg_price_brl"]
                data_final["net_quantity"] = fix_transactions[coin][-1]["net_quantity"]
                list_coin_data_user.append(data_final)

    return jsonify([{
            "coin": data["coin"],
            "avg_price": round(data["avg_price_brl"], 2),
            "quantity": round(data["net_quantity"], 4),
            "current_price": round(data["brl"], 2),
            "24h_change": round(data["brl_24h_change"], 2),
            "current_position": round(data["brl"] * data["net_quantity"], 2),
            "profit": round((data["brl"] - data["avg_price_brl"]) * data["net_quantity"], 2),
        } for data in list_coin_data_user]), HTTPStatus.OK
