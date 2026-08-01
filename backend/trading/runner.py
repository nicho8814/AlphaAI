import time

from trading.main_bot import AlphaAI
from database.logger import Logger


bot = AlphaAI(1000)

logger = Logger()


symbols = [
    "BTCUSDT",
    "SOLUSDT"
]


while True:

    try:

        result = bot.run(symbols)


        print("\n===== AlphaAI =====")

        print("Analysis:")
        print(result["analysis"])


        print("\nDecision:")
        print(result["decision"])


        print("\nBalance:")
        print(result["balance"])


        print("===================\n")


        logger.save(result)


        print("Saved to log ✅")


    except Exception as e:

        print("ERROR:", e)


    time.sleep(10)