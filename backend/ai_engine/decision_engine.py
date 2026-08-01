from ai_engine.risk_manager import RiskManager


class DecisionEngine:

    def __init__(self):
        self.risk_manager = RiskManager()


    def decide(self, market_data, balance):

        if not market_data:
            return {
                "action": "HOLD",
                "reason": "Nessun dato disponibile"
            }


        # sceglie la crypto con lo score più alto
        best_coin = max(
            market_data,
            key=lambda coin: coin["score"]
        )


        score = best_coin["score"]


        # se il punteggio è troppo basso non entra
        if score < 60:
            return {
                "action": "HOLD",
                "symbol": best_coin["symbol"],
                "score": score,
                "reason": "Score troppo basso"
            }


        # per ora usiamo volatilità media
        risk = self.risk_manager.calculate_position_size(
            balance,
            score,
            "MEDIUM"
        )


        return {
            "action": "BUY",
            "symbol": best_coin["symbol"],
            "score": score,
            "confidence": risk["confidence"],
            "amount": risk["amount"],
            "percentage": risk["percentage"]
        }