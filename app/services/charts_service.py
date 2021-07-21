from app.models.coins_historical_quotes_model import CoinsHistorical
from app.services.coingecko_service import get_price
import datetime


today = datetime.datetime.today()
current_month = today.month
month_list = [
    'jan',
    'fev',
    'mar',
    'abr',
    'mai',
    'jun',
    'jul',
    'ago',
    'sep',
    'oct',
    'nov',
    'dec',
]
month_to_date = month_list[:current_month]


def get_user_coins(transactions_list):
    return list(transactions_list.keys())


def quantity_per_month(transactions_list):

    quantity = dict()

    user_coins = list(transactions_list.keys())

    # splits the transactions by coin by month
    for coin in user_coins:
        coin_transactions = transactions_list[coin]

        jan = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 1
        ]
        fev = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 2
        ]
        mar = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 3
        ]
        abr = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 4
        ]
        mai = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 5
        ]
        jun = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 6
        ]
        jul = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 7
        ]
        ago = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 8
        ]
        sep = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 9
        ]
        oct = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 10
        ]
        nov = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 11
        ]
        dec = [
            transaction
            for transaction in coin_transactions
            if transaction['date'].month == 12
        ]

        # gets the last coin net_quantity in each month
        qty_list = [
            jan[-1]['net_quantity'] if jan else 0,
            fev[-1]['net_quantity'] if fev else 0,
            mar[-1]['net_quantity'] if mar else 0,
            abr[-1]['net_quantity'] if abr else 0,
            mai[-1]['net_quantity'] if mai else 0,
            jun[-1]['net_quantity'] if jun else 0,
            jul[-1]['net_quantity'] if jul else 0,
            ago[-1]['net_quantity'] if ago else 0,
            sep[-1]['net_quantity'] if sep else 0,
            oct[-1]['net_quantity'] if oct else 0,
            nov[-1]['net_quantity'] if nov else 0,
            dec[-1]['net_quantity'] if dec else 0,
        ]

        # fill the quantity in months where there is no transaction
        start = 0
        for n in qty_list:
            if n != 0:
                start = qty_list.index(n)
                break

        i = start
        while i < len(qty_list):
            if qty_list[i] == 0:
                qty_list[i] = qty_list[i - 1]
            i += 1

        qty_to_date = qty_list[:current_month]

        qty_per_month = list(zip(month_to_date, qty_to_date))

        quantity[coin] = qty_per_month

    return quantity


def get_historical_price(transactions_list):
    historical_price = dict()
    user_coins = get_user_coins(transactions_list)

    for coin in user_coins:
        historical = (
            CoinsHistorical.query.filter_by(coin=coin)
            .order_by(CoinsHistorical.date.asc())
            .all()
        )
        historical_list = list()
        for price in historical:
            historical_list.append(price.price)
        historical_price[coin] = historical_list

    # current prices
    current_price = get_price()

    for coin in user_coins:
        price = current_price[coin]['brl']
        historical_price[coin].append(price)

    return historical_price


def get_positions(transactions_list, quantity, historical_price):

    user_coins = get_user_coins(transactions_list)
    result_per_coin = dict()

    for coin in user_coins:
        result_per_coin[coin] = dict()

        price_per_month = list(zip(month_to_date, historical_price[coin]))

        qty = quantity[coin]

        for item in qty:
            result_per_coin[coin][item[0]] = dict(qty=item[1])

        for item in price_per_month:
            result_per_coin[coin][item[0]].update(dict(price=item[1]))
    for coin in user_coins:
        for month in month_to_date:
            total = (
                result_per_coin[coin][month]['qty']
                * result_per_coin[coin][month]['price']
            )
            result_per_coin[coin][month].update(dict(total=total))

    return result_per_coin


def total_positions(transactions_list, result_per_coin):
    user_coins = get_user_coins(transactions_list)
    total_balance = dict()

    for month in month_to_date:
        total_balance[month] = list()
        for coin in user_coins:
            total_balance[month].append(result_per_coin[coin][month]['total'])

        total_balance[month] = round(sum(total_balance[month]), 2)

    return total_balance
