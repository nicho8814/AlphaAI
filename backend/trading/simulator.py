from database.connection import SessionLocal
from database.models import Position, Account


class Simulator:

    def __init__(self, balance=1000):

        self.balance = balance
        self.position = 0
        self.entry_price = 0
        self.symbol = None
        self.history = []

        self.load_account()
        self.load_position()


    def load_account(self):

        db = SessionLocal()

        try:
            account = db.query(Account).first()

            if account:
                self.balance = account.balance
                print("ACCOUNT DEBUG BALANCE:", self.balance)

            else:
                account = Account(
                    balance=self.balance
                )

                db.add(account)
                db.commit()

                print("ACCOUNT CREATED:", self.balance)

        finally:
            db.close()



    def save_balance(self):

        db = SessionLocal()

        try:
            account = db.query(Account).first()

            if account:
                account.balance = self.balance

            else:
                account = Account(
                    balance=self.balance
                )

                db.add(account)

            db.commit()

            print("BALANCE SAVED:", self.balance)

        finally:
            db.close()



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

                print(
                    "POSITION LOADED:",
                    self.symbol,
                    self.entry_price
                )

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


        self.save_balance()


        print(
            "BUY SAVED:",
            symbol,
            "BALANCE:",
            self.balance
        )


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


        self.save_balance()


        print(
            "SELL SAVED:",
            self.symbol,
            "BALANCE:",
            self.balance
        )


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