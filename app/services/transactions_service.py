from app.models.transactions_model import Transaction
from app.services import get_data
from flask import current_app

from app.services.current_dollar_value import get_data
import ipdb


def create(body: dict, user_id: int):
    session = current_app.db.session

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
        .order_by(Transaction.date.asc())
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
                price_brl * quantity + avg_price_brl * (net_quantity - quantity)
            ) / net_quantity
            avg_price_usd = (
                price_usd * quantity + avg_price_usd * (net_quantity - quantity)
            ) / net_quantity

        if type == 'sell' or type == 'input':
            net_quantity = transactions[-1].net_quantity
            avg_price_brl = transactions[-1].avg_price_brl
            avg_price_usd = transactions[-1].avg_price_usd

            if net_quantity < quantity:
                raise Exception({"error": "insufficients funds."})
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

    return new_transaction.serialized()


def get_transations(transactions):
    transactions_per_coin = dict()

    coins_list = [coin.coin for coin in transactions]
    coins_set = set(coins_list)
    user_coins = list(coins_set)

    for coin in user_coins:
        coin_transactions = [
            transaction for transaction in transactions if transaction.coin == coin
        ]

        transactions_per_coin[coin] = list()

        net_quantity = 0
        avg_price_brl = 0
        avg_price_usd = 0

        for item in coin_transactions:
            get_ptax = str(item.date)
            get_ptax_str = get_data(get_ptax)
            ptax = float(get_ptax_str['sell_rate'])

            price_usd = (
                item.price_per_coin
                if item.fiat == 'usd'
                else item.price_per_coin / ptax
            )
            price_brl = (
                item.price_per_coin
                if item.fiat == 'brl'
                else item.price_per_coin * ptax
            )

            if item.type == 'buy' or item.type == 'output':
                net_quantity += item.quantity

                avg_price_brl = (
                    price_brl * item.quantity
                    + avg_price_brl * (net_quantity - item.quantity)
                ) / net_quantity
                avg_price_usd = (
                    price_usd * item.quantity
                    + avg_price_usd * (net_quantity - item.quantity)
                ) / net_quantity

            if item.type == 'sell' or item.type == 'input':
                avg_price_brl = result["avg_price_brl"]
                avg_price_usd = result["avg_price_usd"]
                net_quantity = result["net_quantity"] - item.quantity

            result = {
                "id": item.id,
                "date": item.date,
                "type": item.type,
                "coin": item.coin,
                "fiat": item.fiat,
                "price_per_coin": round(item.price_per_coin, 2),
                "quantity": item.quantity,
                "net_quantity": net_quantity,
                "avg_price_brl": round(avg_price_brl, 2),
                "avg_price_usd": round(avg_price_usd, 2),
                "foreign_exch": item.foreign_exch,
                "ptax": ptax,
            }

            transactions_per_coin[coin].append(result)

    return transactions_per_coin
