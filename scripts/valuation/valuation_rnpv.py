"""Risk-adjusted net present value for pipeline assets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from scripts.valuation.valuation_common import require_non_negative, require_positive


@dataclass(frozen=True)
class PipelineAsset:
    name: str
    cash_flows: List[float]
    success_probability: float
    years_until_start: int = 0
    development_costs: List[float] | None = None


def present_value(cash_flows: Iterable[float], discount_rate: float, start_year: int = 1) -> float:
    require_positive(discount_rate, "discount_rate")
    return sum(cf / ((1 + discount_rate) ** (i + start_year)) for i, cf in enumerate(cash_flows))


def rnpv_asset_value(asset: PipelineAsset, discount_rate: float) -> float:
    if not 0 <= asset.success_probability <= 1:
        raise ValueError("success_probability must be between 0 and 1")
    require_non_negative(asset.years_until_start, "years_until_start")

    revenue_pv = present_value(
        asset.cash_flows,
        discount_rate=discount_rate,
        start_year=asset.years_until_start + 1,
    )
    cost_pv = present_value(asset.development_costs or [], discount_rate=discount_rate)
    return revenue_pv * asset.success_probability - cost_pv


def portfolio_rnpv(
    assets: Iterable[PipelineAsset],
    discount_rate: float,
    net_cash: float = 0.0,
    corporate_overhead_pv: float = 0.0,
) -> float:
    return sum(rnpv_asset_value(asset, discount_rate) for asset in assets) + net_cash - corporate_overhead_pv


def build_peak_sales_cash_flows(
    peak_sales: float,
    fcf_margin: float,
    ramp_years: int,
    plateau_years: int,
    decline_years: int = 0,
    terminal_decline_rate: float = 0.2,
) -> List[float]:
    """Create a simple product FCF curve from peak sales and margin."""

    require_positive(peak_sales, "peak_sales")
    if not 0 <= fcf_margin <= 1:
        raise ValueError("fcf_margin must be between 0 and 1")
    require_positive(ramp_years, "ramp_years")
    require_non_negative(plateau_years, "plateau_years")
    require_non_negative(decline_years, "decline_years")
    if not 0 <= terminal_decline_rate <= 1:
        raise ValueError("terminal_decline_rate must be between 0 and 1")

    peak_fcf = peak_sales * fcf_margin
    cash_flows: List[float] = []
    for year in range(1, ramp_years + 1):
        cash_flows.append(peak_fcf * year / ramp_years)
    cash_flows.extend([peak_fcf] * plateau_years)

    declining_fcf = peak_fcf
    for _ in range(decline_years):
        declining_fcf *= 1 - terminal_decline_rate
        cash_flows.append(declining_fcf)
    return cash_flows

