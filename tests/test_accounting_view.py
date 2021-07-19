from flask.testing import FlaskClient
import pytest

from flask.testing import FlaskClient


@pytest.fixture
def new_user():
    yield {
        "name": "Maria",
        "last_name": "Joana",
        "email": "maria@mail.com",
        "password": "1234",
    }


def test_should_return_an_accounting(app_client: FlaskClient, new_user):
    user = app_client.post('/api/register', json=new_user)

    token = user.get_json()['token']
    headers = {'Authorization': f'Bearer {token}'}

    response = app_client.get('/api/accounting', headers=headers)

    assert response.status_code == 200
    assert type(response.get_json()) == dict
