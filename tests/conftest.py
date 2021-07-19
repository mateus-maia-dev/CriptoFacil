from flask import Flask
import pytest
from app import create_app

# uso as fixture pra reutilizar códigos
@pytest.fixture
def sample_app():

    yield create_app()
    # yield vai criar uma instancia de app, e vai retornar a instancia
    # para todos os apps


@pytest.fixture
def app_client(sample_app):

    with sample_app.test_request_context():
        sample_app.db.create_all()  # Cria todas as tabelas (setup)

    yield sample_app.test_client()  # Retorna o teste client enquanto alguem precisar do valor
    # client test que faz a requisição,
    with sample_app.test_request_context():
        sample_app.db.drop_all()  # "Teardown" excluir as tabelas
