from trading.simulator import TradingSimulator


class Backtester:

    def __init__(self, starting_balance=1000):

        self.starting_balance = starting_balance


    def run(self, prices, ai):

        simulator = TradingSimulator(
            balance=self.starting_balance
        )


        for price in prices:

            decision = ai(price)


            if decision == "BUY":

                simulator.buy(price)


            elif decision == "SELL":

                simulator.sell(price)


        return simulator.status(prices[-1])