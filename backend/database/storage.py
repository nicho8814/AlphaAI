import json
import os


FILE = "database/trades.json"


class TradeStorage:

    def __init__(self):

        if not os.path.exists(FILE):

            with open(FILE, "w") as f:
                json.dump([], f)


    def save_trade(self, trade):

        with open(FILE, "r") as f:
            trades = json.load(f)

        trades.append(trade)

        with open(FILE, "w") as f:
            json.dump(trades, f, indent=4)


    def get_trades(self):

        with open(FILE, "r") as f:
            return json.load(f)