from flask.testing import FlaskClient
import pytest
from ipdb import set_trace


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
    # Verificar se transação foi inserida no banco de dados
