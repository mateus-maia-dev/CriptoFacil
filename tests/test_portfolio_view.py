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


def test_should_retrieve_a_portfolio_with_transactions(
    app_client: FlaskClient, new_user, new_transaction
):
    user = app_client.post('/api/register', json=new_user)

    token = user.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    transaction = app_client.post(
        '/api/transactions/register', json=new_transaction, headers=headers
    )
    portfolio = app_client.get('/api/portfolio/list', headers=headers)

    assert portfolio.status_code == 200
    assert type(portfolio.get_json()) == list
    # colocar outros testes, se necessários


def test_should_retrieve_a_portfolio_with_no_transactions(
    app_client: FlaskClient, new_user
):
    user = app_client.post('/api/register', json=new_user)

    token = user.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    portfolio = app_client.get('/api/portfolio/list', headers=headers)

    assert portfolio.get_json() == []
