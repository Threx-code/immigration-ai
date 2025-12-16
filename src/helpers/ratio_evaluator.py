
class RatioEvaluator:
    @staticmethod
    def evaluate(ratio):
        if ratio == 0:
            return "No Debt"
        elif ratio < 20:
            return "Excellent"
        elif 20 <= ratio < 35:
            return "Good"
        elif 35 <= ratio < 50:
            return "Fair"
        else:
            return "High Risk"
