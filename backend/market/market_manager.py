from market.scanner import MarketScanner


class MarketManager:

    def __init__(self):
        self.scanner = MarketScanner()


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