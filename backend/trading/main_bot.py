from market.market_manager import MarketManager
from trading.simulator import Simulator
from ai_engine.decision_engine import DecisionEngine


class AlphaAI:

    def __init__(self, balance=1000):

        self.market_manager = MarketManager()
        self.simulator = Simulator(balance)
        self.decision_engine = DecisionEngine()


    def run(self, symbols):

        markets = self.market_manager.get_live_markets(symbols)

        analysis = self.market_manager.scan_markets(markets)


        decision = self.decision_engine.decide(
            analysis,
            self.simulator.balance
        )


        if decision["action"] == "BUY":

            price = markets[0]["prices"][-1]

            self.simulator.buy(
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