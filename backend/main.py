from fastapi import FastAPI

from ai_engine.analyzer import AIAnalyzer
from market.data_feed import MarketData
from indicators.technical import TechnicalIndicators
from trading.simulator import TradingSimulator
from trading.backtester import Backtester
from database.storage import TradeStorage


app = FastAPI(
    title="AlphaAI",
    version="0.6"
)


simulator = TradingSimulator()
storage = TradeStorage()


@app.get("/")
def home():

    return {
        "status": "AlphaAI online",
        "version": "0.6"
    }



@app.get("/analyze")
def analyze():

    ai = AIAnalyzer()

    return ai.analyze(
        rsi=30,
        price=68000,
        average=65000
    )



@app.get("/analyze/{symbol}")
def analyze_crypto(symbol: str):

    market = MarketData()

    candles = market.get_candles(symbol)

    prices = [
        candle["close"]
        for candle in candles
    ]


    indicators = TechnicalIndicators()

    rsi = indicators.rsi(prices)
    average = indicators.moving_average(prices)


    ai = AIAnalyzer()

    result = ai.analyze(
        rsi=rsi,
        price=prices[-1],
        average=average
    )


    return {
        "symbol": symbol,
        "price": prices[-1],
        "rsi": rsi,
        "average": average,
        "analysis": result
    }



@app.get("/market/{symbol}")
def market_data(symbol: str):

    market = MarketData()

    candles = market.get_candles(symbol)

    return {
        "symbol": symbol,
        "candles": candles[:5]
    }



@app.get("/simulate/{symbol}")
def simulate_trade(symbol: str):

    market = MarketData()

    candles = market.get_candles(symbol)

    prices = [
        candle["close"]
        for candle in candles
    ]


    indicators = TechnicalIndicators()

    rsi = indicators.rsi(prices)
    average = indicators.moving_average(prices)


    ai = AIAnalyzer()

    decision = ai.analyze(
        rsi=rsi,
        price=prices[-1],
        average=average
    )


    if decision["decision"] == "BUY":

        action = simulator.buy(prices[-1])


    elif decision["decision"] == "SELL":

        action = simulator.sell(prices[-1])


    else:

        action = "No action"



    return {
        "symbol": symbol,
        "price": prices[-1],
        "rsi": rsi,
        "decision": decision,
        "action": action,
        "portfolio": simulator.status(prices[-1])
    }



@app.get("/portfolio")
def portfolio():

    return simulator.status(0)



@app.get("/history")
def history():

    return {
        "trades": storage.get_trades()
    }



@app.get("/backtest/{symbol}")
def backtest(symbol: str):

    market = MarketData()

    candles = market.get_candles(symbol)

    prices = [
        candle["close"]
        for candle in candles
    ]


    def alpha_strategy(price):

        if price < 60000:

            return "BUY"


        elif price > 65000:

            return "SELL"


        else:

            return "HOLD"



    tester = Backtester()


    result = tester.run(
        prices,
        alpha_strategy
    )


    return {
        "symbol": symbol,
        "prices_tested": len(prices),
        "result": result
    }