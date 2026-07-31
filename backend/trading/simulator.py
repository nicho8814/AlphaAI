class TradingSimulator:

    def __init__(self):
        self.balance = 1000
        self.position = 0
        self.entry_price = 0
        self.history = []


    def buy(self, price):

        if self.balance <= 0:
            return "No balance"

        risk_per_trade = 0.20  # usa il 20% del capitale disponibile

        amount_to_use = self.balance * risk_per_trade

        self.position = amount_to_use / price
        self.balance -= amount_to_use
        self.entry_price = price

        self.history.append({
            "action": "BUY",
            "price": price,
            "amount": self.position
        })

        return "BUY executed"


    def sell(self, price, reason="STRATEGY"):

        if self.position <= 0:
            return "No position"

        value = self.position * price

        profit = value - (self.position * self.entry_price)

        self.balance += value

        self.history.append({
            "action": "SELL",
            "price": price,
            "profit": round(profit, 2),
            "reason": reason
        })

        self.position = 0
        self.entry_price = 0

        return "SELL executed"


    def check_risk(self, price):

        if self.position <= 0:
            return None

        change = (price - self.entry_price) / self.entry_price

        if change <= -0.02:
            return "STOP_LOSS"

        if change >= 0.05:
            return "TAKE_PROFIT"

        return None