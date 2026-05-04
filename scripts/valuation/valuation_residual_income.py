"""Residual Income valuation."""

from typing import List

from scripts.valuation.valuation_common import ValuationResult, per_share


def residual_income(net_income: float, cost_of_equity: float, beginning_book_value: float) -> float:
    return net_income - cost_of_equity * beginning_book_value


def equity_value_from_residual_income(
    current_book_value: float,
    residual_income_forecast: List[float],
    cost_of_equity: float,
) -> float:
    pv_ri = sum(
        ri / ((1 + cost_of_equity) ** (i + 1))
        for i, ri in enumerate(residual_income_forecast)
    )
    return current_book_value + pv_ri


def theoretical_pb(roe: float, growth: float, cost_of_equity: float) -> float:
    if cost_of_equity <= growth:
        raise ValueError("cost_of_equity must be greater than growth")
    return (roe - growth) / (cost_of_equity - growth)


def residual_income_result(
    current_book_value: float,
    residual_income_forecast: List[float],
    cost_of_equity: float,
    shares_outstanding: float | None = None,
    model_name: str = "Residual Income",
) -> ValuationResult:
    equity_value = equity_value_from_residual_income(
        current_book_value=current_book_value,
        residual_income_forecast=residual_income_forecast,
        cost_of_equity=cost_of_equity,
    )
    result = ValuationResult(
        model_name=model_name,
        base_value=equity_value,
        key_assumptions=[
            f"Current book value: {current_book_value}",
            f"Cost of equity: {cost_of_equity}",
            f"Forecast years: {len(residual_income_forecast)}",
        ],
        metadata={"valuation_status": "usable"},
    )
    if shares_outstanding:
        result.per_share_base = per_share(equity_value, shares_outstanding)
    return result
