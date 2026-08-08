class TechnicalIndicators:
    def calculate_rsi(self, prices, period=14):
        if len(prices) < period + 1:
            return 50
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
        average_gain = sum(
            gains[-period:]
        ) / period
        average_loss = sum(
            losses[-period:]
        ) / period
        # Nessuna perdita = RSI massimo
        if average_loss == 0:
            return 100
        rs = average_gain / average_loss
        rsi_value = 100 - (
            100 / (1 + rs)
        )
        return round(rsi_value, 2)
    def calculate_trend(self, prices):
        if len(prices) < 5:
            return "SIDEWAYS"
        old_price = prices[-5]
        current_price = prices[-1]
        if old_price == 0:
            return "SIDEWAYS"
        change = (
            (current_price - old_price)
            / old_price
        ) * 100
        if change > 0.5:
            return "UP"
        elif change < -0.5:
            return "DOWN"
        else:
            return "SIDEWAYS"
    def calculate_volume(self, volumes):
        if len(volumes) < 2:
            return "LOW"
        previous_volumes = volumes[:-1]
        if not previous_volumes:
            return "LOW"
        avg_volume = (
            sum(previous_volumes)
            / len(previous_volumes)
        )
        current_volume = volumes[-1]
        if current_volume > avg_volume * 1.5:
            return "HIGH"
        elif current_volume > avg_volume:
            return "MEDIUM"
        else:
            return "LOW"