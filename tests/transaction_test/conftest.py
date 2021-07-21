import pytest


@pytest.fixture
def new_transaction():
    yield {
        "date": "2021-01-06",
        "type": "buy",
        "coin": "bitcoin",
        "fiat": "brl",
        "price_per_coin": 100000.0,
        "quantity": 2.0,
        "foreign_exch": True,
    }
