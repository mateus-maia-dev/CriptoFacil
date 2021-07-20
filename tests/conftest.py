from app import create_app
import pytest
from faker import Faker

# uso as fixture pra reutilizar códigos
@pytest.fixture
def sample_app():

    yield create_app()
    # yield vai criar uma instancia de app, e vai retornar a instancia
    # para todos os apps


@pytest.fixture(
    scope="module"
)  # scope para caso eu queira manter o mesmo objeto para todos os testes no modulo. O módulo é o conftest
def new_user():
    fake = Faker(["en_US"])
    yield {
        "name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": fake.password(),
    }


@pytest.fixture
def app_client(sample_app):

    with sample_app.test_request_context():
        sample_app.db.create_all()  # Cria todas as tabelas (setup)

    yield sample_app.test_client()  # Retorna o teste client enquanto alguem precisar do valor
    # client test que faz a requisição,
    with sample_app.test_request_context():
        sample_app.db.drop_all()  # "Teardown" excluir as tabelas
