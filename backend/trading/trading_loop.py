from ai_engine.decision_engine import DecisionEngine
from trading.simulator import Simulator


class TradingLoop:

    def __init__(self, balance=1000):
        self.engine = DecisionEngine()
        self.simulator = Simulator(balance)


    def run_once(self, market_data, price):

        decision = self.engine.decide(
            market_data,
            self.simulator.balance
        )


        if decision["action"] == "BUY":

            self.simulator.buy(
                price,
                decision["amount"]
            )


        risk = self.simulator.check_risk(price)


        if risk:

            self.simulator.sell(
                price,
                risk
            )


        return {
            "decision": decision,
            "history": self.simulator.history,
            "balance": self.simulator.balance
        }