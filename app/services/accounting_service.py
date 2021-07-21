from flask import current_app
from app.models.transactions_model import Transaction
from app.models.accounting_model import Accounting
from datetime import datetime, time
from ipdb import set_trace
from .mock_data import tax_table
from flask_jwt_extended import get_jwt_identity


def create_accounting(transactions):
    accounting = dict()
    accounting_per_coin = dict()

    user_coins = list(transactions.keys())

    for coin in user_coins:
        coin_transactions = transactions[coin]

        accounting_per_coin[coin] = list()

        sell_total = 0
        profit = 0
        foreign_exch_total = 0

        for item in coin_transactions:
            date = item["date"]
            transaction_id = item["id"]
            ptax = item["ptax"]

            price_brl = (
                item["price_per_coin"]
                if item["fiat"] == 'brl'
                else item["price_per_coin"] * ptax
            )

            if item["foreign_exch"]:
                foreign_exch_total = price_brl * item["quantity"]

            if item["type"] == 'sell' or item["type"] == 'input':
                sell_total = price_brl * item["quantity"]
                profit = (
                    (price_brl - item["avg_price_brl"]) * item["quantity"]
                    if price_brl - item["avg_price_brl"] > 0
                    else 0
                )

            accounting = {
                "date": date,
                "transaction_id": transaction_id,
                "sell_total": sell_total,
                "profit": profit,
                "foreign_exch_total": foreign_exch_total,
            }
            set_trace()
            accounting_per_coin[coin].append(accounting)

    return accounting_per_coin


def get_accounting():
    session = current_app.db.session
    set_trace()
    user_id = get_jwt_identity()

    aux_var = (
        session.query(Transaction, Accounting)
        .join(Transaction, Transaction.id == Accounting.transaction_id)
        .filter(Transaction.user_id == user_id)
        .all()
    )

    user_accountings_list = [account[1] for account in aux_var]

    # Return tax_table

    for account in user_accountings_list:
        month = account.date.strftime('%b')
        year = account.date.strftime('%Y')

        tax_table[month]['sell_total'] += account.sell_total
        tax_table[month]['profit'] += account.profit

        # fill the fields foreign_exch_total, status from accounting_table
        tax_table[month]['foreign_exch_total'] += account.foreign_exch_total
        if tax_table[month]['foreign_exch_total'] > 30000:
            tax_table[month]['status'] = "NÃO ISENTO"

        # fill the fields sell_total, profit, and tax from accounting_table
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
