from app.models.coins_list_model import Coins_List
from flask import current_app

coinsListArr = [
    {
        "coin": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "image":
        "https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png?1547033579",
    },
    {
        "coin": "ethereum",
        "symbol": "eth",
        "name": "Ethereum",
        "image":
        "https://assets.coingecko.com/coins/images/279/thumb/ethereum.png?1595348880",
    },
    {
        "coin": "binancecoin",
        "symbol": "bnb",
        "name": "Binance Coin",
        "image":
        "https://assets.coingecko.com/coins/images/825/thumb/binance-coin-logo.png?1547034615",
    },
    {
        "coin": "tether",
        "symbol": "usdt",
        "name": "Tether",
        "image":
        "https://assets.coingecko.com/coins/images/325/thumb/Tether-logo.png?1598003707",
    },
    {
        "coin": "cardano",
        "symbol": "ada",
        "name": "Cardano",
        "image":
        "https://assets.coingecko.com/coins/images/975/thumb/cardano.png?1547034860",
    },
    {
        "coin": "litecoin",
        "symbol": "ltc",
        "name": "Litecoin",
        "image":
        "https://assets.coingecko.com/coins/images/2/thumb/litecoin.png?1547033580",
    },
    {
        "coin": "stellar",
        "symbol": "xlm",
        "name": "Stellar",
        "image":
        "https://assets.coingecko.com/coins/images/100/thumb/Stellar_symbol_black_RGB.png?1552356157",
    },
    {
        "coin": "usd-coin",
        "symbol": "usdc",
        "name": "USD Coin",
        "image":
        "https://assets.coingecko.com/coins/images/6319/thumb/USD_Coin_icon.png?1547042389",
    },
    {
        "coin": "eos",
        "symbol": "eos",
        "name": "EOS",
        "image":
        "https://assets.coingecko.com/coins/images/738/thumb/eos-eos-logo.png?1547034481",
    },
    {
        "coin": "monero",
        "symbol": "xmr",
        "name": "Monero",
        "image":
        "https://assets.coingecko.com/coins/images/69/thumb/monero_logo.png?1547033729",
    },
    {
        "coin": "binance-usd",
        "symbol": "busd",
        "name": "Binance USD",
        "image":
        "https://assets.coingecko.com/coins/images/9576/thumb/BUSD.png?1568947766",
    },
    {
        "coin": "tezos",
        "symbol": "xtz",
        "name": "Tezos",
        "image":
        "https://assets.coingecko.com/coins/images/976/thumb/Tezos-logo.png?1547034862",
    },
    {
        "coin": "neo",
        "symbol": "neo",
        "name": "NEO",
        "image":
        "https://assets.coingecko.com/coins/images/480/thumb/NEO_512_512.png?1594357361",
    },
    {
        "coin": "nem",
        "symbol": "xem",
        "name": "NEM",
        "image":
        "https://assets.coingecko.com/coins/images/242/thumb/NEM_Logo_256x256.png?1598687029",
    },
    {
        "coin": "zilliqa",
        "symbol": "zil",
        "name": "Zilliqa",
        "image":
        "https://assets.coingecko.com/coins/images/2687/thumb/Zilliqa-logo.png?1547036894",
    },
    {
        "coin": "icon",
        "symbol": "icx",
        "name": "ICON",
        "image":
        "https://assets.coingecko.com/coins/images/1060/thumb/icon-icx-logo.png?1547035003",
    },
    {
        "coin": "true-usd",
        "symbol": "tusd",
        "name": "TrueUSD",
        "image":
        "https://assets.coingecko.com/coins/images/3449/thumb/TUSD.png?1559172762",
    },
    {
        "coin": "dash",
        "symbol": "dash",
        "name": "Dash",
        "image":
        "https://assets.coingecko.com/coins/images/19/thumb/dash-logo.png?1548385930",
    },
    {
        "coin": "decred",
        "symbol": "dcr",
        "name": "Decred",
        "image":
        "https://assets.coingecko.com/coins/images/329/thumb/decred.png?1547034093",
    },
]

def coins():
    for item in coinsListArr:
        session = current_app.db.session

        newItem = Coins_List(coin=item["coin"], symbol=item["symbol"], name=item["name"], image=item["image"])

        session.add(newItem)
        session.commit()

