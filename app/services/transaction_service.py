from app.services.current_dollar_value import get_data


def get_transations(transactions):
    net_transactions = dict()
    transactions_list = list()
    
    net_quantity = 0
    avg_price_brl = 0
    avg_price_usd = 0

    for item in transactions:
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
            avg_price_brl = net_transactions["avg_price_brl"]
            avg_price_usd = net_transactions["avg_price_usd"]
            net_quantity = net_transactions["net_quantity"] - item.quantity

        net_transactions = {
            "net_quantity": net_quantity,
            "avg_price_brl": avg_price_brl,
            "avg_price_usd": avg_price_usd,
            "date": item.date,
            "type": item.type,
            "coin": item.coin,
            "fiat": item.fiat,
            "price_per_coin": item.price_per_coin,
            "quantity": item.quantity,
            "foreign_exch": item.foreign_exch
        }

        transactions_list.append(net_transactions)

    return transactions_list    


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
