"""Structured assumption gate for valuation models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping


REQUIRED_ASSUMPTION_FIELDS = [
    "assumption",
    "value",
    "scenario",
    "evidence",
    "confidence",
    "sensitivity",
]


MODEL_REQUIRED_ASSUMPTIONS: Dict[str, List[str]] = {
    "owner_earnings_dcf": [
        "base_owner_earnings_or_fcf",
        "forecast_growth",
        "discount_rate",
        "terminal_growth",
        "net_debt",
        "shares_outstanding",
    ],
    "reverse_dcf": [
        "market_cap_or_price",
        "base_fcf_or_revenue",
        "discount_rate",
        "terminal_growth",
        "forecast_period",
    ],
    "ddm": [
        "current_dividend_per_share",
        "dividend_growth",
        "cost_of_equity",
        "terminal_growth",
        "payout_sustainability",
    ],
    "epv": [
        "normalized_ebit",
        "tax_rate",
        "wacc",
        "net_debt",
        "shares_outstanding",
    ],
    "sotp": [
        "segment_metrics",
        "segment_multiples_or_values",
        "corporate_costs",
        "net_debt",
    ],
    "comps": [
        "peer_set",
        "peer_multiple_selection",
        "target_metric",
        "quality_adjustment",
    ],
    "liquidation": [
        "asset_recovery_rates",
        "liability_claims",
        "liquidation_costs",
    ],
    "rnpv": [
        "pipeline_assets",
        "success_probabilities",
        "launch_timing",
        "cash_flow_or_peak_sales",
        "discount_rate",
    ],
    "reit": [
        "noi_or_affo",
        "cap_rate_or_affo_multiple",
        "net_debt",
        "distribution_coverage",
    ],
    "cyclical": [
        "mid_cycle_metric",
        "mid_cycle_multiple",
        "downcycle_stress",
        "net_debt",
    ],
    "insurance": [
        "adjusted_book_or_embedded_value",
        "underwriting_profitability",
        "investment_portfolio_adjustment",
        "holding_company_discount",
    ],
    "scenario": [
        "scenario_values",
        "scenario_probabilities",
        "scenario_rationale",
    ],
    "fintech_brokerage": [
        "funded_customers",
        "auc",
        "arpu_or_revenue_build",
        "net_interest_sensitivity",
        "crypto_or_transaction_volume_stress",
        "regulatory_risk",
    ],
}


@dataclass
class AssumptionGateResult:
    status: str
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    required_missing: List[str] = field(default_factory=list)
    low_confidence: List[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == "Passed"


def _normalize_assumption(item: Any) -> Dict[str, Any]:
    if hasattr(item, "__dict__"):
        return dict(item.__dict__)
    if isinstance(item, Mapping):
        return dict(item)
    raise TypeError("assumption must be a mapping or dataclass-like object")


def _assumption_names(assumptions: Iterable[Mapping[str, Any]]) -> set[str]:
    return {str(item.get("assumption", "")).strip() for item in assumptions if item.get("assumption")}


def audit_structured_assumptions(
    assumptions: Iterable[Mapping[str, Any] | Any],
    required_assumptions: Iterable[str] | None = None,
) -> AssumptionGateResult:
    normalized = [_normalize_assumption(item) for item in assumptions]
    issues: List[str] = []
    warnings: List[str] = []
    low_confidence: List[str] = []

    for index, item in enumerate(normalized):
        label = item.get("assumption", f"assumption[{index}]")
        for field_name in REQUIRED_ASSUMPTION_FIELDS:
            value = item.get(field_name)
            if value is None or value == "" or value == () or value == []:
                issues.append(f"{label}: missing {field_name}")

        evidence = item.get("evidence")
        if isinstance(evidence, list) and len(evidence) == 1:
            warnings.append(f"{label}: only one evidence item; confidence should usually be medium or low")

        if item.get("confidence") == "low":
            low_confidence.append(str(label))

        if item.get("sensitivity") == "high" and item.get("confidence") == "low":
            warnings.append(f"{label}: high sensitivity and low confidence; widen valuation range or block action")

    names = _assumption_names(normalized)
    required_missing = sorted(set(required_assumptions or []) - names)
    for name in required_missing:
        issues.append(f"missing required assumption: {name}")

    status = "Passed"
    if issues:
        status = "Blocked"
    elif low_confidence or warnings:
        status = "Warning"

    return AssumptionGateResult(
        status=status,
        issues=issues,
        warnings=warnings,
        required_missing=required_missing,
        low_confidence=low_confidence,
    )


def audit_model_assumptions(
    model_key: str,
    assumptions: Iterable[Mapping[str, Any] | Any],
) -> AssumptionGateResult:
    return audit_structured_assumptions(
        assumptions,
        required_assumptions=MODEL_REQUIRED_ASSUMPTIONS.get(model_key, []),
    )
