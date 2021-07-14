import requests
from flask import current_app
from app.models.coins_historical_quotes_model import CoinsHistorical


# List of all coins available in the application
coins = [
    'bitcoin',
    'ethereum',
    'tether',
    'cardano',
    'litecoin',
    'stellar',
    'usd-coin',
    'eos',
    'monero',
    'binance-usd',
    'tezos',
    'neo',
    'nem',
    'zilliqa',
    'icon',
    'true-usd',
    'dash',
    'decred',
]

# List of dates to get prices
dates = [
    "01-01-2021",
    "31-01-2021",
    "28-02-2021",
    "31-03-2021",
    "30-04-2021",
    "31-05-2021",
    "30-06-2021",
]


# Function to get historical prices based on coin and date
def get_price(coin, date):
    response = requests.get(
        f'https://api.coingecko.com/api/v3/coins/{coin}/history?date={date}&localization=false'
    )

    prices = response.json()

    json = {
        "coin": prices['id'],
        "date": date,
        "price": prices['market_data']['current_price']['brl'],
    }

    return json


# Function to create a list of all prices collected. Necessary to get one date at time due to API request limit.
def make_list():
    price_list = list()

    for coin in coins:
        price = get_price(coin, dates[6])
        price_list.append(price)

    return price_list


historical_prices = [
    {'coin': 'bitcoin', 'date': '01-01-2021', 'price': 150730.83217785193},
    {'coin': 'ethereum', 'date': '01-01-2021', 'price': 3836.0809299864463},
    {'coin': 'tether', 'date': '01-01-2021', 'price': 5.193770397675597},
    {'coin': 'cardano', 'date': '01-01-2021', 'price': 0.9456046358307472},
    {'coin': 'litecoin', 'date': '01-01-2021', 'price': 648.1545175648345},
    {'coin': 'stellar', 'date': '01-01-2021', 'price': 0.6679603776847395},
    {'coin': 'usd-coin', 'date': '01-01-2021', 'price': 5.201341624133275},
    {'coin': 'eos', 'date': '01-01-2021', 'price': 13.48160604145111},
    {'coin': 'monero', 'date': '01-01-2021', 'price': 813.9433440796322},
    {'coin': 'binance-usd', 'date': '01-01-2021', 'price': 5.196540776064342},
    {'coin': 'tezos', 'date': '01-01-2021', 'price': 10.475906351521624},
    {'coin': 'neo', 'date': '01-01-2021', 'price': 74.22155952843826},
    {'coin': 'nem', 'date': '01-01-2021', 'price': 1.0617012630201987},
    {'coin': 'zilliqa', 'date': '01-01-2021', 'price': 0.42966583706516437},
    {'coin': 'icon', 'date': '01-01-2021', 'price': 2.419721885618852},
    {'coin': 'true-usd', 'date': '01-01-2021', 'price': 5.1965267827812935},
    {'coin': 'dash', 'date': '01-01-2021', 'price': 517.5128858030487},
    {'coin': 'decred', 'date': '01-01-2021', 'price': 212.1355059128222},
]


def create_coins_historical_models():
    session = current_app.db.session
    models_list = list()

    for coin in historical_prices:
        model: CoinsHistorical = CoinsHistorical(
            coin=coin['coin'], date=coin['date'], price=coin['price']
        )
        models_list.append(model)

    session.add_all(models_list)
    session.commit()
