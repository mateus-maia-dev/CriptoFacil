from flask import current_app
from app.models.transactions_model import Transaction
from app.models.accounting_model import Accounting
from datetime import datetime, time
from ipdb import set_trace
from .mock_data import tax_table
from flask_jwt_extended import get_jwt_identity


def populate_accounting(user_id):
    session = current_app.db.session

    transaction: Transaction = (
        Transaction.query.filter_by(user_id=user_id)
        .order_by(Transaction.id.desc())
        .first()
    )

    price_brl = (
        transaction.price_per_coin
        if transaction.fiat == 'brl'
        else transaction.price_per_coin * 5
    )

    date = transaction.date
    transaction_id = transaction.id
    sell_total = 0
    profit = 0
    foreign_exch_total = 0

    if transaction.foreign_exch:
        foreign_exch_total = price_brl * transaction.quantity

    if transaction.type == 'sell' or transaction.type == 'input':
        sell_total = price_brl * transaction.quantity
        profit = (
            (price_brl - transaction.avg_price_brl) * transaction.quantity
            if price_brl - transaction.avg_price_brl > 0
            else 0
        )

    new_accounting = Accounting(
        date=date,
        sell_total=sell_total,
        profit=profit,
        foreign_exch_total=foreign_exch_total,
        transaction_id=transaction_id,
    )

    session.add(new_accounting)
    session.commit()


def get_accounting():
    session = current_app.db.session

    user_id = get_jwt_identity()

    aux_var = (
        session.query(Transaction, Accounting)
        .join(Transaction, Transaction.id == Accounting.transaction_id)
        .filter(Transaction.user_id == user_id)
        .all()
    )

    user_accountings_list = [account[1] for account in aux_var]

    # Return tax

    for account in user_accountings_list:
        month = account.date.strftime('%b')

        tax_table[month]['sell_total'] += account.sell_total
        tax_table[month]['profit'] += account.profit

        if tax_table[month]['sell_total'] > 30000:
            tax_table[month]['tax'] = tax_table[month]['profit'] * 0.3

    return tax_table
