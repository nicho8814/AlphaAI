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


        if self.simulator.position > 0:
         symbol = self.simulator.symbol
        else:
            symbol = decision.get("symbol")

        price = None


        for market in markets:

            if market["symbol"] == symbol:

                price = market["prices"][-1]
                break


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



        # Se abbiamo una posizione aperta controlliamo rischio

        if self.simulator.position > 0:
            print(
            "POSITION DEBUG:",
            "SYMBOL:", self.simulator.symbol,
            "ENTRY:", self.simulator.entry_price,
            "CURRENT:", price
            )

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



        # Compra solo senza posizione

        elif decision.get("action") == "BUY":


            self.simulator.buy(
                decision["symbol"],
                price,
                decision.get("amount", 0)
            )


            decision["price"] = price



        return {

            "analysis": analysis,
            "decision": decision,
            "history": self.simulator.history,
            "balance": self.simulator.balance

        }