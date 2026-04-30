"""Margin of safety scoring."""

def margin_of_safety(intrinsic_value: float, market_price: float) -> float:
    return (intrinsic_value - market_price) / intrinsic_value


def classify_margin_of_safety(mos: float) -> str:
    if mos > 0.40:
        return "Very attractive"
    if mos > 0.25:
        return "Attractive"
    if mos > 0.10:
        return "Watchlist"
    if mos >= 0:
        return "Fair value"
    return "Overvalued"
