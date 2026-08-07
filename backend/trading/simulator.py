from database.connection import SessionLocal
from database.models import Position, Account, TradeHistory


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

            print(
                "ACCOUNT LOADED:",
                round(self.balance, 2)
            )

        finally:
            db.close()


    def save_balance(self):
        db = SessionLocal()

        try:
            account = db.query(Account).first()

            if account:
                account.balance = round(self.balance, 2)

            db.commit()

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
                    self.position
                )

        finally:
            db.close()



    def buy(self, symbol, price, amount):

        print("===== BUY DEBUG =====")
        print("SYMBOL:", symbol)
        print("PRICE:", price)
        print("CAPITAL:", amount)
        print("BALANCE BEFORE:", self.balance)


        if amount > self.balance:
            return "NOT ENOUGH BALANCE"


        crypto_amount = amount / price

        self.position = crypto_amount
        self.balance -= amount
        self.entry_price = price
        self.symbol = symbol


        db = SessionLocal()

        try:

            position = Position(
                symbol=symbol,
                entry_price=price,
                amount=crypto_amount,
                capital_used=amount,
                status="OPEN"
            )

            db.add(position)


            trade = TradeHistory(
                symbol=symbol,
                action="BUY",
                entry_price=price,
                exit_price=0,
                amount=crypto_amount,
                capital_used=amount,
                profit=0,
                reason="ENTRY"
            )

            db.add(trade)

            db.commit()


        finally:
            db.close()


        self.save_balance()


        print(
            "BUY SAVED:",
            symbol,
            "BALANCE:",
            round(self.balance,2)
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


        try:

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


            trade = TradeHistory(
                symbol=self.symbol,
                action="SELL",
                entry_price=self.entry_price,
                exit_price=price,
                amount=self.position,
                capital_used=(
                    self.position * self.entry_price
                ),
                profit=round(profit,2),
                reason=reason
            )


            db.add(trade)

            db.commit()


        finally:
            db.close()


        self.save_balance()


        print(
            "SELL SAVED:",
            self.symbol,
            "BALANCE:",
            round(self.balance,2),
            "PROFIT:",
            round(profit,2)
        )


        self.history.append(
            {
                "action":"SELL",
                "symbol":self.symbol,
                "profit":round(profit,2)
            }
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