from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transactions_model import Transaction
from app.services.transactions_service import get_transations
from app.services.charts_service import quantity_per_month, get_historical_price, get_positions, total_positions
from http import HTTPStatus


charts = Blueprint("charts", __name__, url_prefix="/api")


@charts.route("/chart", methods=["GET"])
@jwt_required()
def data_graphic():
    user_id = get_jwt_identity()

    transactions = (
        Transaction.query.filter_by(user_id=user_id)
        .order_by(Transaction.date.asc())
        .all()
    )

    transactions_list = get_transations(transactions)

    quantity = quantity_per_month(transactions_list)

    historical_price = get_historical_price(transactions_list)

    result_per_coin = get_positions(
        transactions_list, quantity, historical_price)

    total_balance = total_positions(transactions_list, result_per_coin)

    return total_balance, HTTPStatus.OK
