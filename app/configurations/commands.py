from flask import Flask
from flask.cli import AppGroup
import click
from app.services import create_coins_historical_models


def cli_coins_historical(app: Flask):
    cli_coins_historical_group = AppGroup("coins_historical")

    @cli_coins_historical_group.command("create")
    def cli_coins_historical_create():

        create_coins_historical_models()

        click.echo(f"table coins_historical populated")

    app.cli.add_command(cli_coins_historical_group)


def init_app(app: Flask):
    cli_coins_historical(app)
