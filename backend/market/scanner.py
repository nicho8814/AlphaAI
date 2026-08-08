from indicators.technical import TechnicalIndicators


class MarketScanner:

    def __init__(self):
        self.technical = TechnicalIndicators()

    def calculate_score(self, rsi, trend, volume):

        score = 0

        # =========================
        # RSI
        # =========================

        if 40 <= rsi <= 60:
            score += 35

        elif 30 <= rsi < 40:
            score += 25

        elif 60 < rsi <= 70:
            score += 25

        else:
            score += 10


        # =========================
        # TREND
        # =========================

        if trend == "UP":
            score += 40

        elif trend == "SIDEWAYS":
            score += 15

        elif trend == "DOWN":
            score -= 20


        # =========================
        # VOLUME
        # =========================

        if volume == "HIGH":
            score += 25

        elif volume == "MEDIUM":
            score += 15

        elif volume == "LOW":
            score += 5


        # Non permettere score negativi
        return max(score, 0)


    def analyze_market(self, symbol, prices, volumes):

        try:

            rsi = self.technical.calculate_rsi(prices)

            trend = self.technical.calculate_trend(
                prices
            )

            volume = self.technical.calculate_volume(
                volumes
            )

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

        except Exception as e:

            print(
                "ANALYSIS ERROR:",
                symbol,
                e
            )

            return {
                "symbol": symbol,
                "rsi": None,
                "trend": "UNKNOWN",
                "volume": "UNKNOWN",
                "score": 0
            }