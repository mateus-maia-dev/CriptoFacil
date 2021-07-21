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
    {'coin': 'bitcoin', 'date': '01-31-2021', 'price': 186808.03706014613},
    {'coin': 'ethereum', 'date': '01-31-2021', 'price': 7496.609252771344},
    {'coin': 'tether', 'date': '01-31-2021', 'price': 5.443210472994422},
    {'coin': 'cardano', 'date': '01-31-2021', 'price': 1.9690535784854122},
    {'coin': 'litecoin', 'date': '01-31-2021', 'price': 726.4083035365211},
    {'coin': 'stellar', 'date': '01-31-2021', 'price': 1.7684228200222962},
    {'coin': 'usd-coin', 'date': '01-31-2021', 'price': 5.443208002316456},
    {'coin': 'eos', 'date': '01-31-2021', 'price': 15.914091613531989},
    {'coin': 'monero', 'date': '01-31-2021', 'price': 758.7276311400542},
    {'coin': 'binance-usd', 'date': '01-31-2021', 'price': 5.433956917468385},
    {'coin': 'tezos', 'date': '01-31-2021', 'price': 15.745243333003305},
    {'coin': 'neo', 'date': '01-31-2021', 'price': 124.32480599599626},
    {'coin': 'nem', 'date': '01-31-2021', 'price': 1.2601794842498806},
    {'coin': 'zilliqa', 'date': '01-31-2021', 'price': 0.39778358379641454},
    {'coin': 'icon', 'date': '01-31-2021', 'price': 4.14280176067329},
    {'coin': 'true-usd', 'date': '01-31-2021', 'price': 5.434825871589757},
    {'coin': 'dash', 'date': '01-31-2021', 'price': 569.6273866237837},
    {'coin': 'decred', 'date': '01-31-2021', 'price': 340.37661677102295},
    {'coin': 'bitcoin', 'date': '02-28-2021', 'price': 261222.4250154972},
    {'coin': 'ethereum', 'date': '02-28-2021', 'price': 8287.541526685944},
    {'coin': 'tether', 'date': '02-28-2021', 'price': 5.56558220386223},
    {'coin': 'cardano', 'date': '02-28-2021', 'price': 7.5186543269835315},
    {'coin': 'litecoin', 'date': '02-28-2021', 'price': 970.2473504874896},
    {'coin': 'stellar', 'date': '02-28-2021', 'price': 2.482375097812126},
    {'coin': 'usd-coin', 'date': '02-28-2021', 'price': 5.6500655555799835},
    {'coin': 'eos', 'date': '02-28-2021', 'price': 20.780905465018265},
    {'coin': 'monero', 'date': '02-28-2021', 'price': 1181.5153682278947},
    {'coin': 'binance-usd', 'date': '02-28-2021', 'price': 5.681845556178229},
    {'coin': 'tezos', 'date': '02-28-2021', 'price': 20.594744444510553},
    {'coin': 'neo', 'date': '02-28-2021', 'price': 210.8960053308035},
    {'coin': 'nem', 'date': '02-28-2021', 'price': 3.2786564276303416},
    {'coin': 'zilliqa', 'date': '02-28-2021', 'price': 0.6566043124928317},
    {'coin': 'icon', 'date': '02-28-2021', 'price': 8.630575869456964},
    {'coin': 'true-usd', 'date': '02-28-2021', 'price': 5.665768336771724},
    {'coin': 'dash', 'date': '02-28-2021', 'price': 1200.2005191573385},
    {'coin': 'decred', 'date': '02-28-2021', 'price': 765.5073315524086},
    {'coin': 'bitcoin', 'date': '03-31-2021', 'price': 338723.32570228947},
    {'coin': 'ethereum', 'date': '03-31-2021', 'price': 10624.942905287671},
    {'coin': 'tether', 'date': '03-31-2021', 'price': 5.772554472699129},
    {'coin': 'cardano', 'date': '03-31-2021', 'price': 6.993852561133799},
    {'coin': 'litecoin', 'date': '03-31-2021', 'price': 1130.0667776249657},
    {'coin': 'stellar', 'date': '03-31-2021', 'price': 2.325962535938315},
    {'coin': 'usd-coin', 'date': '03-31-2021', 'price': 5.777500744149672},
    {'coin': 'eos', 'date': '03-31-2021', 'price': 25.03722821578729},
    {'coin': 'monero', 'date': '03-31-2021', 'price': 1407.1960539709755},
    {'coin': 'binance-usd', 'date': '03-31-2021', 'price': 5.7711620651391735},
    {'coin': 'tezos', 'date': '03-31-2021', 'price': 26.310634383488072},
    {'coin': 'neo', 'date': '03-31-2021', 'price': 259.3507741733367},
    {'coin': 'nem', 'date': '03-31-2021', 'price': 2.2680321380437416},
    {'coin': 'zilliqa', 'date': '03-31-2021', 'price': 1.063471519970492},
    {'coin': 'icon', 'date': '03-31-2021', 'price': 15.372476860793382},
    {'coin': 'true-usd', 'date': '03-31-2021', 'price': 5.772267958386702},
    {'coin': 'dash', 'date': '03-31-2021', 'price': 1248.91051848115},
    {'coin': 'decred', 'date': '03-31-2021', 'price': 1041.1830357004399},
    {'coin': 'bitcoin', 'date': '04-30-2021', 'price': 286093.8464025924},
    {'coin': 'ethereum', 'date': '04-30-2021', 'price': 14719.246184448712},
    {'coin': 'tether', 'date': '04-30-2021', 'price': 5.342225605960517},
    {'coin': 'cardano', 'date': '04-30-2021', 'price': 7.020275421140506},
    {'coin': 'litecoin', 'date': '04-30-2021', 'price': 1365.3815485741125},
    {'coin': 'stellar', 'date': '04-30-2021', 'price': 2.6380617414450716},
    {'coin': 'usd-coin', 'date': '04-30-2021', 'price': 5.345952680085261},
    {'coin': 'eos', 'date': '04-30-2021', 'price': 31.386293052695034},
    {'coin': 'monero', 'date': '04-30-2021', 'price': 2174.8911670961484},
    {'coin': 'binance-usd', 'date': '04-30-2021', 'price': 5.344169777963941},
    {'coin': 'tezos', 'date': '04-30-2021', 'price': 27.934883507804948},
    {'coin': 'neo', 'date': '04-30-2021', 'price': 477.7065081605829},
    {'coin': 'nem', 'date': '04-30-2021', 'price': 1.8162941015967327},
    {'coin': 'zilliqa', 'date': '04-30-2021', 'price': 1.029436671666403},
    {'coin': 'icon', 'date': '04-30-2021', 'price': 12.665107201997225},
    {'coin': 'true-usd', 'date': '04-30-2021', 'price': 5.336531290686818},
    {'coin': 'dash', 'date': '04-30-2021', 'price': 1526.3291434416828},
    {'coin': 'decred', 'date': '04-30-2021', 'price': 1114.4437334771492},
    {'coin': 'bitcoin', 'date': '05-31-2021', 'price': 186659.5799582725},
    {'coin': 'ethereum', 'date': '05-31-2021', 'price': 12521.687310833526},
    {'coin': 'tether', 'date': '05-31-2021', 'price': 5.220061154923275},
    {'coin': 'cardano', 'date': '05-31-2021', 'price': 8.241230953823313},
    {'coin': 'litecoin', 'date': '05-31-2021', 'price': 893.0456464740768},
    {'coin': 'stellar', 'date': '05-31-2021', 'price': 1.967233668634829},
    {'coin': 'usd-coin', 'date': '05-31-2021', 'price': 5.228673103042277},
    {'coin': 'eos', 'date': '05-31-2021', 'price': 31.531079055210657},
    {'coin': 'monero', 'date': '05-31-2021', 'price': 1363.7489236766078},
    {'coin': 'binance-usd', 'date': '05-31-2021', 'price': 5.220793660683904},
    {'coin': 'tezos', 'date': '05-31-2021', 'price': 17.158970567304447},
    {'coin': 'neo', 'date': '05-31-2021', 'price': 268.8851505558641},
    {'coin': 'nem', 'date': '05-31-2021', 'price': 0.9649249801775365},
    {'coin': 'zilliqa', 'date': '05-31-2021', 'price': 0.5523090393498388},
    {'coin': 'icon', 'date': '05-31-2021', 'price': 5.502104171012056},
    {'coin': 'true-usd', 'date': '05-31-2021', 'price': 5.219049921087191},
    {'coin': 'dash', 'date': '05-31-2021', 'price': 953.1338158035264},
    {'coin': 'decred', 'date': '05-31-2021', 'price': 810.1370249648542},
    {'coin': 'bitcoin', 'date': '06-30-2021', 'price': 178291.107813396},
    {'coin': 'ethereum', 'date': '06-30-2021', 'price': 10753.282256398144},
    {'coin': 'tether', 'date': '06-30-2021', 'price': 4.95896876170584},
    {'coin': 'cardano', 'date': '06-30-2021', 'price': 6.797072244282432},
    {'coin': 'litecoin', 'date': '06-30-2021', 'price': 714.178266759836},
    {'coin': 'stellar', 'date': '06-30-2021', 'price': 1.3947972460099354},
    {'coin': 'usd-coin', 'date': '06-30-2021', 'price': 4.954646744495748},
    {'coin': 'eos', 'date': '06-30-2021', 'price': 20.491816438304934},
    {'coin': 'monero', 'date': '06-30-2021', 'price': 1079.278546119828},
    {'coin': 'binance-usd', 'date': '06-30-2021', 'price': 4.963180863444025},
    {'coin': 'tezos', 'date': '06-30-2021', 'price': 14.73060805543447},
    {'coin': 'neo', 'date': '06-30-2021', 'price': 173.90361355240975},
    {'coin': 'nem', 'date': '06-30-2021', 'price': 0.6366648475493712},
    {'coin': 'zilliqa', 'date': '06-30-2021', 'price': 0.42833985906856664},
    {'coin': 'icon', 'date': '06-30-2021', 'price': 4.068319587351589},
    {'coin': 'true-usd', 'date': '06-30-2021', 'price': 4.952855804493291},
    {'coin': 'dash', 'date': '06-30-2021', 'price': 693.6364139297316},
    {'coin': 'decred', 'date': '06-30-2021', 'price': 726.3916163299344},
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
