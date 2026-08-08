import os
import requests

from dotenv import load_dotenv


load_dotenv()


class TelegramBot:

    def __init__(self):

        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        self.url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/sendMessage"
        )

    def send_message(self, message):

        if not self.token or not self.chat_id:
            print("Telegram error: TOKEN o CHAT_ID mancanti")
            return None

        try:

            data = {
                "chat_id": self.chat_id,
                "text": message
            }

            response = requests.post(
                self.url,
                data=data,
                timeout=10
            )

            response.raise_for_status()

            result = response.json()

            print("Telegram:", result)

            return result

        except Exception as e:

            print("Telegram error:", e)

            return None