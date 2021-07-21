from flask.testing import FlaskClient

from flask.testing import FlaskClient


def test_should_return_an_accounting(app_client: FlaskClient, new_user):
    app_client.post('/api/register', json=new_user)

    credentials = {'email': new_user['email'], 'password': new_user['password']}

    response = app_client.post('/api/login', json=credentials)

    token = response.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    response = app_client.get('/api/accounting', headers=headers)

    assert response.status_code == 200
    assert type(response.get_json()) == dict
