class MarketScanner:

    def __init__(self):
        self.markets = [
            "BTCUSDT",
            "ETHUSDT",
            "SOLUSDT",
            "BNBUSDT",
            "XRPUSDT"
        ]


    def calculate_score(self, rsi, trend, volume):

        score = 0

        # RSI
        if 30 <= rsi <= 50:
            score += 30
        elif rsi < 30:
            score += 20
        else:
            score += 10


        # Trend
        if trend == "UP":
            score += 40
        elif trend == "SIDEWAYS":
            score += 20


        # Volume
        if volume == "HIGH":
            score += 30
        elif volume == "MEDIUM":
            score += 15


        return score


    def scan(self, data):

        results = []

        for coin in data:

            score = self.calculate_score(
                coin["rsi"],
                coin["trend"],
                coin["volume"]
            )

            results.append({
                "symbol": coin["symbol"],
                "score": score
            })


        results.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return results