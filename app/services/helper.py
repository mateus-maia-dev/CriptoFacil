from flask import current_app
from ipdb import set_trace


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
