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
    # =========================================================
    # ACCOUNT
    # =========================================================
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
                account.balance = round(
                    self.balance,
                    2
                )
                db.commit()
        finally:
            db.close()
    # =========================================================
    # POSITION
    # =========================================================
    def load_position(self):
        db = SessionLocal()
        try:
            position = (
                db.query(Position)
                .filter(
                    Position.status == "OPEN"
                )
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
    # =========================================================
    # BUY
    # =========================================================
    def buy(self, symbol, price, amount):
        print("\n===== BUY DEBUG =====")
        print("SYMBOL:", symbol)
        print("PRICE:", price)
        print("CAPITAL:", amount)
        print(
            "BALANCE BEFORE:",
            self.balance
        )
        print("=====================")
        # Controlli di sicurezza
        if price is None or price <= 0:
            return "INVALID PRICE"
        if amount <= 0:
            return "INVALID AMOUNT"
        if amount > self.balance:
            return "NOT ENOUGH BALANCE"
        # Non permettere due posizioni contemporaneamente
        if self.position > 0:
            return "POSITION ALREADY OPEN"
        crypto_amount = amount / price
        # Aggiorna simulatore
        self.position = crypto_amount
        self.balance -= amount
        self.entry_price = price
        self.symbol = symbol
        db = SessionLocal()
        try:
            # Salva posizione
            position = Position(
                symbol=symbol,
                entry_price=price,
                amount=crypto_amount,
                capital_used=amount,
                status="OPEN"
            )
            db.add(position)
            # Salva storico BUY
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
        self.history.append({
            "action": "BUY",
            "symbol": symbol,
            "price": price,
            "amount": crypto_amount,
            "capital": amount,
            "profit": 0,
            "reason": "ENTRY"
        })
        print(
            "BUY SAVED:",
            symbol,
            "BALANCE:",
            round(self.balance, 2)
        )
        return "BUY executed"
    # =========================================================
    # SELL
    # =========================================================
    def sell(
        self,
        price,
        reason="STRATEGY"
    ):
        if self.position <= 0:
            return "NO POSITION"
        if price is None or price <= 0:
            return "INVALID PRICE"
        print("\n===== SELL DEBUG =====")
        print("SYMBOL:", self.symbol)
        print("ENTRY:", self.entry_price)
        print("PRICE:", price)
        print("AMOUNT:", self.position)
        # Valore della posizione al momento della vendita
        value = self.position * price
        # Capitale inizialmente investito
        capital_used = (
            self.position
            * self.entry_price
        )
        # Profitto reale
        profit = value - capital_used
        print(
            "CAPITAL USED:",
            round(capital_used, 2)
        )
        print(
            "SELL VALUE:",
            round(value, 2)
        )
        print(
            "PROFIT:",
            round(profit, 2)
        )
        print("======================")
        # Il capitale ottenuto dalla vendita
        # torna nel balance
        self.balance += value
        db = SessionLocal()
        try:
            # Cerca ESATTAMENTE la posizione aperta
            # appartenente alla crypto venduta
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
            # Salva SELL nello storico
            trade = TradeHistory(
                symbol=self.symbol,
                action="SELL",
                entry_price=self.entry_price,
                exit_price=price,
                amount=self.position,
                capital_used=capital_used,
                profit=round(profit, 2),
                reason=reason
            )
            db.add(trade)
            db.commit()
        finally:
            db.close()
        self.save_balance()
        self.history.append({
            "action": "SELL",
            "symbol": self.symbol,
            "entry_price": self.entry_price,
            "exit_price": price,
            "amount": self.position,
            "capital": capital_used,
            "profit": round(profit, 2),
            "reason": reason
        })
        print(
            "SELL SAVED:",
            self.symbol,
            "BALANCE:",
            round(self.balance, 2),
            "PROFIT:",
            round(profit, 2)
        )
        # Reset posizione in memoria
        self.position = 0
        self.entry_price = 0
        self.symbol = None
        return "SELL executed"
    # =========================================================
    # STOP LOSS / TAKE PROFIT
    # =========================================================
    def check_risk(self, price):
        if self.entry_price == 0:
            return None
        if price is None or price <= 0:
            return None
        change = (
            (price - self.entry_price)
            / self.entry_price
        )
        # STOP LOSS -2%
        if change <= -0.02:
            return "STOP_LOSS"
        # TAKE PROFIT +5%
        if change >= 0.05:
            return "TAKE_PROFIT"
        return None