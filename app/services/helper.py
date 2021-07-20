from re import I
from flask import current_app
from ipdb import set_trace
import re
from app.services.coins_list import coinsListArr


def init_app(model) -> None:
    current_app.db.session.add(model)
    current_app.db.session.commit()


def validate_fields(body: dict, required_fields: list):
    keys = body.keys()

    missing_fields = [key for key in required_fields if key not in keys]

    if missing_fields:
        raise KeyError(
            {
                'error': {
                    'required_fields': required_fields,
                    'missing_fields': missing_fields,
                }
            }
        )


def verify_received_keys_from_create_transactions(body: dict):
    required_fields = [
        'date',
        'type',
        'coin',
        'fiat',
        'price_per_coin',
        'quantity',
        'foreign_exch',
    ]

    validate_fields(body, required_fields)


def verify_received_keys_from_create_user(body: dict):
    required_fields = ['name', 'email', 'last_name', 'password']

    validate_fields(body, required_fields)


def verify_received_keys_from_login(body: dict):
    required_fields = ['email', 'password']

    validate_fields(body, required_fields)


def validated_values_for_register_user(body: dict):
    name = body.get("name")
    last_name = body.get("last_name")
    email = body.get("email")
    password = body.get("password")

    email_pattern = r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
    name_pattern = r"^[a-z]{3,15}$"
    password_pattern = (
        r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$"
    )

    if not bool(re.match(email_pattern, email)):
        raise Exception({"error": "invalid value on email's field"})

    if not bool(re.match(name_pattern, name)):
        raise Exception({"error": "invalid value on name's field"})

    if not bool(re.match(name_pattern, last_name)):
        raise Exception({"error": "invalid value on last_name's field"})

    if not bool(re.match(password_pattern, password)):
        raise Exception(
            {
                "error": "password must contain at least 1 capital letter, a special character and a number."
            }
        )


def validated_values_for_login(body: dict):
    email = body.get("email")

    email_pattern = r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"

    if not bool(re.match(email_pattern, email)):
        raise Exception({"error": "invalid value on email's field"})


def validated_values_for_register_transaction(body: dict):
    date = body.get("date")
    type = body.get("type")
    coin = body.get("coin")
    fiat = body.get("fiat")
    price_per_coin = body.get("price_per_coin")
    quantity = body.get("quantity")
    foreign_exch = body.get("foreign_exch")

    date_pattern = r"(\d{4})[/.-](\d{2})[/.-](\d{2})$"
    type_pattern = ["buy", "sell"]
    coin_pattern = [coin['coin'] for coin in coinsListArr]
    fiat_pattern = ["usd", "brl"]

    if not bool(re.match(date_pattern, date)):
        raise Exception({"error": "date format is not correct."})
    if type not in type_pattern:
        raise Exception({"error": "only entries 'buy' and 'sell' are accepted"})
    if coin not in coin_pattern:
        raise Exception({"error": "Invalid coin."})
    if fiat not in fiat_pattern:
        raise Exception({"error": "only 'brl' and 'usd' are accepted."})
    if price_per_coin < 0:
        raise Exception({"error": "the 'price_per_coin' must be greater than 0"})
    if quantity < 0:
        raise Exception({"error": "the quantity must be greater than 0"})
    if not isinstance(foreign_exch, bool):
        raise Exception({"error": "the field 'foreign_exc' must be 'True'or 'False'"})
