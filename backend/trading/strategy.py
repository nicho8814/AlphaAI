class AlphaStrategy:

    def decide(self, price, rsi, average):

        if rsi < 30 and price < average:
            return "BUY"

        elif rsi > 70 and price > average:
            return "SELL"

        else:
            return "HOLD"