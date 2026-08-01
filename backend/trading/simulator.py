class Simulator:

    def __init__(self, balance=1000):

        self.balance = balance
        self.position = 0
        self.entry_price = 0
        self.history = []


    def buy(self, price, amount):

        if amount > self.balance:
            return "NOT ENOUGH BALANCE"


        self.position = amount / price
        self.balance -= amount
        self.entry_price = price


        self.history.append({
            "action": "BUY",
            "price": price,
            "amount": self.position,
            "capital_used": amount
        })


        return "BUY executed"



    def sell(self, price, reason="STRATEGY"):

        if self.position == 0:
            return "NO POSITION"


        value = self.position * price

        profit = value - (self.position * self.entry_price)


        self.balance += value


        self.history.append({
            "action": "SELL",
            "price": price,
            "reason": reason,
            "profit": round(profit, 2)
        })


        self.position = 0
        self.entry_price = 0


        return "SELL executed"



    def check_risk(self, price):

        if self.entry_price == 0:
            return None


        change = (price - self.entry_price) / self.entry_price


        if change <= -0.02:
            return "STOP_LOSS"


        if change >= 0.05:
            return "TAKE_PROFIT"


        return None