"""Conformance tests for value investing skill outputs.

These tests are intentionally lightweight. They check structural consistency,
not investment correctness.
"""

from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class TestResult:
    name: str
    status: str
    severity: str
    note: str = ""


REQUIRED_TOP_LEVEL_KEYS = [
    "target_overview",
    "data_freshness_check",
    "data_provenance",
    "valuation_model_selection",
    "execution_gate_checklist",
    "final_view",
]


REQUIRED_GATES = [
    "Data Freshness",
    "Data Provenance",
    "Source Quality",
    "Primary Valuation",
    "Cross-check Valuation",
    "Downside Valuation",
    "Margin of Safety",
    "Execution Gate Audit",
]


def check_required_keys(report: Dict[str, Any]) -> TestResult:
    missing = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in report]
    if missing:
        return TestResult(
            name="Required top-level keys",
            status="Fail",
            severity="Critical",
            note=f"Missing keys: {missing}",
        )
    return TestResult("Required top-level keys", "Pass", "Critical")


def check_execution_gates(report: Dict[str, Any]) -> TestResult:
    gates = report.get("execution_gate_checklist", [])
    gate_names = {g.get("gate") or g.get("name") for g in gates if isinstance(g, dict)}
    missing = [gate for gate in REQUIRED_GATES if gate not in gate_names]
    if missing:
        return TestResult(
            name="Execution gates",
            status="Fail",
            severity="High",
            note=f"Missing gates: {missing}",
        )
    return TestResult("Execution gates", "Pass", "High")


def check_reverse_dcf_gate(report: Dict[str, Any]) -> TestResult:
    model_selection = report.get("valuation_model_selection", {})
    implied = str(model_selection.get("implied_expectation", "")).lower()
    if "reverse dcf" not in implied:
        return TestResult("Reverse DCF gate", "Not Applicable", "Medium")

    valuation_results = report.get("valuation_results", {})
    has_result = "reverse_dcf" in valuation_results
    has_blocked = "reverse_dcf_blocked" in valuation_results

    if has_result or has_blocked:
        return TestResult("Reverse DCF gate", "Pass", "High")

    return TestResult(
        "Reverse DCF gate",
        "Fail",
        "High",
        "Reverse DCF selected but no result or blocked section found.",
    )


def check_token_budget(manifest: Dict[str, Any]) -> TestResult:
    mode = manifest.get("run_mode", "L1")
    estimated = manifest.get("estimated_input_tokens", 0)
    budgets = {"L0": 4000, "L1": 12000, "L2": 30000, "L3": 50000}
    budget = budgets.get(mode, 12000)

    if estimated > budget:
        return TestResult(
            "Token budget",
            "Fail",
            "Medium",
            f"Estimated {estimated} tokens exceeds {mode} budget {budget}.",
        )
    return TestResult("Token budget", "Pass", "Medium")


def run_conformance_tests(report: Dict[str, Any], manifest: Dict[str, Any]) -> List[TestResult]:
    return [
        check_required_keys(report),
        check_execution_gates(report),
        check_reverse_dcf_gate(report),
        check_token_budget(manifest),
    ]


if __name__ == "__main__":
    sample_report = {
        "target_overview": {},
        "data_freshness_check": {},
        "data_provenance": {},
        "valuation_model_selection": {"implied_expectation": "Reverse DCF"},
        "valuation_results": {"reverse_dcf_blocked": {"reason": "Missing FCF"}},
        "execution_gate_checklist": [
            {"gate": "Data Freshness"},
            {"gate": "Data Provenance"},
            {"gate": "Source Quality"},
            {"gate": "Primary Valuation"},
            {"gate": "Cross-check Valuation"},
            {"gate": "Downside Valuation"},
            {"gate": "Margin of Safety"},
            {"gate": "Execution Gate Audit"},
        ],
        "final_view": {},
    }
    sample_manifest = {
        "run_mode": "L1",
        "estimated_input_tokens": 8000,
    }
    for result in run_conformance_tests(sample_report, sample_manifest):
        print(result)
