"""Audit data provenance for investment models."""

from typing import Any, Dict, List


REQUIRED_FIELDS_RAW = [
    "data_id",
    "metric",
    "value",
    "unit",
    "period",
    "source_name",
    "source_type",
    "source_date",
    "confidence",
    "raw_or_derived",
]


def audit_data_point(dp: Dict[str, Any]) -> List[str]:
    issues: List[str] = []

    for field in REQUIRED_FIELDS_RAW:
        if field not in dp or dp[field] in {None, ""}:
            issues.append(f"Missing required field: {field}")

    kind = dp.get("raw_or_derived")

    if kind == "raw":
        if not dp.get("source_url") and not dp.get("source_path"):
            issues.append("Raw data point lacks source_url or source_path.")
        if dp.get("source_type") == "AI-generated":
            issues.append("AI-generated data cannot be used as raw source data.")

    if kind == "derived":
        if not dp.get("formula"):
            issues.append("Derived metric lacks formula.")
        if not dp.get("input_data_ids"):
            issues.append("Derived metric lacks input_data_ids.")

    if kind == "assumption":
        if not dp.get("notes"):
            issues.append("Assumption should include rationale in notes.")

    return issues


def audit_dataset(data_points: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    for dp in data_points:
        issues = audit_data_point(dp)
        if issues:
            result[dp.get("data_id", "UNKNOWN_DATA_ID")] = issues
    return result


def can_use_for_valuation(data_points: List[Dict[str, Any]]) -> tuple[bool, Dict[str, List[str]]]:
    issues = audit_dataset(data_points)

    blocking = {}
    for data_id, problems in issues.items():
        for problem in problems:
            if "AI-generated" in problem or "lacks source_url" in problem or "lacks formula" in problem:
                blocking.setdefault(data_id, []).append(problem)

    return len(blocking) == 0, blocking
