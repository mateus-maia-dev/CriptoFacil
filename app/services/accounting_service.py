from .mock_data import tax_table


def create_accounting(transactions):
    accounting_per_coin = dict()

    user_coins = list(transactions.keys())

    for coin in user_coins:
        coin_transactions = transactions[coin]

        accounting_per_coin[coin] = list()

        for item in coin_transactions:

            month = item['date'].strftime('%B')

            ptax = item["ptax"]

            price_brl = (
                item["price_per_coin"]
                if item["fiat"] == 'brl'
                else item["price_per_coin"] * ptax
            )
            if item["foreign_exch"]:
                tax_table[month]['foreign_exch_total'] += price_brl * item["quantity"]

            if item["type"] == 'sell' or item["type"] == 'input':

                # if item['net_quantity'] >= item['quantity']:
                tax_table[month]['sell_total'] += price_brl * item["quantity"]
                tax_table[month]['profit'] += (
                    (price_brl - item["avg_price_brl"]) * item["quantity"]
                    if price_brl - item["avg_price_brl"] > 0
                    else 0
                )

            # fill the fields foreign_exch_total, status

            if tax_table[month]['foreign_exch_total'] > 30000:
                tax_table[month]['status'] = "NÃO ISENTO"

            # tax
            if tax_table[month]['sell_total'] > 35000:
                if tax_table[month]['profit'] < 5000000:
                    tax_table[month]['tax'] = tax_table[month]['profit'] * 0.15
                if (
                    tax_table[month]['profit'] > 5000000
                    and tax_table[month]['profit'] < 10000000
                ):
                    tax_table[month]['tax'] = tax_table[month]['profit'] * 0.175
                if (
                    tax_table[month]['profit'] > 10000000
                    and tax_table[month]['profit'] < 30000000
                ):
                    tax_table[month]['tax'] = tax_table[month]['profit'] * 0.2
                if tax_table[month]['profit'] > 30000000:
                    tax_table[month]['tax'] = tax_table[month]['profit'] * 0.225
    return tax_table
