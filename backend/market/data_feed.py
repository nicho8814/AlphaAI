import requests


class MarketData:


    def __init__(self):

        self.url = "https://api.binance.com/api/v3/klines"



    def get_candles(self, symbol="BTCUSDT", limit=100):

        params = {
            "symbol": symbol.upper(),
            "interval": "1h",
            "limit": limit
        }


        response = requests.get(
            self.url,
            params=params
        )


        data = response.json()


        candles = []


        for candle in data:

            candles.append({

                "open": float(candle[1]),

                "high": float(candle[2]),

                "low": float(candle[3]),

                "close": float(candle[4]),

                "volume": float(candle[5])

            })


        return candles