"""NAV valuation."""

from typing import Dict


def nav(asset_fair_values: Dict[str, float], liability_fair_values: Dict[str, float]) -> float:
    return sum(asset_fair_values.values()) - sum(liability_fair_values.values())


def nav_per_share(total_nav: float, shares_outstanding: float) -> float:
    return total_nav / shares_outstanding


def discount_to_nav(nav_per_share_value: float, market_price: float) -> float:
    return (nav_per_share_value - market_price) / nav_per_share_value
