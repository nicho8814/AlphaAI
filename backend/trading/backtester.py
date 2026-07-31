from trading.simulator import TradingSimulator


class Backtester:

    def run(self, prices, strategy):

        simulator = TradingSimulator()

        for price_data in prices:

            price = price_data["price"]

            risk = simulator.check_risk(price)

            if risk == "STOP_LOSS" or risk == "TAKE_PROFIT":
                simulator.sell(price)
                continue

            decision = strategy.decide(
                price_data["price"],
                price_data["rsi"],
                price_data["average"]
            )

            if decision == "BUY":
                simulator.buy(price)

            elif decision == "SELL":
                simulator.sell(price)

        sells = [
            trade for trade in simulator.history
            if trade["action"] == "SELL"
        ]

        total_trades = len(sells)

        winning_trades = [
            trade for trade in sells
            if trade.get("profit", 0) > 0
        ]

        losing_trades = [
            trade for trade in sells
            if trade.get("profit", 0) <= 0
        ]

        win_rate = 0

        if total_trades > 0:
            win_rate = (len(winning_trades) / total_trades) * 100

        return {
            "balance": simulator.balance,
            "position": simulator.position,
            "history": simulator.history,
            "statistics": {
                "total_trades": total_trades,
                "winning_trades": len(winning_trades),
                "losing_trades": len(losing_trades),
                "win_rate": round(win_rate, 2)
            }
        }