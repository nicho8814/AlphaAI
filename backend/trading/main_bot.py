from market.market_manager import MarketManager
from trading.simulator import Simulator
from ai_engine.decision_engine import DecisionEngine


class AlphaAI:

    def __init__(self, balance=1000):

        self.market_manager = MarketManager()
        self.simulator = Simulator(balance)
        self.decision_engine = DecisionEngine()


    def run(self, symbols):

        print("DEBUG POSITION:", self.simulator.position)
        print("DEBUG SYMBOL:", self.simulator.symbol)


        markets = self.market_manager.get_live_markets(symbols)

        analysis = self.market_manager.scan_markets(markets)


        decision = self.decision_engine.decide(
            analysis,
            self.simulator.balance
        )


        symbol = decision.get("symbol")

        price = None


        for market in markets:

            if market["symbol"] == symbol:

                price = market["prices"][-1]
                break


        # PREZZO NON TROVATO

        if price is None:

            return {
                "analysis": analysis,
                "decision": {
                    "action": "HOLD",
                    "reason": "Prezzo non trovato"
                },
                "history": self.simulator.history,
                "balance": self.simulator.balance
            }



        # GESTIONE POSIZIONE APERTA

        if self.simulator.position > 0:


            change = (
                (price - self.simulator.entry_price)
                / self.simulator.entry_price
            ) * 100


            print("\n===== OPEN POSITION =====")
            print("Symbol:", self.simulator.symbol)
            print("Entry:", round(self.simulator.entry_price, 4))
            print("Current:", round(price, 4))
            print("P/L:", round(change, 2), "%")

            risk = self.simulator.check_risk(price)

            print("Risk:", risk if risk else "NONE")
            print("=========================")


            risk = self.simulator.check_risk(price)


            if risk:


                old_symbol = self.simulator.symbol


                self.simulator.sell(
                    price,
                    risk
                )


                decision = {

                    "action": "SELL",
                    "symbol": old_symbol,
                    "reason": risk,
                    "score": None

                }


            else:


                decision = {

                    "action": "HOLD",
                    "symbol": self.simulator.symbol,
                    "reason": "Posizione aperta"

                }



        # APERTURA NUOVA POSIZIONE

        elif decision.get("action") == "BUY":


            amount = decision.get(
                "amount",
                0
            )


            self.simulator.buy(
                decision["symbol"],
                price,
                amount
            )


            decision["price"] = price



        return {

            "analysis": analysis,
            "decision": decision,
            "history": self.simulator.history,
            "balance": self.simulator.balance

        }