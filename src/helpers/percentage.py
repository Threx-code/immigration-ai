from decimal import Decimal, ROUND_HALF_UP


class PercentageHelper:

    @staticmethod
    def calculate(part, total):
        if total == 0:
            return Decimal('0.00')
        return (part / total) * 100

    @staticmethod
    def quantize_decimal(value):
        """Helper function to quantize Decimal values to a specific precision."""
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)