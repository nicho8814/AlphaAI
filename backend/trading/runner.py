import time

from trading.main_bot import AlphaAI
from database.logger import Logger
from notifications.telegram_bot import TelegramBot


bot = AlphaAI(1000)

logger = Logger()

telegram = TelegramBot()

symbols = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "AVAXUSDT",
    "LINKUSDT",
    "DOGEUSDT",
    "SUIUSDT"
]


last_signal = None


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


        current_signal = (
            decision.get("action"),
            decision.get("symbol")
        )


        # Telegram solo per nuovi segnali
        if (
            decision.get("action") in ["BUY", "SELL"]
            and current_signal != last_signal
        ):

            message = f"""
AlphaAI SIGNAL

Action: {decision.get('action')}
Symbol: {decision.get('symbol')}
Score: {decision.get('score')}
Confidence: {decision.get('confidence', 'N/A')}

Balance: {result['balance']}
"""


            telegram.send_message(message)

            last_signal = current_signal

            print("Telegram signal sent")


        else:

            print("No new signal - Telegram skipped")


    except Exception as e:

        print("ERROR:", e)


    time.sleep(10)