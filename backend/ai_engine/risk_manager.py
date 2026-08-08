class RiskManager:
    def __init__(self, max_risk=0.40):
        self.max_risk = max_risk
    def calculate_confidence(self, score):
        if score >= 90:
            return "HIGH"
        elif score >= 75:
            return "MEDIUM"
        else:
            return "LOW"
    def calculate_position_size(
        self,
        balance,
        score,
        volatility
    ):
        confidence = self.calculate_confidence(score)
        # Dimensione base della posizione
        if confidence == "HIGH":
            size = 0.30
        elif confidence == "MEDIUM":
            size = 0.15
        else:
            size = 0.05
        # Se la volatilità è alta,
        # dimezza la posizione
        if volatility == "HIGH":
            size = size / 2
        # Non superare mai il limite massimo
        if size > self.max_risk:
            size = self.max_risk
        # Protezione da balance non valido
        if balance <= 0:
            return {
                "confidence": confidence,
                "percentage": 0,
                "amount": 0
            }
        amount = balance * size
        return {
            "confidence": confidence,
            "percentage": round(size * 100, 2),
            "amount": round(amount, 2)
        }