from market.market_manager import MarketManager
from trading.simulator import Simulator


class AlphaAI:

    def __init__(self, balance=1000):

        self.market_manager = MarketManager()
        self.simulator = Simulator(balance)


    def run(self, symbols):

        markets = self.market_manager.get_live_markets(symbols)

        analysis = self.market_manager.scan_markets(markets)

        best = analysis[0]


        decision = {
            "action": "HOLD",
            "symbol": best["symbol"],
            "score": best["score"],
            "confidence": "LOW"
        }


        if best["score"] >= 90:

            price = markets[0]["prices"][-1]

            decision = {
                "action": "BUY",
                "symbol": best["symbol"],
                "score": best["score"],
                "confidence": "HIGH",
                "price": price
            }

            self.simulator.buy(price)


        elif best["score"] >= 70:

            decision["confidence"] = "MEDIUM"


        return {

            "analysis": analysis,
            "decision": decision,
            "history": self.simulator.history,
            "balance": self.simulator.balance

        }