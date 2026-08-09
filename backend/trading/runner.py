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
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "LINKUSDT",
    "SUIUSDT",
    "TRXUSDT",
    "DOTUSDT",
    "LTCUSDT",
    "BCHUSDT",
    "ATOMUSDT",
    "NEARUSDT",
    "APTUSDT",
    "ARBUSDT",
    "OPUSDT",
    "FILUSDT",
    "INJUSDT",
    "TIAUSDT",
    "UNIUSDT",
    "AAVEUSDT",
    "ETCUSDT",
]
while True:
    try:
        result = bot.run(symbols)
        print("\n===== AlphaAI =====")
        print("\nAnalysis:")
        print(result["analysis"])
        print("\nDecision:")
        print(result["decision"])
        print("\nBalance:")
        print(round(result["balance"], 2))
        logger.save(result)
        decision = result["decision"]
        action = decision.get("action")
        symbol = decision.get("symbol")
        # =====================================================
        # TELEGRAM
        # =====================================================
        # HOLD non viene notificato.
        # BUY, SELL e SWITCH vengono notificati.
        if action == "SWITCH":
            message = (
                "🔄 ALPHAAI SWITCH\n\n"
                f"SELL: {decision.get('sell_symbol')}\n"
                f"SELL PRICE: {decision.get('sell_price')}\n\n"
                f"BUY: {decision.get('buy_symbol')}\n"
                f"BUY PRICE: {decision.get('buy_price')}\n\n"
                f"OLD SCORE: {decision.get('old_score')}\n"
                f"NEW SCORE: {decision.get('new_score')}\n\n"
                f"Balance: {result['balance']}"
            )
            telegram.send_message(message)
            print("Telegram SWITCH sent")
        elif action == "BUY":
            message = (
                "🟢 ALPHAAI BUY\n\n"
                f"Symbol: {symbol}\n"
                f"Price: {decision.get('price')}\n"
                f"Score: {decision.get('score')}\n"
                f"Confidence: "
                f"{decision.get('confidence', 'N/A')}\n"
                f"Balance: {result['balance']}"
            )
            telegram.send_message(message)
            print("Telegram BUY sent")
        elif action == "SELL":
            reason = decision.get(
                "reason",
                "SELL"
            )
            message = (
                "🔴 ALPHAAI SELL\n\n"
                f"Symbol: {symbol}\n"
                f"Price: {decision.get('price')}\n"
                f"Reason: {reason}\n"
                f"Score: {decision.get('score')}\n"
                f"Balance: {result['balance']}"
            )
            telegram.send_message(message)
            print("Telegram SELL sent")
        else:
            print("No new signal - Telegram skipped")
    except Exception as e:
        print("ERROR:", e)
    time.sleep(10)