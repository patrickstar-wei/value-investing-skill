"""Audit financial-history and technology-cycle context gates."""

from __future__ import annotations

from typing import Any, Dict, List


def financial_history_gate(financial_history: Dict[str, Any] | None) -> Dict[str, str]:
    if not financial_history:
        return {
            "gate": "Financial History Gate",
            "status": "Blocked",
            "comment": "Financial history builder did not return a packet.",
        }

    coverage = financial_history.get("coverage", {})
    status = str(coverage.get("status", "blocked")).lower()
    if status == "passed":
        return {
            "gate": "Financial History Gate",
            "status": "Passed",
            "comment": (
                f"Core history available: annual_min={coverage.get('core_annual_periods_min', 0)}, "
                f"quarterly_min={coverage.get('core_quarterly_periods_min', 0)}."
            ),
        }
    if status == "limited":
        return {
            "gate": "Financial History Gate",
            "status": "Limited",
            "comment": (
                "Financial history is usable for trend context but below the default target. "
                f"Missing metrics: {', '.join(financial_history.get('missing_metrics', [])[:8]) or 'not specified'}."
            ),
        }
    return {
        "gate": "Financial History Gate",
        "status": "Blocked",
        "comment": (
            "Financial history coverage is insufficient for current valuation trend checks. "
            f"Errors: {financial_history.get('errors', [])}"
        ),
    }


def _has_any_metric(financial_history: Dict[str, Any], metric_names: List[str]) -> bool:
    metrics = financial_history.get("metrics", {})
    for metric in metric_names:
        payload = metrics.get(metric, {})
        if payload.get("annual") or payload.get("quarterly"):
            return True
    return False


def tech_cycle_context_gates(
    applicability: Dict[str, Any] | None,
    financial_history: Dict[str, Any] | None,
) -> List[Dict[str, str]]:
    """Return route-specific cycle gates.

    First version uses company financial history as the evidence base. External
    industry indicators can be added later without changing the gate names.
    """

    if not applicability:
        return [
            {
                "gate": "Tech Cycle Applicability Gate",
                "status": "Blocked",
                "comment": "Technology cycle applicability router did not run.",
            }
        ]

    profile = str(applicability.get("cycle_profile", "not_material"))
    gates = [
        {
            "gate": "Tech Cycle Applicability Gate",
            "status": "Not Applicable" if profile == "not_material" else "Passed",
            "comment": str(applicability.get("rationale", "")),
        }
    ]
    if profile == "not_material":
        return gates

    if not financial_history:
        for gate in applicability.get("required_gates", []):
            if gate != "Financial History Gate":
                gates.append({"gate": gate, "status": "Blocked", "comment": "Missing financial history packet."})
        return gates

    if profile == "physical_inventory":
        has_inventory = _has_any_metric(financial_history, ["inventory", "inventory_to_revenue"])
        has_capacity = _has_any_metric(financial_history, ["capex", "ppe", "depreciation_amortization", "capex_to_revenue"])
        gates.append(
            {
                "gate": "Inventory Cycle Gate",
                "status": "Passed" if has_inventory else "Limited",
                "comment": "Inventory history available from company filings." if has_inventory else "Inventory tags were not available; use IR or industry evidence before high-confidence margin normalization.",
            }
        )
        gates.append(
            {
                "gate": "Capacity Cycle Gate",
                "status": "Passed" if has_capacity else "Limited",
                "comment": "Capex / PP&E / depreciation evidence available." if has_capacity else "Capacity indicators are incomplete; capex-cycle stress should be low-confidence.",
            }
        )
    elif profile == "compute_capacity":
        has_capacity = _has_any_metric(financial_history, ["capex", "ppe", "depreciation_amortization", "capex_to_revenue"])
        gates.append(
            {
                "gate": "Compute Capacity Gate",
                "status": "Passed" if has_capacity else "Limited",
                "comment": "Capex / PP&E / depreciation history can constrain compute-capacity assumptions." if has_capacity else "Compute-capacity history is incomplete; capex monetization should be low-confidence.",
            }
        )
    elif profile == "subscription_budget":
        has_subscription = _has_any_metric(financial_history, ["deferred_revenue", "operating_cash_flow"])
        gates.append(
            {
                "gate": "Subscription Budget Cycle Gate",
                "status": "Passed" if has_subscription else "Limited",
                "comment": "Deferred revenue or operating cash flow history can constrain subscription growth." if has_subscription else "Deferred revenue / billings evidence is incomplete; RPO or retention disclosures should be requested.",
            }
        )
    elif profile == "advertising_demand":
        has_demand = _has_any_metric(financial_history, ["revenue", "operating_income", "operating_cash_flow"])
        gates.append(
            {
                "gate": "Advertising Demand Cycle Gate",
                "status": "Passed" if has_demand else "Limited",
                "comment": "Revenue and operating leverage history can constrain advertising demand assumptions." if has_demand else "Demand-cycle evidence is incomplete; external ad-market data would improve confidence.",
            }
        )
    else:
        gates.append(
            {
                "gate": "Technology Cycle Context Gate",
                "status": "Limited",
                "comment": f"Unknown or emerging tech cycle profile: {profile}.",
            }
        )

    return gates
