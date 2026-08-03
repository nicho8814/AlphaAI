from indicators.technical import TechnicalIndicators


class MarketScanner:

    def __init__(self):

        self.technical = TechnicalIndicators()


    def calculate_score(self, rsi, trend, volume):

        score = 0


        # RSI
        if 35 < rsi < 55:
            score += 30

        elif 55 <= rsi < 70:
            score += 20

        elif rsi < 35:
            score += 10

        else:
            score += 5


        # Trend
        if trend == "UP":
            score += 40

        elif trend == "SIDEWAYS":
            score += 10

        elif trend == "DOWN":
            score -= 30


        # Volume
        if volume == "HIGH":
            score += 30

        elif volume == "MEDIUM":
            score += 15

        elif volume == "LOW":
            score -= 10


        if score < 0:
            score = 0


        return score



    def analyze_market(self, symbol, prices, volumes):

        rsi = self.technical.calculate_rsi(prices)

        trend = self.technical.calculate_trend(prices)

        volume = self.technical.calculate_volume(volumes)


        score = self.calculate_score(
            rsi,
            trend,
            volume
        )


        return {
            "symbol": symbol,
            "rsi": rsi,
            "trend": trend,
            "volume": volume,
            "score": score
        }



    def scan(self, markets):

        results = []


        for market in markets:

            result = self.analyze_market(
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