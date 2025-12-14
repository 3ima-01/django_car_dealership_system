from decimal import ROUND_HALF_UP, Decimal


def normalize_decimal(value, places=2):
    return str(Decimal(str(value)).quantize(Decimal(f"0.{'0' * places}"), rounding=ROUND_HALF_UP))
