from flask import Flask
from flask.cli import AppGroup
import click
from app.services import create_coins_historical_models
from app.services.coins_list import coins


def cli_coins_historical(app: Flask):
    cli_coins_historical_group = AppGroup("coins_historical")

    @cli_coins_historical_group.command("create")
    def cli_coins_historical_create():

        create_coins_historical_models()

        click.echo(f"table coins_historical populated")

    app.cli.add_command(cli_coins_historical_group)


def cli_coins_list(app: Flask):
    cli_coins_list_group = AppGroup("coins_list")

    @cli_coins_list_group.command("create")
    def cli_coins_list_create():

        coins()

        click.echo(f"table coins_list populated")

    app.cli.add_command(cli_coins_list_group)


def init_app(app: Flask):
    cli_coins_historical(app)
    cli_coins_list(app)
