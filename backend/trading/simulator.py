class Simulator:

    def __init__(self, balance=1000):
        self.balance = balance
        self.position = 0
        self.entry_price = 0
        self.entry_amount = 0
        self.history = []


    def buy(self, price, amount):

        if amount > self.balance:
            return "Not enough balance"


        quantity = amount / price

        self.position = quantity
        self.entry_price = price
        self.entry_amount = amount

        self.balance -= amount


        self.history.append({
            "action": "BUY",
            "price": price,
            "amount": quantity,
            "capital_used": amount
        })


        return "BUY executed"



    def sell(self, price, reason="STRATEGY"):

        if self.position <= 0:
            return "No position"


        value = self.position * price

        profit = value - self.entry_amount


        self.balance += value
        self.position = 0
        self.entry_price = 0
        self.entry_amount = 0


        self.history.append({
            "action": "SELL",
            "price": price,
            "profit": round(profit, 2),
            "reason": reason
        })


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