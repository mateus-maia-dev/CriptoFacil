from flask import Blueprint, jsonify
from app.services.coingecko_service import get_price
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transactions_model import Transaction
from http import HTTPStatus

portfolio = Blueprint("portfolio", __name__, url_prefix="/api")

@portfolio.route("/portfolio/list", methods=["GET"])
@jwt_required()
def list_portfolio():
    user_id = get_jwt_identity()

    data_coingecko = get_price()

    transaction_user = Transaction.query.filter_by(user_id=user_id).all()
    list_dict_transaction_user = [object_transaction.coin.lower() for object_transaction in transaction_user]

    list_data_coin_end = list()

    list_name_coin = list(set(list_dict_transaction_user))

    for name in list_name_coin:
        list_Transaction_coin = Transaction.query.filter_by(coin=name, user_id=user_id).all()
        list_data_coin_end.append(list_Transaction_coin[-1])

    list_coin_data_user = list()

    for _, name in enumerate(data_coingecko):
        if name.lower() in list_dict_transaction_user:
            data_final = data_coingecko[name]
            data_final["coin"] = name.lower()
            data_final["avg_price_brl"] = [data.avg_price_brl for data in list_data_coin_end if data.coin == name.lower()][0]
            data_final["net_quantity"] = [data.net_quantity for data in list_data_coin_end if data.coin == name.lower()][0]
            list_coin_data_user.append(data_final)

    return jsonify([{
        "coin": data["coin"],
        "avg_price": data["avg_price_brl"],
        "quantity": data["net_quantity"],
        "current_price": data["brl"],
        "24h_change": data["brl_24h_change"],
        "current_position": data["brl"] * data["net_quantity"],
        "profit": (data["brl"] - data["avg_price_brl"]) * data["net_quantity"],
    } for data in list_coin_data_user]), HTTPStatus.OK
