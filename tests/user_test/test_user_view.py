from flask.testing import FlaskClient
from app.models.user_model import User


def test_should_register_an_user(app_client: FlaskClient, new_user, sample_app):
    response = app_client.post('/api/register', json=new_user)

    assert response.status_code == 201
    assert isinstance(response.get_json(), dict)

    with sample_app.test_request_context():
        found_user: User = User.query.filter_by(id=1).first()

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

    assert response_valid_token.status_code == 200
    # assert response_valid_token.get_json() == tax_table
