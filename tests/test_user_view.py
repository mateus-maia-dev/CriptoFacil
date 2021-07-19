from flask.testing import FlaskClient
from ipdb.__main__ import set_trace
import pytest
from app.models.user_model import User


@pytest.fixture(
    scope="module"
)  # scope para caso eu queira manter o mesmo objeto para todos os teste
def new_user():
    yield {
        "name": "Maria",
        "last_name": "Joana",
        "email": "maria@mail.com",
        "password": "1234",
    }


def test_should_register_an_user(app_client: FlaskClient, new_user):
    response = app_client.post('/api/register', json=new_user)  # new_user -> payload

    assert response.status_code == 201


def test_should_log_in_an_user(app_client: FlaskClient, new_user):
    user = app_client.post('/api/register', json=new_user)

    credentials = {'email': new_user['email'], 'password': new_user['password']}

    response = app_client.post('/api/login', json=credentials)

    assert response.status_code == 200
    assert type(response.get_json()) == dict
    assert 'token' in response.get_json().keys()


def test_should_verify_register_in_database(app_client: FlaskClient, new_user):
    user = app_client.post('/api/register', json=new_user)

    users = User.query.filter_by(id=1).first()
    set_trace()

    # TODO Fazer o teste no banco de dados
    assert len(users) == 1


# def test_shouldnt_register_an_user():
#     new_user = {
#         "n0me": "Maria",
#         "las_name": "Joana",
#         "eail": "maria@mail.com",
#         "pasword": "1234",
#     }
#     assert 'token' not in response.get_json().keys()
