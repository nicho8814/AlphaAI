import requests


class CryptoComClient:


    def __init__(
        self,
        api_key=None,
        secret_key=None
    ):

        self.api_key = api_key
        self.secret_key = secret_key

        self.base_url = (
            "https://api.crypto.com/"
            "v2"
        )


    def get_ticker(
        self,
        symbol="BTC_USDT"
    ):

        url = (
            f"{self.base_url}"
            "/public/get-ticker"
        )


        params = {
            "instrument_name": symbol
        }


        response = requests.get(
            url,
            params=params
        )


        return response.json()
