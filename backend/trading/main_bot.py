from market.market_manager import MarketManager
from trading.simulator import Simulator
from ai_engine.decision_engine import DecisionEngine


class AlphaAI:

    def __init__(self, balance=1000):

        self.market_manager = MarketManager()
        self.simulator = Simulator(balance)
        self.decision_engine = DecisionEngine()


    def run(self, symbols):

        print(
            "DEBUG POSITION:",
            self.simulator.position
        )

        print(
            "DEBUG SYMBOL:",
            self.simulator.symbol
        )


        markets = self.market_manager.get_live_markets(symbols)

        analysis = self.market_manager.scan_markets(markets)


        decision = self.decision_engine.decide(
            analysis,
            self.simulator.balance
        )


        # PREZZO DELLA DECISIONE AI (solo per BUY)

        decision_symbol = decision.get("symbol")

        buy_price = None


        for market in markets:

            if market["symbol"] == decision_symbol:

                buy_price = market["prices"][-1]

                break



        # GESTIONE POSIZIONE APERTA

        if self.simulator.position > 0:


            current_price = None


            # CERCA IL PREZZO DELLA POSIZIONE APERTA
            for market in markets:

                if market["symbol"] == self.simulator.symbol:

                    current_price = market["prices"][-1]

                    break



            if current_price is None:

                return {
                    "decision": {
                        "action": "HOLD",
                        "reason": "Prezzo posizione non trovato"
                    },
                    "balance": self.simulator.balance
                }



            change = (
                (current_price - self.simulator.entry_price)
                /
                self.simulator.entry_price
            ) * 100



            print("\n===== OPEN POSITION =====")

            print(
                "Symbol:",
                self.simulator.symbol
            )

            print(
                "Entry:",
                round(self.simulator.entry_price,4)
            )

            print(
                "Current:",
                round(current_price,4)
            )

            print(
                "P/L:",
                round(change,2),
                "%"
            )



            risk = self.simulator.check_risk(current_price)


            print(
                "Risk:",
                risk if risk else "NONE"
            )



            if risk:


                old_symbol = self.simulator.symbol


                self.simulator.sell(
                    current_price,
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
                buy_price,
                amount
            )


            decision["price"] = buy_price




        return {

            "analysis": analysis,

            "decision": decision,

            "history": self.simulator.history,

            "balance": round(
                self.simulator.balance,
                2
            )

        }