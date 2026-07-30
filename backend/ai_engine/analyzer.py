class AIAnalyzer:

    def analyze(self, rsi, price, average):

        score = 50

        if rsi < 30:
            score += 20

        if price > average:
            score += 15

        if rsi > 70:
            score -= 20

        if score >= 70:
            decision = "BUY"

        elif score <= 35:
            decision = "SELL"

        else:
            decision = "HOLD"

        return {
            "decision": decision,
            "score": score
        }