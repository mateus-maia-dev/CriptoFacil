from flask.testing import FlaskClient
import pytest
from ipdb import set_trace


@pytest.fixture
def new_user():
    yield {
        "name": "Maria",
        "last_name": "Joana",
        "email": "maria@mail.com",
        "password": "1234",
    }


@pytest.fixture
def new_transaction():
    yield {
        "date": "2021-01-06",
        "type": "buy",
        "coin": "bitcoin",
        "fiat": "brl",
        "price_per_coin": 100000,
        "quantity": 2,
        "foreign_exch": True,
    }


def test_should_make_a_transaction(app_client: FlaskClient, new_user, new_transaction):
    user = app_client.post('/api/register', json=new_user)

    token = user.get_json()['token']

    headers = {'Authorization': f'Bearer {token}'}

    transaction = app_client.post(
        '/api/transactions/register', json=new_transaction, headers=headers
    )

    assert transaction.status_code == 201
    assert type(transaction.get_json()) == dict
    # Colocar outros testes aqui, se necessários
