import requests


def get_price():
    response = requests.get(
        'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin%2Cethereum%2Ctether%2Ccardano%2Clitecoin%2Cstellar%2Cusd-coin%2Ceos%2Cmonero%2Cbinance-usd%2Ctezos%2Cneo%2Cnem%2Czilliqa%2Cicon%2Ctrue-usd%2Cdash%2Cdecred&vs_currencies=usd%2Cbrl&include_24hr_change=true'
    )

    return response.json()
