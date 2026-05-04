"""Comparable company and multiple-based valuation."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from typing import Iterable, List, Optional

from scripts.valuation.valuation_common import equity_value_from_enterprise_value, per_share, require_positive


@dataclass(frozen=True)
class ComparableCompany:
    name: str
    multiple: float
    growth: Optional[float] = None
    margin: Optional[float] = None
    roic: Optional[float] = None
    leverage: Optional[float] = None


def trimmed_median(values: Iterable[float], trim_fraction: float = 0.1) -> float:
    values_sorted = sorted(values)
    if not values_sorted:
        raise ValueError("values must not be empty")
    if not 0 <= trim_fraction < 0.5:
        raise ValueError("trim_fraction must be between 0 and 0.5")

    trim_count = int(len(values_sorted) * trim_fraction)
    if trim_count:
        values_sorted = values_sorted[trim_count:-trim_count]
    return median(values_sorted)


def peer_multiple(peers: Iterable[ComparableCompany], trim_fraction: float = 0.1) -> float:
    multiples: List[float] = []
    for peer in peers:
        require_positive(peer.multiple, f"{peer.name}.multiple")
        multiples.append(peer.multiple)
    return trimmed_median(multiples, trim_fraction=trim_fraction)


def quality_adjusted_multiple(
    base_multiple: float,
    growth_premium: float = 0.0,
    margin_premium: float = 0.0,
    roic_premium: float = 0.0,
    leverage_discount: float = 0.0,
) -> float:
    require_positive(base_multiple, "base_multiple")
    adjustment = 1 + growth_premium + margin_premium + roic_premium - leverage_discount
    if adjustment <= 0:
        raise ValueError("combined multiple adjustment must be positive")
    return base_multiple * adjustment


def enterprise_value_from_multiple(metric: float, multiple: float) -> float:
    require_positive(multiple, "multiple")
    return metric * multiple


def equity_value_from_multiple(
    metric: float,
    multiple: float,
    net_debt: float = 0.0,
    minority_interest: float = 0.0,
    non_operating_assets: float = 0.0,
) -> float:
    enterprise_value = enterprise_value_from_multiple(metric, multiple)
    return equity_value_from_enterprise_value(
        enterprise_value=enterprise_value,
        net_debt=net_debt,
        minority_interest=minority_interest,
        non_operating_assets=non_operating_assets,
    )


def multiple_value_per_share(equity_value: float, shares_outstanding: float) -> float:
    return per_share(equity_value, shares_outstanding)

