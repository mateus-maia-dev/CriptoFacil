from flask import Flask
from app import configurations
from app.configurations import database
from app.configurations import migrations
from app.configurations import jwt_authentication
from app import views
from app.services.coins_list import coins

def create_app():
    app = Flask(__name__)

    configurations.init_app(app)
    database.init_app(app)
    migrations.init_app(app)
    jwt_authentication.init_app(app)
    views.init_app(app)

    return app
    