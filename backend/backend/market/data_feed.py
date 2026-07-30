import requests
from datetime import datetime


class MarketData:

    def __init__(self):
        self.url = (
            "https://api.crypto.com/"
            "v2/public/get-ticker"
        )


    def get_price(self, symbol="BTC_USDT"):

        params = {
            "instrument_name": symbol
        }

        response = requests.get(
            self.url,
            params=params
        )

        data = response.json()

        ticker = data["result"]["data"][0]

        return {
            "symbol": symbol,
            "price": float(ticker["a"]),
            "time": datetime.now().isoformat()
        }
