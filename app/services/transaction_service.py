from app.services.current_dollar_value import get_data
import ipdb


def get_transations(transactions):
    net_transactions = dict()
    transactions_list = list()
    transactions_per_coin = dict()

    coins_list = [coin.coin for coin in transactions]
    coins_set = set(coins_list)
    user_coins = list(coins_set)

    for coin in user_coins:
        coin_transactions = [
            transaction for transaction in transactions if transaction.coin == coin]

        transactions_per_coin[coin] = list()

        net_quantity = 0
        avg_price_brl = 0
        avg_price_usd = 0

        for item in coin_transactions:
            get_ptax = str(item.date)
            get_ptax_str = get_data(get_ptax)
            ptax = float(get_ptax_str['sell_rate'])

            price_usd = item.price_per_coin if item.fiat == 'usd' else item.price_per_coin / ptax
            price_brl = item.price_per_coin if item.fiat == 'brl' else item.price_per_coin * ptax

            if item.type == 'buy' or item.type == 'output':
                net_quantity += item.quantity

                avg_price_brl = (
                    price_brl * item.quantity + avg_price_brl *
                    (net_quantity - item.quantity)
                ) / net_quantity
                avg_price_usd = (
                    price_usd * item.quantity + avg_price_usd *
                    (net_quantity - item.quantity)
                ) / net_quantity

            if item.type == 'sell' or item.type == 'input':
                avg_price_brl = result["avg_price_brl"]
                avg_price_usd = result["avg_price_usd"]
                net_quantity = result["net_quantity"] - item.quantity

            result = {
                "date": item.date,
                "type": item.type,
                "coin": item.coin,
                "fiat": item.fiat,
                "price_per_coin": round(item.price_per_coin, 2),
                "quantity": item.quantity,
                "net_quantity": net_quantity,
                "avg_price_brl": round(avg_price_brl, 2),
                "avg_price_usd": round(avg_price_usd, 2),
                "foreign_exch": item.foreign_exch
            }

            transactions_per_coin[coin].append(result)

    # print('transactions_per_coin', transactions_per_coin)
    resultado = list()
    resultado.append(transactions_per_coin)
    print(resultado)

    return resultado


def get_accounting(transactions):
    accounting = dict()
    accounting_list = list()

    sell_total = 0
    profit = 0
    foreign_exch_total = 0

    for item in transactions:
        get_ptax = str(item.date)
        get_ptax_str = get_data(get_ptax)
        ptax = float(get_ptax_str['sell_rate'])

        date = item.date
        transaction_id = item.id

        price_brl = item.price_per_coin if item.fiat == 'brl' else item.price_per_coin * ptax

        if item.foreign_exch:
            foreign_exch_total = price_brl * item.quantity

        if item.type == 'sell' or item.type == 'input':
            sell_total = price_brl * item.quantity
            profit = (
                (price_brl - item.avg_price_brl) * item.quantity
                if price_brl - item.avg_price_brl > 0
                else 0
            )

        accounting = {
            "date": date,
            "transaction_id": transaction_id,
            "sell_total": sell_total,
            "profit": profit,
            "foreign_exch_total": foreign_exch_total,
        }

        accounting_list.append(accounting)

    return accounting_list
