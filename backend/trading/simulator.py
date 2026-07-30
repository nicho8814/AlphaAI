from database.storage import TradeStorage


class TradingSimulator:

    def __init__(self, balance=1000):

        self.balance = balance
        self.position = 0
        self.entry_price = 0
        self.history = []

        self.storage = TradeStorage()


    def buy(self, price):

        if self.balance <= 0:
            return "No balance"


        self.position = self.balance / price
        self.entry_price = price
        self.balance = 0


        trade = {
            "action": "BUY",
            "price": price,
            "amount": self.position
        }


        self.history.append(trade)
        self.storage.save_trade(trade)


        return "BUY executed"



    def sell(self, price):

        if self.position <= 0:
            return "No position"


        self.balance = self.position * price

        profit = self.balance - 1000


        trade = {
            "action": "SELL",
            "price": price,
            "profit": round(profit, 2)
        }


        self.history.append(trade)
        self.storage.save_trade(trade)


        self.position = 0


        return "SELL executed"



    def status(self, current_price):

        total = self.balance


        if self.position > 0:
            total += self.position * current_price


        return {
            "balance": round(self.balance, 2),
            "position": round(self.position, 6),
            "portfolio_value": round(total, 2),
            "history": self.history
        }