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

    print(data_coingecko)

    for _, name in enumerate(data_coingecko):
        if name.lower() in user_coins:
            data_final = data_coingecko[name]
            data_final["coin"] = name.lower()
            #data_final["avg_price_brl"] = [data.avg_price_brl for data in list_data_coin_end if data.coin == name.lower()]
            #data_final["net_quantity"] = [data.net_quantity for data in list_data_coin_end if data.coin == name.lower()]
            list_coin_data_user.append(data_final)

    # print(data_final)
    # print(list_coin_data_user)
    return "", HTTPStatus.OK


# return jsonify([{
#         "coin": data["coin"],
#         "avg_price": data["avg_price_brl"],
#         "quantity": data["net_quantity"],
#         "current_price": data["brl"],
#         "24h_change": data["brl_24h_change"],
#         "current_position": data["brl"] * data["net_quantity"],
#         "profit": (data["brl"] - data["avg_price_brl"]) * data["net_quantity"],
#     } for data in list_coin_data_user]), HTTPStatus.OK