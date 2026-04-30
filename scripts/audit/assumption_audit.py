"""Assumption audit helpers."""

from typing import Dict, List


def audit_dcf_assumptions(assumptions: Dict[str, float]) -> List[str]:
    warnings: List[str] = []

    revenue_growth = assumptions.get("revenue_growth")
    terminal_growth = assumptions.get("terminal_growth")
    wacc = assumptions.get("wacc")
    operating_margin = assumptions.get("operating_margin")

    if revenue_growth is not None and revenue_growth > 0.25:
        warnings.append("Revenue growth assumption is high; verify TAM, competition, and reinvestment needs.")

    if terminal_growth is not None and terminal_growth > 0.04:
        warnings.append("Terminal growth may be too high for a conservative valuation.")

    if wacc is not None and wacc < 0.07:
        warnings.append("WACC appears low; verify risk-free rate, beta, equity risk premium, and capital structure.")

    if operating_margin is not None and operating_margin > 0.40:
        warnings.append("Operating margin is very high; check historical and peer benchmarks.")

    return warnings
