from database.connection import SessionLocal
from database.models import Position


class Simulator:

    def __init__(self, balance=1000):

        self.balance = balance
        self.position = 0
        self.entry_price = 0
        self.symbol = None
        self.history = []

        self.load_position()


    def load_position(self):

        db = SessionLocal()

        try:
            position = (
                db.query(Position)
                .filter(Position.status == "OPEN")
                .first()
            )

            if position:
                self.symbol = position.symbol
                self.entry_price = position.entry_price
                self.position = position.amount

        finally:
            db.close()


    def buy(self, symbol, price, amount):

        if amount > self.balance:
            return "NOT ENOUGH BALANCE"


        self.position = amount / price
        self.balance -= amount
        self.entry_price = price
        self.symbol = symbol


        db = SessionLocal()

        position = Position(
            symbol=symbol,
            entry_price=price,
            amount=self.position,
            capital_used=amount,
            status="OPEN"
        )

        db.add(position)
        db.commit()
        db.close()


        self.history.append({
            "action": "BUY",
            "symbol": symbol,
            "price": price,
            "amount": self.position,
            "capital_used": amount
        })


        return "BUY executed"



    def sell(self, price, reason="STRATEGY"):

        if self.position == 0:
            return "NO POSITION"


        value = self.position * price

        profit = value - (
            self.position * self.entry_price
        )


        self.balance += value


        db = SessionLocal()

        position = (
            db.query(Position)
            .filter(
                Position.symbol == self.symbol,
                Position.status == "OPEN"
            )
            .first()
        )


        if position:
            position.status = "CLOSED"


        db.commit()
        db.close()


        self.history.append({
            "action": "SELL",
            "symbol": self.symbol,
            "price": price,
            "reason": reason,
            "profit": round(profit, 2)
        })


        self.position = 0
        self.entry_price = 0
        self.symbol = None


        return "SELL executed"



    def check_risk(self, price):

        if self.entry_price == 0:
            return None


        change = (
            price - self.entry_price
        ) / self.entry_price


        if change <= -0.02:
            return "STOP_LOSS"


        if change >= 0.05:
            return "TAKE_PROFIT"


        return None