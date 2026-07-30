from trading.simulator import TradingSimulator


class Backtester:

    def __init__(self, starting_balance=1000):

        self.starting_balance = starting_balance


    def run(self, prices, strategy):

        simulator = TradingSimulator(
            balance=self.starting_balance
        )


        for price_data in prices:

            decision = strategy.decide(
                price_data["rsi"],
                price_data["price"],
                price_data["average"]
            )

            price = price_data["price"]


            if decision == "BUY":

                simulator.buy(price)


            elif decision == "SELL":

                simulator.sell(price)



        result = simulator.status(
            prices[-1]["price"]
        )


        trades = result["history"]


        sells = [
            trade for trade in trades
            if trade["action"] == "SELL"
        ]


        wins = [
            trade for trade in sells
            if trade.get("profit", 0) > 0
        ]


        losses = [
            trade for trade in sells
            if trade.get("profit", 0) <= 0
        ]


        total_trades = len(sells)


        win_rate = 0

        if total_trades > 0:

            win_rate = (
                len(wins) / total_trades
            ) * 100



        result["statistics"] = {

            "total_trades": total_trades,

            "winning_trades": len(wins),

            "losing_trades": len(losses),

            "win_rate": round(win_rate, 2)

        }


        return result