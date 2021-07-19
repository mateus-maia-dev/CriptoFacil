from flask import Blueprint, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.transactions_model import Transaction
from app.models.coins_historical_quotes_model import CoinsHistorical
from http import HTTPStatus
from sqlalchemy import extract

graphic = Blueprint("graphic", __name__, url_prefix="/api")

@graphic.route("/graphic", methods=["GET"])
@jwt_required()
def data_graphic():
    user_id = get_jwt_identity()
    session = current_app.db.session
    date_month = [{"month": "janeiro", "num_month": 1}, {"month": "fevereiro", "num_month": 2}, {"month": "marco", "num_month": 3}, {"month": "abril", "num_month": 4}, {"month": "maio", "num_month": 5}, {"month": "junho", "num_month": 6}, {"month": "julho", "num_month": 7}, {"month": "agosto", "num_month": 8}, {"month": "setembro", "num_month": 9}, {"month": "outubro", "num_month": 10}, {"month": "novembro", "num_month": 11}, {"month": "dezembro", "num_month": 12}]
    next_end_coin = {"janeiro": [], "fevereiro": [], "marco": [], "abril": [], "maio": [], "junho": [], "julho": [], "agosto": [], "setembro": [], "outubro": [], "novembro": [], "dezembro": []}
    price_end_coin = {"janeiro": [], "fevereiro": [], "marco": [], "abril": [], "maio": [], "junho": [], "julho": [], "agosto": [], "setembro": [], "outubro": [], "novembro": [], "dezembro": []}
    data_end = {"janeiro": {}, "fevereiro": {}, "marco": {}, "abril": {}, "maio": {}, "junho": {}, "julho": {}, "agosto": {}, "setembro": {}, "outubro": {}, "novembro": {}, "dezembro": {}}
    next_price_end_coin = {"janeiro": {}, "fevereiro": {}, "marco": {}, "abril": {}, "maio": {}, "junho": {}, "julho": {}, "agosto": {}, "setembro": {}, "outubro": {}, "novembro": {}, "dezembro": {}}

    transaction_user = Transaction.query.filter_by(user_id=user_id).all()
    list_dict_transaction_user = [object_transaction.coin.lower() for object_transaction in transaction_user]

    list_name_coin = list(set(list_dict_transaction_user))
    list_data_coin_end = list()

    for name_coin in list_name_coin:
        for month in date_month:
            list_month_coin = session.query(Transaction).filter_by(user_id=user_id, coin=name_coin).filter(extract('month', Transaction.date)==month["num_month"]).all()
            list_data_coin_end.append({month["month"]: list_month_coin[-1] if len(list_month_coin) > 0 else list_month_coin})

    for month in next_end_coin.keys():
        for obj in list_data_coin_end:
            if obj.get(month):
                next_end_coin.get(month).append(obj.get(month))

    dict_next_end_coin = dict()

    for month in next_end_coin.keys():
        if len(next_end_coin.get(month)) > 0:
            dict_next_end_coin[month] = [{dt.coin: dt.net_quantity} for dt in next_end_coin.get(month)]      

############################

    list_price_coin = list()

    for name_coin in list_name_coin:
        for month in date_month:
            list_month_price = session.query(CoinsHistorical).filter_by(coin=name_coin).filter(extract('month', CoinsHistorical.date)==month["num_month"]).all()
            list_price_coin.append({month["month"]: list_month_price[-1] if len(list_month_price) > 0 else list_month_price})

    for month in price_end_coin.keys():
        for obj in list_price_coin:
            if obj.get(month):
                price_end_coin.get(month).append(obj.get(month))

    dict_price_end_coin = dict()
    
    for month in price_end_coin.keys():
        if len(price_end_coin.get(month)) > 0:
            dict_price_end_coin[month] = [{f'{dt.coin}_price': dt.price} for dt in price_end_coin.get(month)]   

    list_data = list()

    for month in next_end_coin.keys():
        if len(next_end_coin.get(month)) > 0:
            list_data.append({month: [*dict_next_end_coin.get(month), *dict_price_end_coin.get(month)]})


    for month in next_end_coin.keys():
        if len(next_end_coin.get(month)) > 0:
            for obj in list_data:
                if obj.get(month):
                    for item_obj in obj.get(month):
                        next_price_end_coin.get(month).update({**next_price_end_coin.get(month), **item_obj})
    
    ##############
    
    for name_coin in list_name_coin:
        for month in next_end_coin.keys():
            if len(next_end_coin.get(month)) > 0:
                if next_price_end_coin.get(month).get(name_coin) and next_price_end_coin.get(month).get(f"{name_coin}_price"):
                    data_end.get(month).update({**data_end.get(month), **{name_coin: next_price_end_coin.get(month).get(name_coin) * next_price_end_coin.get(month).get(f"{name_coin}_price")}})


    return {k: v for k,v in data_end.items() if len(v) > 0}, HTTPStatus.OK
