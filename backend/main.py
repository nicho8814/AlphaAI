from fastapi import FastAPI

from market.data_feed import MarketData
from ai_engine.analyzer import AIAnalyzer


app = FastAPI(
    title="AlphaAI Trading System",
    version="0.1"
)


@app.get("/")
def home():

    return {
        "status": "AlphaAI online",
        "version": "0.1"
    }


@app.get("/price/{symbol}")
def get_price(symbol: str):

    market = MarketData()

    return market.get_price(symbol)


@app.get("/analyze")
def analyze():

    ai = AIAnalyzer()

    result = ai.analyze(
        rsi=30,
        price=68000,
        average=65000
    )

    return result
