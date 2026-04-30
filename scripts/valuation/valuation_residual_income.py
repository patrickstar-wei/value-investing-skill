"""Residual Income valuation."""

from typing import List


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
