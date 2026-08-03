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


        logger.save(result)


        decision = result["decision"]


        # Invia Telegram solo per segnali importanti
        if decision["action"] in ["BUY", "SELL"]:

            message = f"""
🤖 AlphaAI SIGNAL

Action: {decision['action']}
Symbol: {decision['symbol']}
Score: {decision['score']}
Confidence: {decision.get('confidence', 'N/A')}

Balance: {result['balance']}
"""


            telegram.send_message(message)

            print("Telegram signal sent ✅")


        else:

            print("No signal - Telegram skipped")


    except Exception as e:

        print("ERROR:", e)


    time.sleep(10)