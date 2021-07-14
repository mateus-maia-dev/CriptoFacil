from flask import Flask
from config import selector_config

# from environs import Env

# env = Env()


def init_app(app: Flask):
    # select_type = env("FLASK_ENV")
    object_config = selector_config["production"]
    app.config.from_object(object_config)
