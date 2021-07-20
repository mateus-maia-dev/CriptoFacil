from flask import Flask
from app import configurations
from app.configurations import database, migrations, jwt_authentication, api, commands
from app import views


def create_app():
    app = Flask(__name__)

    configurations.init_app(app)
    database.init_app(app)
    migrations.init_app(app)
    jwt_authentication.init_app(app)
    views.init_app(app)
    commands.init_app(app)

    app.config["JSON_SORT_KEYS"] = False

    return app
