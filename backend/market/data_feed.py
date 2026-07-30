import random


class MarketData:

    def get_price(self, symbol: str):

        # Simulazione temporanea del mercato
        # (poi lo collegheremo alle API reali)

        price = round(random.uniform(60000, 70000), 2)

        return {
            "symbol": symbol,
            "price": price
        }


    def get_candles(self, symbol: str, limit: int = 100):

        candles = []

        price = self.get_price(symbol)["price"]

        for i in range(limit):

            candles.append({
                "open": price,
                "high": price * 1.01,
                "low": price * 0.99,
                "close": price + random.uniform(-200, 200),
                "volume": random.uniform(10, 100)
            })

        return candles