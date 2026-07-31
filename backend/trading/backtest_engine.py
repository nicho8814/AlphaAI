from indicators.technical import TechnicalIndicators
from trading.backtester import Backtester
from trading.strategy import AlphaStrategy


class BacktestEngine:

    def run(self, candles):

        prices = [
            candle["close"]
            for candle in candles
        ]

        indicators = TechnicalIndicators()

        dataset = []

        for i in range(len(prices)):

            if i < 20:
                continue

            history = prices[:i+1]

            rsi = indicators.rsi(history)

            average = indicators.moving_average(history)

            dataset.append({
                "price": prices[i],
                "rsi": rsi,
                "average": average
            })


        tester = Backtester()

        strategy = AlphaStrategy()

        result = tester.run(
            dataset,
            strategy
        )

        return result
