class TechnicalIndicators:

    def moving_average(self, prices, period=20):

        if len(prices) < period:
            return None

        return sum(prices[-period:]) / period


    def rsi(self, prices, period=14):

        if len(prices) <= period:
            return None

        gains = []
        losses = []

        for i in range(1, len(prices)):

            change = prices[i] - prices[i - 1]

            if change > 0:
                gains.append(change)
                losses.append(0)

            else:
                gains.append(0)
                losses.append(abs(change))


        average_gain = sum(gains[-period:]) / period
        average_loss = sum(losses[-period:]) / period


        if average_loss == 0:
            return 100


        rs = average_gain / average_loss

        rsi_value = 100 - (100 / (1 + rs))

        return round(rsi_value, 2)