from market.market_manager import MarketManager
from ai_engine.decision_engine import DecisionEngine
from trading.simulator import Simulator


class AlphaAI:

    def __init__(self, balance=1000):

        self.market = MarketManager()
        self.decision = DecisionEngine()
        self.simulator = Simulator(balance)


    def run(self, markets):

        # Analizza tutte le crypto
        analysis = self.market.scan_markets(markets)


        # Decide quale crypto tradare
        decision = self.decision.decide(
            analysis,
            self.simulator.balance
        )


        # Se decide di comprare
        if decision["action"] == "BUY":

            selected_market = next(
                m for m in markets
                if m["symbol"] == decision["symbol"]
            )

            current_price = selected_market["prices"][-1]


            self.simulator.buy(
                current_price,
                decision["amount"]
            )


        return {
            "analysis": analysis,
            "decision": decision,
            "history": self.simulator.history,
            "balance": self.simulator.balance
        }