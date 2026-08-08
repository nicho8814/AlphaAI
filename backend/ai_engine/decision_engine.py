from ai_engine.risk_manager import RiskManager


class DecisionEngine:

    def __init__(self):
        self.risk_manager = RiskManager()

    def decide(self, market_data, balance):

        # Nessun dato disponibile
        if not market_data:
            return {
                "action": "HOLD",
                "symbol": None,
                "score": None,
                "reason": "Nessun dato disponibile"
            }

        # Considera solo dati con uno score valido
        valid_coins = [
            coin
            for coin in market_data
            if coin.get("score") is not None
        ]

        # Nessuno score valido
        if not valid_coins:
            return {
                "action": "HOLD",
                "symbol": None,
                "score": None,
                "reason": "Nessuno score valido"
            }

        # Prende la crypto con lo score più alto
        best_coin = max(
            valid_coins,
            key=lambda coin: coin["score"]
        )

        symbol = best_coin["symbol"]
        score = best_coin["score"]

        print("\n===== DECISION DEBUG =====")
        print("SYMBOL:", symbol)
        print("SCORE:", score)
        print("BALANCE:", balance)
        print("==========================")

        # Score troppo basso
        if score < 60:
            return {
                "action": "HOLD",
                "symbol": symbol,
                "score": score,
                "reason": "Score troppo basso"
            }

        # Calcolo della dimensione della posizione
        risk = self.risk_manager.calculate_position_size(
            balance,
            score,
            "MEDIUM"
        )

        print("\n===== RISK DEBUG =====")
        print("BALANCE:", balance)
        print("SCORE:", score)
        print("RISK:", risk)
        print("======================")

        # Controllo sicurezza
        if not risk:
            return {
                "action": "HOLD",
                "symbol": symbol,
                "score": score,
                "reason": "Risk manager non ha restituito una posizione"
            }

        amount = risk.get("amount", 0)
        confidence = risk.get("confidence", "N/A")
        percentage = risk.get("percentage", 0)

        # Nessun capitale disponibile
        if amount <= 0:
            return {
                "action": "HOLD",
                "symbol": symbol,
                "score": score,
                "reason": "Importo di posizione non valido"
            }

        # BUY
        return {
            "action": "BUY",
            "symbol": symbol,
            "score": score,
            "confidence": confidence,
            "amount": amount,
            "percentage": percentage
        }