from flask.testing import FlaskClient
from ipdb.__main__ import set_trace
from requests.api import delete
from sqlalchemy.sql.functions import user
from app.models.user_model import User


def test_should_register_an_user(app_client: FlaskClient, new_user, sample_app):
    response = app_client.post('/api/register', json=new_user)  # new_user -> payload

    assert response.status_code == 201
    assert isinstance(response.get_json(), dict)
    assert 'token' in response.get_json().keys()

    with sample_app.test_request_context():
        found_user: User = User.query.filter_by(id=1).first()

        # set_trace()

    created_user = found_user.__dict__
    del created_user['password_hash']
    del created_user['_sa_instance_state']

    expected_user = {**new_user, 'id': 1}
    del expected_user['password']

    assert isinstance(found_user, User)
    assert expected_user == created_user


def test_should_log_in_an_user(app_client: FlaskClient, new_user):
    app_client.post('/api/register', json=new_user)

    credentials = {'email': new_user['email'], 'password': new_user['password']}

    response = app_client.post('/api/login', json=credentials)

    response_data = response.get_json()

    assert response.status_code == 200
    assert isinstance(response_data, dict)
    assert 'token' in response_data.keys()

    headers = {'Authorization': f'Bearer {response_data["token"]}'}

    response_valid_token = app_client.get('/api/accounting', headers=headers)

    # from app.services.mock_data import tax_table

    assert response_valid_token.status_code == 200
    # assert response_valid_token.get_json() == tax_table


# def test_should_verify_register_in_database(app_client: FlaskClient, new_user):
#     user = app_client.post('/api/register', json=new_user)

#     users = User.query.filter_by(id=1).first()
#     set_trace()


#     # TODO Fazer o teste no banco de dados
#     assert len(users) == 1


# def test_shouldnt_register_an_user():
#     new_user = {
#         "n0me": "Maria",
#         "las_name": "Joana",
#         "eail": "maria@mail.com",
#         "pasword": "1234",
#     }
#     assert 'token' not in response.get_json().keys()
