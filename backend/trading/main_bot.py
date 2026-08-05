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


        # prende il prezzo della crypto scelta
        selected_symbol = decision.get("symbol")

        price = None


        for market in markets:

            if market["symbol"] == selected_symbol:

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



        # gestione posizione aperta

        if self.simulator.position > 0:


            risk = self.simulator.check_risk(price)


            if risk == "STOP_LOSS":

                self.simulator.sell(
                    price,
                    "STOP_LOSS"
                )


            elif risk == "TAKE_PROFIT":

                self.simulator.sell(
                    price,
                    "TAKE_PROFIT"
                )



        # nuovo BUY solo se non possiede crypto

        elif (
            decision["action"] == "BUY"
            and self.simulator.position == 0
        ):


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