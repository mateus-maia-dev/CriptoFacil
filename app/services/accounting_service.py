from flask import current_app
from app.models.transactions_model import Transaction
from app.models.accounting_model import Accounting


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
