"""Formula audit checks."""

from typing import List


def audit_model_suitability(industry: str, selected_model: str) -> List[str]:
    warnings: List[str] = []
    industry_lower = industry.lower()
    model_lower = selected_model.lower()

    if "bank" in industry_lower and "ev/ebitda" in model_lower:
        warnings.append("Banks should not use EV/EBITDA as the primary valuation model.")

    if "biotech" in industry_lower and "p/e" in model_lower:
        warnings.append("Clinical-stage biotech should not use P/E as the primary valuation model.")

    if "cyclical" in industry_lower and "current p/e" in model_lower:
        warnings.append("Cyclicals should use mid-cycle earnings rather than current-year P/E.")

    return warnings
