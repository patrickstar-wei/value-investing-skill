"""Insurance and embedded-value valuation helpers."""

from __future__ import annotations

from scripts.valuation.valuation_common import per_share, require_positive


def price_to_embedded_value(embedded_value: float, multiple: float) -> float:
    require_positive(multiple, "multiple")
    return embedded_value * multiple


def insurance_equity_value(
    adjusted_book_value: float,
    value_of_new_business: float = 0.0,
    underwriting_value: float = 0.0,
    investment_portfolio_adjustment: float = 0.0,
    holding_company_discount: float = 0.0,
) -> float:
    if not 0 <= holding_company_discount < 1:
        raise ValueError("holding_company_discount must be between 0 and 1")
    gross_value = (
        adjusted_book_value
        + value_of_new_business
        + underwriting_value
        + investment_portfolio_adjustment
    )
    return gross_value * (1 - holding_company_discount)


def combined_ratio(incurred_losses: float, expenses: float, earned_premiums: float) -> float:
    require_positive(earned_premiums, "earned_premiums")
    return (incurred_losses + expenses) / earned_premiums


def float_cost(underwriting_profit: float, average_float: float) -> float:
    require_positive(average_float, "average_float")
    return -underwriting_profit / average_float


def implied_roe_valuation(book_value: float, target_pb: float) -> float:
    require_positive(target_pb, "target_pb")
    return book_value * target_pb


def insurance_value_per_share(equity_value: float, shares_outstanding: float) -> float:
    return per_share(equity_value, shares_outstanding)

