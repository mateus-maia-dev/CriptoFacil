import pytest
from flask.testing import FlaskClient
from app.services.accounting_service import get_accounting, populate_accounting
from flask_jwt_extended import get_jwt_identity


@pytest.fixture
def new_user():
    yield {
        "name": "Maria",
        "last_name": "Joana",
        "email": "maria@mail.com",
        "password": "1234",
    }


# def test_should_
