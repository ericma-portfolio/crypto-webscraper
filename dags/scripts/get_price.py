import sys
from requests import Request, Session
import json
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_price():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    # get top 10 currencies based by market cap
    parameters = {"start": "1", "limit": "10", "convert": "USD"}

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": os.getenv("COIN_MARKET_CAP_API"),
    }

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    # return coins in json format
    coins = json.loads(response.text)["data"]

    price = []

    for coin in coins:

        data = coin["symbol"], coin["quote"]["USD"]["price"]
        
        
        price.append(data)

    return price


get_price()
