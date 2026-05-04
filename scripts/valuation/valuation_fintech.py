"""Fintech and brokerage platform valuation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from scripts.valuation.valuation_common import equity_value_from_enterprise_value, per_share, require_positive


@dataclass(frozen=True)
class RevenueStream:
    name: str
    revenue: float
    growth_rate: float = 0.0
    stress_factor: float = 1.0


def brokerage_revenue_build(
    funded_customers: float,
    arpu: float,
    net_interest_income: float = 0.0,
    crypto_revenue: float = 0.0,
    other_revenue: float = 0.0,
) -> float:
    require_positive(funded_customers, "funded_customers")
    return funded_customers * arpu + net_interest_income + crypto_revenue + other_revenue


def revenue_stream_forecast(streams: Iterable[RevenueStream], years: int = 5) -> list[float]:
    require_positive(years, "years")
    yearly = [0.0 for _ in range(years)]
    for stream in streams:
        revenue = stream.revenue
        for year in range(years):
            revenue *= 1 + stream.growth_rate
            yearly[year] += revenue * stream.stress_factor
    return yearly


def net_interest_income_sensitivity(
    interest_earning_assets: float,
    current_yield: float,
    rate_change: float,
    deposit_beta: float = 0.0,
) -> float:
    if not 0 <= deposit_beta <= 1:
        raise ValueError("deposit_beta must be between 0 and 1")
    effective_change = rate_change * (1 - deposit_beta)
    return interest_earning_assets * (current_yield + effective_change)


def auc_based_value(assets_under_custody: float, value_to_auc: float) -> float:
    require_positive(value_to_auc, "value_to_auc")
    return assets_under_custody * value_to_auc


def normalized_earnings_value(
    revenue: float,
    normalized_margin: float,
    earnings_multiple: float,
    net_debt: float = 0.0,
    non_operating_assets: float = 0.0,
) -> float:
    if not -1 <= normalized_margin <= 1:
        raise ValueError("normalized_margin must be between -100% and 100%")
    require_positive(earnings_multiple, "earnings_multiple")
    net_income = revenue * normalized_margin
    enterprise_value = net_income * earnings_multiple
    return equity_value_from_enterprise_value(
        enterprise_value=enterprise_value,
        net_debt=net_debt,
        non_operating_assets=non_operating_assets,
    )


def fintech_value_per_share(equity_value: float, shares_outstanding: float) -> float:
    return per_share(equity_value, shares_outstanding)

