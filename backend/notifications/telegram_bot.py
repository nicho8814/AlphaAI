import os
import requests
from dotenv import load_dotenv


load_dotenv()


class TelegramBot:

    def __init__(self):

        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

        self.url = (
            f"https://api.telegram.org/bot{self.token}/sendMessage"
        )


    def send_message(self, message):

        try:

            data = {
                "chat_id": self.chat_id,
                "text": message
            }

            response = requests.post(
                self.url,
                data=data
            )

            return response.json()


        except Exception as e:

            print("Telegram error:", e)
            return None