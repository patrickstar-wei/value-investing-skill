"""Reverse DCF utilities.

Supports:
1. FCF growth reverse DCF
2. Revenue-to-FCF reverse DCF

This is a lightweight deterministic module. Production versions should add
scenario tables, taxes, reinvestment, dilution, and explicit forecast drivers.
"""

from typing import List


def market_implied_ev(market_cap: float, net_debt: float) -> float:
    return market_cap + net_debt


def dcf_value_from_fcf_growth(
    base_fcf: float,
    growth_rate: float,
    years: int,
    discount_rate: float,
    terminal_growth: float,
) -> float:
    if discount_rate <= terminal_growth:
        raise ValueError("discount_rate must exceed terminal_growth")

    fcf = base_fcf
    cash_flows: List[float] = []
    for _ in range(years):
        fcf *= (1 + growth_rate)
        cash_flows.append(fcf)

    pv_stage = sum(cf / ((1 + discount_rate) ** (i + 1)) for i, cf in enumerate(cash_flows))
    terminal = cash_flows[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    pv_terminal = terminal / ((1 + discount_rate) ** years)
    return pv_stage + pv_terminal


def solve_implied_fcf_growth(
    target_ev: float,
    base_fcf: float,
    years: int,
    discount_rate: float,
    terminal_growth: float,
    low: float = -0.30,
    high: float = 0.60,
    iterations: int = 100,
) -> float:
    for _ in range(iterations):
        mid = (low + high) / 2
        value = dcf_value_from_fcf_growth(
            base_fcf=base_fcf,
            growth_rate=mid,
            years=years,
            discount_rate=discount_rate,
            terminal_growth=terminal_growth,
        )
        if value < target_ev:
            low = mid
        else:
            high = mid
    return (low + high) / 2


def dcf_value_from_revenue_to_fcf(
    base_revenue: float,
    revenue_growth: float,
    target_fcf_margin: float,
    years: int,
    discount_rate: float,
    terminal_growth: float,
) -> float:
    if discount_rate <= terminal_growth:
        raise ValueError("discount_rate must exceed terminal_growth")

    revenue = base_revenue
    cash_flows: List[float] = []
    for _ in range(years):
        revenue *= (1 + revenue_growth)
        cash_flows.append(revenue * target_fcf_margin)

    pv_stage = sum(cf / ((1 + discount_rate) ** (i + 1)) for i, cf in enumerate(cash_flows))
    terminal = cash_flows[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    pv_terminal = terminal / ((1 + discount_rate) ** years)
    return pv_stage + pv_terminal


def solve_implied_revenue_growth(
    target_ev: float,
    base_revenue: float,
    target_fcf_margin: float,
    years: int,
    discount_rate: float,
    terminal_growth: float,
    low: float = -0.20,
    high: float = 0.50,
    iterations: int = 100,
) -> float:
    for _ in range(iterations):
        mid = (low + high) / 2
        value = dcf_value_from_revenue_to_fcf(
            base_revenue=base_revenue,
            revenue_growth=mid,
            target_fcf_margin=target_fcf_margin,
            years=years,
            discount_rate=discount_rate,
            terminal_growth=terminal_growth,
        )
        if value < target_ev:
            low = mid
        else:
            high = mid
    return (low + high) / 2
