"""Owner Earnings DCF model."""

from typing import List

from scripts.valuation.valuation_common import ValuationResult, per_share


def owner_earnings(
    net_income: float,
    depreciation_amortization: float,
    maintenance_capex: float,
    required_working_capital_increase: float = 0.0,
) -> float:
    return (
        net_income
        + depreciation_amortization
        - maintenance_capex
        - required_working_capital_increase
    )


def present_value(cash_flows: List[float], discount_rate: float) -> float:
    return sum(cf / ((1 + discount_rate) ** (i + 1)) for i, cf in enumerate(cash_flows))


def terminal_value_gordon(final_cash_flow: float, discount_rate: float, terminal_growth: float) -> float:
    if discount_rate <= terminal_growth:
        raise ValueError("discount_rate must be greater than terminal_growth")
    return final_cash_flow * (1 + terminal_growth) / (discount_rate - terminal_growth)


def intrinsic_equity_value(
    owner_earnings_forecast: List[float],
    discount_rate: float,
    terminal_growth: float,
    net_debt: float,
) -> float:
    pv_forecast = present_value(owner_earnings_forecast, discount_rate)
    tv = terminal_value_gordon(owner_earnings_forecast[-1], discount_rate, terminal_growth)
    pv_tv = tv / ((1 + discount_rate) ** len(owner_earnings_forecast))
    enterprise_value = pv_forecast + pv_tv
    return enterprise_value - net_debt


def owner_earnings_dcf_result(
    owner_earnings_forecast: List[float],
    discount_rate: float,
    terminal_growth: float,
    net_debt: float,
    shares_outstanding: float | None = None,
    model_name: str = "Owner Earnings DCF",
) -> ValuationResult:
    equity_value = intrinsic_equity_value(
        owner_earnings_forecast=owner_earnings_forecast,
        discount_rate=discount_rate,
        terminal_growth=terminal_growth,
        net_debt=net_debt,
    )
    result = ValuationResult(
        model_name=model_name,
        base_value=equity_value,
        key_assumptions=[
            f"Discount rate: {discount_rate}",
            f"Terminal growth: {terminal_growth}",
            f"Forecast years: {len(owner_earnings_forecast)}",
        ],
        metadata={"valuation_status": "usable"},
    )
    if shares_outstanding:
        result.per_share_base = per_share(equity_value, shares_outstanding)
    return result
