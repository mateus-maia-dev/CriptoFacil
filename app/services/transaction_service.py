from datetime import date
from ipdb.__main__ import set_trace
from app.models.transactions_model import Transaction
from flask import Flask, request, current_app
from app.services.helper import init_app, get_user
from flask_restful import reqparse
from flask_jwt_extended import jwt_required


def create_transaction():
    # data = request.get_json()

    parser = reqparse.RequestParser()

    parser.add_argument("date", type=date, required=True)
    parser.add_argument("type", type=str, choices=('buy', 'sell'), required=True)
    parser.add_argument("coin", type=str, choices=('bitcoin'), required=True)
    parser.add_argument("fiat", type=str, choices=('usd', 'brl'), required=True)
    parser.add_argument("price_per_coin", type=str, required=True)
    parser.add_argument("quantity", type=str, required=True)
    parser.add_argument(
        "brazilian_exch", choices=('true', 'false'), type=str, required=True
    )
    # TODO Cada transação receberá a ID do usuário. Com isso não se faz mais necessária a tabela portfolio
    # com vamos utilizar o jwt para autenticação de rotas. Seria interessante usar a lib jwt-decode
    # para pegar o id do usuário
    set_trace()

    new_transaction: Transaction = Transaction(**parser.parse_args())
    init_app(new_transaction)

    return {
        "date": new_transaction.date,
        "type": new_transaction.type,
        "coin": new_transaction.type,
        "fiat": new_transaction.type,
        "price_per_coin": new_transaction.price_per_coin,
        "quantity": new_transaction.quantity,
        "brazilian_exch": new_transaction.brazilian_exch,
    }
