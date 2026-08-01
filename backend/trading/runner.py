import time

from trading.main_bot import AlphaAI


bot = AlphaAI(1000)


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


    except Exception as e:

        print("ERROR:", e)


    time.sleep(300)