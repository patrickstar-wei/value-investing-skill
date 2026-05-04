"""REIT and infrastructure yield valuation helpers."""

from __future__ import annotations

from scripts.valuation.valuation_common import equity_value_from_enterprise_value, per_share, require_positive


def noi_capitalized_value(noi: float, cap_rate: float) -> float:
    require_positive(cap_rate, "cap_rate")
    return noi / cap_rate


def affo_multiple_value(affo: float, affo_multiple: float) -> float:
    require_positive(affo_multiple, "affo_multiple")
    return affo * affo_multiple


def affo_yield(affo: float, equity_market_cap: float) -> float:
    require_positive(equity_market_cap, "equity_market_cap")
    return affo / equity_market_cap


def distribution_coverage(affo: float, distributions: float) -> float:
    require_positive(distributions, "distributions")
    return affo / distributions


def reit_equity_value_from_noi(
    noi: float,
    cap_rate: float,
    net_debt: float = 0.0,
    minority_interest: float = 0.0,
    non_operating_assets: float = 0.0,
) -> float:
    enterprise_value = noi_capitalized_value(noi, cap_rate)
    return equity_value_from_enterprise_value(
        enterprise_value=enterprise_value,
        net_debt=net_debt,
        minority_interest=minority_interest,
        non_operating_assets=non_operating_assets,
    )


def reit_value_per_share(equity_value: float, shares_outstanding: float) -> float:
    return per_share(equity_value, shares_outstanding)

