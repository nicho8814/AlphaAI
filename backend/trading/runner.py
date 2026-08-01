import time

from trading.main_bot import AlphaAI
from database.logger import Logger
from notifications.telegram_bot import TelegramBot


bot = AlphaAI(1000)

logger = Logger()

telegram = TelegramBot()


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


        message = f"""
🤖 AlphaAI Update

Decision: {result['decision']['action']}
Symbol: {result['decision']['symbol']}
Score: {result['decision']['score']}

Balance: {result['balance']}
"""


        telegram.send_message(message)


        print("Telegram sent ✅")


    except Exception as e:

        print("ERROR:", e)


    time.sleep(10)