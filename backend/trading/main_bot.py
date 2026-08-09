from datetime import datetime, timedelta
from database.connection import SessionLocal
from database.models import TradeHistory
from market.market_manager import MarketManager
from trading.simulator import Simulator
from ai_engine.decision_engine import DecisionEngine
class AlphaAI:
    # Dopo un SELL, la stessa moneta non può essere
    # ricomprata immediatamente.
    COOLDOWN_MINUTES = 180
    # Per cambiare moneta, la nuova opportunità deve
    # avere almeno 10 punti di score in più.
    SWITCH_SCORE_GAP = 10
    def __init__(self, balance=1000):
        self.market_manager = MarketManager()
        self.simulator = Simulator(balance)
        self.decision_engine = DecisionEngine()
    # =========================================================
    # COOLDOWN
    # =========================================================
    def is_in_cooldown(self, symbol):
        db = SessionLocal()
        try:
            last_sell = (
                db.query(TradeHistory)
                .filter(
                    TradeHistory.symbol == symbol,
                    TradeHistory.action == "SELL"
                )
                .order_by(
                    TradeHistory.created_at.desc()
                )
                .first()
            )
            if not last_sell:
                return False
            if not last_sell.created_at:
                return False
            cooldown_until = (
                last_sell.created_at
                + timedelta(
                    minutes=self.COOLDOWN_MINUTES
                )
            )
            return datetime.utcnow() < cooldown_until
        finally:
            db.close()
    # =========================================================
    # TROVA MIGLIORE OPPORTUNITÀ
    # =========================================================
    def get_best_available_coin(self, analysis):
        available = []
        for coin in analysis:
            symbol = coin.get("symbol")
            if not symbol:
                continue
            if self.is_in_cooldown(symbol):
                continue
            available.append(coin)
        if not available:
            return None
        return max(
            available,
            key=lambda coin: coin.get("score", 0)
        )
    # =========================================================
    # RUN
    # =========================================================
    def run(self, symbols):
        print(
            "DEBUG POSITION:",
            self.simulator.position
        )
        print(
            "DEBUG SYMBOL:",
            self.simulator.symbol
        )
        # =====================================================
        # MARKET DATA
        # =====================================================
        markets = (
            self.market_manager
            .get_live_markets(symbols)
        )
        if not markets:
            return {
                "analysis": [],
                "decision": {
                    "action": "HOLD",
                    "reason": "Nessun mercato disponibile"
                },
                "history": self.simulator.history,
                "balance": round(
                    self.simulator.balance,
                    2
                )
            }
        analysis = (
            self.market_manager
            .scan_markets(markets)
        )
        # =====================================================
        # POSIZIONE APERTA
        # =====================================================
        if self.simulator.position > 0:
            current_symbol = self.simulator.symbol
            current_price = None
            current_analysis = None
            # -------------------------------------------------
            # PREZZO DELLA POSIZIONE
            # -------------------------------------------------
            for market in markets:
                if market["symbol"] == current_symbol:
                    prices = market.get(
                        "prices",
                        []
                    )
                    if prices:
                        current_price = prices[-1]
                    break
            # -------------------------------------------------
            # ANALISI DELLA POSIZIONE
            # -------------------------------------------------
            for coin in analysis:
                if coin["symbol"] == current_symbol:
                    current_analysis = coin
                    break
            # -------------------------------------------------
            # PREZZO NON TROVATO
            # -------------------------------------------------
            if current_price is None:
                return {
                    "analysis": analysis,
                    "decision": {
                        "action": "HOLD",
                        "symbol": current_symbol,
                        "reason": "Prezzo posizione non trovato"
                    },
                    "history": self.simulator.history,
                    "balance": round(
                        self.simulator.balance,
                        2
                    )
                }
            # -------------------------------------------------
            # PROFIT / LOSS
            # -------------------------------------------------
            change = (
                (
                    current_price
                    - self.simulator.entry_price
                )
                / self.simulator.entry_price
            ) * 100
            print("\n===== OPEN POSITION =====")
            print(
                "Symbol:",
                current_symbol
            )
            print(
                "Entry:",
                round(
                    self.simulator.entry_price,
                    4
                )
            )
            print(
                "Current:",
                round(
                    current_price,
                    4
                )
            )
            print(
                "P/L:",
                round(change, 2),
                "%"
            )
            # =================================================
            # STOP LOSS / TAKE PROFIT
            # =================================================
            risk = self.simulator.check_risk(
                current_price
            )
            print(
                "Risk:",
                risk if risk else "NONE"
            )
            if risk:
                old_symbol = current_symbol
                sell_result = self.simulator.sell(
                    current_price,
                    risk
                )
                decision = {
                    "action": "SELL",
                    "symbol": old_symbol,
                    "price": current_price,
                    "reason": risk,
                    "result": sell_result,
                    "score": (
                        current_analysis.get("score")
                        if current_analysis
                        else None
                    )
                }
                return {
                    "analysis": analysis,
                    "decision": decision,
                    "history": self.simulator.history,
                    "balance": round(
                        self.simulator.balance,
                        2
                    )
                }
            # =================================================
            # TROVA ALTERNATIVA MIGLIORE
            # =================================================
            best_coin = self.get_best_available_coin(
                analysis
            )
            current_score = (
                current_analysis.get("score", 0)
                if current_analysis
                else 0
            )
            best_score = (
                best_coin.get("score", 0)
                if best_coin
                else 0
            )
            print("\n===== OPPORTUNITY CHECK =====")
            print(
                "CURRENT:",
                current_symbol,
                "SCORE:",
                current_score
            )
            if best_coin:
                print(
                    "BEST:",
                    best_coin["symbol"],
                    "SCORE:",
                    best_score
                )
            else:
                print(
                    "BEST: NONE"
                )
            # =================================================
            # SWITCH
            # =================================================
            if (
                best_coin
                and best_coin["symbol"] != current_symbol
                and best_score
                >= current_score + self.SWITCH_SCORE_GAP
            ):
                new_symbol = best_coin["symbol"]
                new_price = None
                for market in markets:
                    if market["symbol"] == new_symbol:
                        prices = market.get(
                            "prices",
                            []
                        )
                        if prices:
                            new_price = prices[-1]
                        break
                if new_price is None:
                    return {
                        "analysis": analysis,
                        "decision": {
                            "action": "HOLD",
                            "symbol": current_symbol,
                            "reason": (
                                "Alternativa migliore "
                                "senza prezzo disponibile"
                            )
                        },
                        "history": self.simulator.history,
                        "balance": round(
                            self.simulator.balance,
                            2
                        )
                    }
                # ---------------------------------------------
                # SELL VECCHIA POSIZIONE
                # ---------------------------------------------
                old_symbol = current_symbol
                sell_result = self.simulator.sell(
                    current_price,
                    "SWITCH_TO_BETTER"
                )
                print(
                    "SWITCH:",
                    old_symbol,
                    "->",
                    new_symbol
                )
                # BUY NUOVA POSIZIONE
                # La moneta è già stata scelta come migliore:
                # non chiediamo una seconda decisione al DecisionEngine.

                risk = self.decision_engine.risk_manager.calculate_position_size(
                    self.simulator.balance,
                    best_score,
                    best_coin.get("volatility", "MEDIUM")
                )

                amount = risk["amount"]

                print("===== SWITCH BUY DEBUG =====")
                print("NEW SYMBOL:", new_symbol)
                print("NEW PRICE:", new_price)
                print("NEW SCORE:", best_score)
                print("BALANCE AFTER SELL:", self.simulator.balance)
                print("BUY AMOUNT:", amount)

                buy_result = None

                if amount > 0:
                    buy_result = self.simulator.buy(
                        new_symbol,
                        new_price,
                        amount
                    )
                    return {
                        "analysis": analysis,
                        "decision": {
                            "action": "SWITCH",
                            "sell_symbol": old_symbol,
                            "buy_symbol": new_symbol,
                            "sell_price": current_price,
                            "buy_price": new_price,
                            "old_score": current_score,
                            "new_score": best_score,
                            "sell_result": sell_result,
                            "buy_result": buy_result
                        },
                        "history": self.simulator.history,
                        "balance": round(
                            self.simulator.balance,
                            2
                        )
                    }
                return {
                    "analysis": analysis,
                    "decision": {
                        "action": "SELL",
                        "symbol": old_symbol,
                        "price": current_price,
                        "reason": (
                            "Switch eseguito ma "
                            "BUY non disponibile"
                        )
                    },
                    "history": self.simulator.history,
                    "balance": round(
                        self.simulator.balance,
                        2
                    )
                }
            # =================================================
            # NESSUNA OPPORTUNITÀ SUFFICIENTEMENTE MIGLIORE
            # =================================================
            return {
                "analysis": analysis,
                "decision": {
                    "action": "HOLD",
                    "symbol": current_symbol,
                    "price": current_price,
                    "reason": "Posizione aperta",
                    "score": current_score,
                    "best_score": best_score
                },
                "history": self.simulator.history,
                "balance": round(
                    self.simulator.balance,
                    2
                )
            }
        # =====================================================
        # NESSUNA POSIZIONE → CERCA OPPORTUNITÀ
        # =====================================================
        best_coin = self.get_best_available_coin(
            analysis
        )
        if not best_coin:
            return {
                "analysis": analysis,
                "decision": {
                    "action": "HOLD",
                    "reason": "Nessuna opportunità disponibile"
                },
                "history": self.simulator.history,
                "balance": round(
                    self.simulator.balance,
                    2
                )
            }
        # Usiamo il DecisionEngine solo dopo aver
        # filtrato le monete in cooldown.
        decision = self.decision_engine.decide(
            [best_coin],
            self.simulator.balance
        )
        # =====================================================
        # BUY
        # =====================================================
        if decision.get("action") == "BUY":
            symbol = decision.get(
                "symbol"
            )
            buy_price = None
            for market in markets:
                if market["symbol"] == symbol:
                    prices = market.get(
                        "prices",
                        []
                    )
                    if prices:
                        buy_price = prices[-1]
                    break
            if buy_price is None:
                decision = {
                    "action": "HOLD",
                    "symbol": symbol,
                    "reason": "Prezzo BUY non trovato"
                }
            else:
                amount = decision.get(
                    "amount",
                    0
                )
                if amount > 0:
                    buy_result = self.simulator.buy(
                        symbol,
                        buy_price,
                        amount
                    )
                    decision["price"] = buy_price
                    decision["result"] = buy_result
                else:
                    decision = {
                        "action": "HOLD",
                        "symbol": symbol,
                        "price": buy_price,
                        "reason": "Importo BUY non valido"
                    }
        # =====================================================
        # RETURN
        # =====================================================
        return {
            "analysis": analysis,
            "decision": decision,
            "history": self.simulator.history,
            "balance": round(
                self.simulator.balance,
                2
            )
        }