from flask import current_app
from ipdb import set_trace


def init_app(model) -> None:
    current_app.db.session.add(model)
    current_app.db.session.commit()


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

    keys = body.keys()

    missing_fields = [key for key in required_fields if key not in keys]
    set_trace()
    if missing_fields:
        raise KeyError(
            {
                "error": {
                    "required_field": required_fields,
                    "missing_fields": list(missing_fields),
                }
            }
        )


def verify_received_keys_from_create_user():
    ...


def verify_received_keys_from_login():
    ...
