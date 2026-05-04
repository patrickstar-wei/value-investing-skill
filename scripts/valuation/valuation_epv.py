"""Earnings Power Value model."""

from scripts.valuation.valuation_common import ValuationResult, per_share

def epv_enterprise_value(normalized_ebit: float, tax_rate: float, wacc: float) -> float:
    if wacc <= 0:
        raise ValueError("wacc must be positive")
    nopat = normalized_ebit * (1 - tax_rate)
    return nopat / wacc


def epv_equity_value(normalized_ebit: float, tax_rate: float, wacc: float, net_debt: float) -> float:
    return epv_enterprise_value(normalized_ebit, tax_rate, wacc) - net_debt


def franchise_value(dcf_value: float, epv_value: float) -> float:
    return dcf_value - epv_value


def epv_result(
    normalized_ebit: float,
    tax_rate: float,
    wacc: float,
    net_debt: float,
    shares_outstanding: float | None = None,
    model_name: str = "EPV",
) -> ValuationResult:
    equity_value = epv_equity_value(
        normalized_ebit=normalized_ebit,
        tax_rate=tax_rate,
        wacc=wacc,
        net_debt=net_debt,
    )
    result = ValuationResult(
        model_name=model_name,
        base_value=equity_value,
        key_assumptions=[
            f"Normalized EBIT: {normalized_ebit}",
            f"Tax rate: {tax_rate}",
            f"WACC: {wacc}",
        ],
        metadata={"valuation_status": "usable"},
    )
    if shares_outstanding:
        result.per_share_base = per_share(equity_value, shares_outstanding)
    return result
