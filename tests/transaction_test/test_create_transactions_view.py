from flask.testing import FlaskClient
from app.models.transactions_model import Transaction


def test_should_make_a_transaction(
    app_client: FlaskClient, new_user, new_transaction, sample_app
):
    app_client.post('/api/register', json=new_user)

    credentials = {'email': new_user['email'], 'password': new_user['password']}

    response = app_client.post('/api/login', json=credentials)

    token = response.get_json()['token']

    headers = {'Authorization': f'Bearer {token}'}

    transaction = app_client.post(
        '/api/transactions/register', json=new_transaction, headers=headers
    )

    with sample_app.test_request_context():
        found_transaction: Transaction = Transaction.query.filter_by(id=1).first()

    found_transaction = found_transaction.__dict__

    del found_transaction['_sa_instance_state']
    del found_transaction['avg_price_brl']
    del found_transaction['avg_price_usd']
    del found_transaction['net_quantity']
    del found_transaction['user_id']

    found_transaction['date'] = found_transaction['date'].isoformat()

    expected_transaction = {**new_transaction, "id": 1}
    # set_trace()
    assert transaction.status_code == 201
    assert type(transaction.get_json()) == dict
    assert expected_transaction == found_transaction
    # Colocar outros testes aqui, se necessários
    # Verificar se transação foi inserida no banco de dados
