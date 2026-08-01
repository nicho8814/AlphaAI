from market.scanner import MarketScanner
from market.data_feed import MarketData


class MarketManager:

    def __init__(self):

        self.scanner = MarketScanner()
        self.data = MarketData()


    def scan_markets(self, markets):

        results = []

        for market in markets:

            result = self.scanner.analyze_market(
                market["symbol"],
                market["prices"],
                market["volumes"]
            )

            results.append(result)


        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results



    def get_live_markets(self, symbols):

        markets = []

        for symbol in symbols:

            candles = self.data.get_candles(
                symbol,
                100
            )


            prices = [
                candle["close"]
                for candle in candles
            ]


            volumes = [
                candle["volume"]
                for candle in candles
            ]


            markets.append({

                "symbol": symbol,
                "prices": prices,
                "volumes": volumes

            })


        return markets