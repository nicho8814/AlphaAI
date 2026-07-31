class TradingSimulator:

    def __init__(self):
        self.balance = 1000
        self.position = 0
        self.entry_price = 0
        self.history = []

    def buy(self, price):

        if self.balance <= 0:
            return "No balance"

        self.position = self.balance / price
        self.balance = 0
        self.entry_price = price

        self.history.append({
            "action": "BUY",
            "price": price,
            "amount": self.position
        })

        return "BUY executed"


    def sell(self, price):

        if self.position <= 0:
            return "No position"

        self.balance = self.position * price

        profit = self.balance - 1000

        self.history.append({
            "action": "SELL",
            "price": price,
            "profit": round(profit, 2)
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