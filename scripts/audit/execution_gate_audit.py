"""Execution gate audit helpers."""

from dataclasses import dataclass
from typing import List


@dataclass
class ExecutionGate:
    name: str
    trigger: bool
    has_result: bool
    has_blocker: bool
    severity: str
    note: str = ""


@dataclass
class GateAuditResult:
    name: str
    status: str
    severity: str
    note: str


def audit_gates(gates: List[ExecutionGate]) -> List[GateAuditResult]:
    results: List[GateAuditResult] = []

    for gate in gates:
        if not gate.trigger:
            results.append(GateAuditResult(
                name=gate.name,
                status="Not Applicable",
                severity="None",
                note=gate.note,
            ))
            continue

        if gate.has_result:
            results.append(GateAuditResult(
                name=gate.name,
                status="Passed",
                severity=gate.severity,
                note=gate.note,
            ))
            continue

        if gate.has_blocker:
            results.append(GateAuditResult(
                name=gate.name,
                status="Blocked",
                severity=gate.severity,
                note=gate.note,
            ))
            continue

        results.append(GateAuditResult(
            name=gate.name,
            status="Silent Skip",
            severity=gate.severity,
            note=gate.note or "Gate was triggered but neither result nor blocker was provided.",
        ))

    return results


def has_critical_blocker(results: List[GateAuditResult]) -> bool:
    return any(
        r.severity.lower() == "critical" and r.status in {"Blocked", "Silent Skip"}
        for r in results
    )


if __name__ == "__main__":
    sample = [
        ExecutionGate(
            name="Reverse DCF",
            trigger=True,
            has_result=False,
            has_blocker=False,
            severity="High",
            note="Selected as implied-expectation model."
        ),
        ExecutionGate(
            name="Data Freshness",
            trigger=True,
            has_result=True,
            has_blocker=False,
            severity="Critical",
        ),
    ]
    for result in audit_gates(sample):
        print(result)
