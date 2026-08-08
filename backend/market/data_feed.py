import requests
class MarketData:
    def __init__(self):
        self.url = "https://api.binance.com/api/v3/klines"
    def get_candles(
        self,
        symbol="BTCUSDT",
        limit=100
    ):
        params = {
            "symbol": symbol.upper(),
            "interval": "1h",
            "limit": limit
        }
        try:
            response = requests.get(
                self.url,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(
                "BINANCE API ERROR:",
                symbol,
                e
            )
            return []
        except ValueError as e:
            print(
                "BINANCE JSON ERROR:",
                symbol,
                e
            )
            return []
        candles = []
        for candle in data:
            try:
                candles.append({
                    "open": float(candle[1]),
                    "high": float(candle[2]),
                    "low": float(candle[3]),
                    "close": float(candle[4]),
                    "volume": float(candle[5])
                })
            except (
                IndexError,
                TypeError,
                ValueError
            ) as e:
                print(
                    "CANDLE ERROR:",
                    symbol,
                    e
                )
                continue
        return candles