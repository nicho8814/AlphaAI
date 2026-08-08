from market.scanner import MarketScanner
from market.data_feed import MarketData
class MarketManager:
    def __init__(self):
        self.scanner = MarketScanner()
        self.data = MarketData()
    def scan_markets(self, markets):
        results = []
        for market in markets:
            try:
                result = self.scanner.analyze_market(
                    market["symbol"],
                    market["prices"],
                    market["volumes"]
                )
                # Mantiene il simbolo anche se lo scanner
                # non lo restituisce
                if "symbol" not in result:
                    result["symbol"] = market["symbol"]
                results.append(result)
            except Exception as e:
                print(
                    "SCAN ERROR:",
                    market.get("symbol"),
                    e
                )
        # Ordina solo se ci sono risultati
        results.sort(
            key=lambda x: x.get("score", 0),
            reverse=True
        )
        return results
    def get_live_markets(self, symbols):
        markets = []
        for symbol in symbols:
            try:
                candles = self.data.get_candles(
                    symbol,
                    100
                )
                if not candles:
                    print(
                        "NO CANDLES:",
                        symbol
                    )
                    continue
                prices = [
                    candle["close"]
                    for candle in candles
                ]
                volumes = [
                    candle["volume"]
                    for candle in candles
                ]
                markets.append({
                    "symbol": symbol,
                    "prices": prices,
                    "volumes": volumes
                })
            except Exception as e:
                print(
                    "MARKET DATA ERROR:",
                    symbol,
                    e
                )
        return markets