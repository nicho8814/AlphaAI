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



        # prende la crypto con score più alto

        best_coin = max(
            market_data,
            key=lambda coin: coin["score"]
        )


        score = best_coin["score"]



        # score troppo basso

        if score < 60:

            return {

                "action": "HOLD",
                "symbol": best_coin["symbol"],
                "score": score,
                "reason": "Score troppo basso"

            }



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