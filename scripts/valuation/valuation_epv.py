"""Earnings Power Value model."""

def epv_enterprise_value(normalized_ebit: float, tax_rate: float, wacc: float) -> float:
    if wacc <= 0:
        raise ValueError("wacc must be positive")
    nopat = normalized_ebit * (1 - tax_rate)
    return nopat / wacc


def epv_equity_value(normalized_ebit: float, tax_rate: float, wacc: float, net_debt: float) -> float:
    return epv_enterprise_value(normalized_ebit, tax_rate, wacc) - net_debt


def franchise_value(dcf_value: float, epv_value: float) -> float:
    return dcf_value - epv_value
