from ai_engine.risk_manager import RiskManager


class DecisionEngine:

    def __init__(self):
        self.risk_manager = RiskManager()


    def decide(self, market_data, balance):

        # prende la crypto migliore
        best_coin = market_data[0]

        score = best_coin["score"]

        # sotto questa soglia non compra
        if score < 60:
            return {
                "action": "HOLD",
                "reason": "Score troppo basso"
            }


        # per ora consideriamo volatilità media
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