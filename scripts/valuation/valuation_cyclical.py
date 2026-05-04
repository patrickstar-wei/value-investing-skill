"""Cyclical and mid-cycle valuation helpers."""

from __future__ import annotations

from typing import Iterable

from scripts.valuation.valuation_common import equity_value_from_enterprise_value, per_share, require_positive


def mid_cycle_metric(values: Iterable[float]) -> float:
    values_list = list(values)
    if not values_list:
        raise ValueError("values must not be empty")
    return sum(values_list) / len(values_list)


def mid_cycle_enterprise_value(normalized_metric: float, mid_cycle_multiple: float) -> float:
    require_positive(mid_cycle_multiple, "mid_cycle_multiple")
    return normalized_metric * mid_cycle_multiple


def cyclical_equity_value(
    normalized_metric: float,
    mid_cycle_multiple: float,
    net_debt: float = 0.0,
    minority_interest: float = 0.0,
    non_operating_assets: float = 0.0,
) -> float:
    enterprise_value = mid_cycle_enterprise_value(normalized_metric, mid_cycle_multiple)
    return equity_value_from_enterprise_value(
        enterprise_value=enterprise_value,
        net_debt=net_debt,
        minority_interest=minority_interest,
        non_operating_assets=non_operating_assets,
    )


def commodity_scenario_ebitda(
    base_volume: float,
    commodity_price: float,
    cash_cost_per_unit: float,
    fixed_costs: float = 0.0,
) -> float:
    return base_volume * (commodity_price - cash_cost_per_unit) - fixed_costs


def cycle_stress_drawdown(normalized_value: float, stressed_value: float) -> float:
    require_positive(normalized_value, "normalized_value")
    return (normalized_value - stressed_value) / normalized_value


def cyclical_value_per_share(equity_value: float, shares_outstanding: float) -> float:
    return per_share(equity_value, shares_outstanding)

