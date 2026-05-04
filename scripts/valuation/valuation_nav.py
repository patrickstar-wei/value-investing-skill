"""NAV valuation."""

from typing import Dict

from scripts.valuation.valuation_common import ValuationResult


def nav(asset_fair_values: Dict[str, float], liability_fair_values: Dict[str, float]) -> float:
    return sum(asset_fair_values.values()) - sum(liability_fair_values.values())


def nav_per_share(total_nav: float, shares_outstanding: float) -> float:
    return total_nav / shares_outstanding


def discount_to_nav(nav_per_share_value: float, market_price: float) -> float:
    return (nav_per_share_value - market_price) / nav_per_share_value


def nav_result(
    asset_fair_values: Dict[str, float],
    liability_fair_values: Dict[str, float],
    shares_outstanding: float | None = None,
    model_name: str = "NAV",
) -> ValuationResult:
    total_nav = nav(asset_fair_values, liability_fair_values)
    result = ValuationResult(
        model_name=model_name,
        base_value=total_nav,
        key_assumptions=[
            f"Asset categories: {len(asset_fair_values)}",
            f"Liability categories: {len(liability_fair_values)}",
        ],
        metadata={"valuation_status": "usable"},
    )
    if shares_outstanding:
        result.per_share_base = nav_per_share(total_nav, shares_outstanding)
    return result
