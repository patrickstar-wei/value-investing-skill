"""Dividend discount valuation models."""

from __future__ import annotations

from typing import Dict, List

from scripts.valuation.valuation_common import require_non_negative, require_positive, require_rate_order


def gordon_growth_value(next_dividend_per_share: float, cost_of_equity: float, terminal_growth: float) -> float:
    """Single-stage Gordon Growth dividend value per share."""

    require_non_negative(next_dividend_per_share, "next_dividend_per_share")
    require_rate_order(cost_of_equity, terminal_growth)
    return next_dividend_per_share / (cost_of_equity - terminal_growth)


def two_stage_ddm(
    current_dividend_per_share: float,
    first_stage_growth: float,
    terminal_growth: float,
    cost_of_equity: float,
    years: int = 5,
) -> float:
    """Two-stage dividend discount model value per share."""

    require_non_negative(current_dividend_per_share, "current_dividend_per_share")
    require_positive(years, "years")
    require_rate_order(cost_of_equity, terminal_growth)

    dividend = current_dividend_per_share
    present_value = 0.0
    for year in range(1, years + 1):
        dividend *= 1 + first_stage_growth
        present_value += dividend / ((1 + cost_of_equity) ** year)

    terminal_value = dividend * (1 + terminal_growth) / (cost_of_equity - terminal_growth)
    present_value += terminal_value / ((1 + cost_of_equity) ** years)
    return present_value


def dividend_yield(dividend_per_share: float, market_price: float) -> float:
    require_non_negative(dividend_per_share, "dividend_per_share")
    require_positive(market_price, "market_price")
    return dividend_per_share / market_price


def payout_ratio(dividend_per_share: float, earnings_per_share: float) -> float:
    require_non_negative(dividend_per_share, "dividend_per_share")
    require_positive(earnings_per_share, "earnings_per_share")
    return dividend_per_share / earnings_per_share


def dividend_coverage(fcfe: float, dividends_paid: float) -> float:
    require_positive(dividends_paid, "dividends_paid")
    return fcfe / dividends_paid


def implied_dividend_growth(
    market_price: float,
    next_dividend_per_share: float,
    cost_of_equity: float,
) -> float:
    """Implied perpetual dividend growth from Gordon Growth."""

    require_positive(market_price, "market_price")
    require_non_negative(next_dividend_per_share, "next_dividend_per_share")
    return cost_of_equity - (next_dividend_per_share / market_price)


def dividend_yield_band_value(dividend_per_share: float, target_yields: Dict[str, float]) -> Dict[str, float]:
    """Map scenario names to price values using target dividend yields."""

    require_non_negative(dividend_per_share, "dividend_per_share")
    values: Dict[str, float] = {}
    for name, target_yield in target_yields.items():
        require_positive(target_yield, f"target_yields[{name}]")
        values[name] = dividend_per_share / target_yield
    return values


def dividend_forecast(
    current_dividend_per_share: float,
    growth_rates: List[float],
) -> List[float]:
    require_non_negative(current_dividend_per_share, "current_dividend_per_share")
    dividend = current_dividend_per_share
    dividends: List[float] = []
    for growth in growth_rates:
        dividend *= 1 + growth
        dividends.append(dividend)
    return dividends

