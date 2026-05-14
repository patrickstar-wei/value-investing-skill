"""Generic data consistency checks for valuation inputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List


@dataclass
class ConsistencyIssue:
    issue_type: str
    severity: str
    message: str


def check_currency_consistency(items: Iterable[Dict[str, Any]]) -> List[ConsistencyIssue]:
    currencies = {str(item.get("currency") or "").upper() for item in items if item.get("currency")}
    if len(currencies) <= 1:
        return []
    return [
        ConsistencyIssue(
            issue_type="CURRENCY_MISMATCH",
            severity="CRITICAL",
            message=f"Multiple currencies found in one valuation input set: {sorted(currencies)}.",
        )
    ]


def check_required_source_ids(items: Iterable[Dict[str, Any]]) -> List[ConsistencyIssue]:
    issues: List[ConsistencyIssue] = []
    for item in items:
        metric = item.get("metric") or item.get("period") or "unknown"
        if not item.get("source_id") and not item.get("source_url"):
            issues.append(
                ConsistencyIssue(
                    issue_type="MISSING_SOURCE",
                    severity="HIGH",
                    message=f"{metric} is missing source_id/source_url.",
                )
            )
    return issues


def check_period_completeness(financials: Dict[str, Any], required_keys: Iterable[str]) -> List[ConsistencyIssue]:
    issues: List[ConsistencyIssue] = []
    for key in required_keys:
        if not financials.get(key):
            issues.append(
                ConsistencyIssue(
                    issue_type="MISSING_PERIOD_INPUT",
                    severity="CRITICAL",
                    message=f"Required financial period input is missing: {key}.",
                )
            )
    return issues
