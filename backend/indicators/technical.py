class TechnicalIndicators:

    def calculate_rsi(self, prices, period=14):
        gains = []
        losses = []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]

            if change >= 0:
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
        rsi = 100 - (100 / (1 + rs))

        return round(rsi, 2)


    def calculate_trend(self, prices):

        if prices[-1] > prices[-5]:
            return "UP"

        elif prices[-1] < prices[-5]:
            return "DOWN"

        return "SIDEWAYS"


    def calculate_volume(self, volumes):

        avg = sum(volumes[:-1]) / len(volumes[:-1])

        if volumes[-1] > avg * 1.5:
            return "HIGH"

        elif volumes[-1] > avg:
            return "MEDIUM"

        return "LOW"