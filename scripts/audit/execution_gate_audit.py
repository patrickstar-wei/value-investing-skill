"""Execution gate audit helpers."""

from dataclasses import dataclass
from typing import Any, Dict, List

from scripts.markets.registry import detect_market
from scripts.validation.pe_validator import BLOCKED, PASS, validate_pe_calculation


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


def market_adapter_gate(ticker: str, packet: Dict[str, Any]) -> ExecutionGate:
    expected_market = detect_market(ticker)
    actual_market = packet.get("market")
    has_result = bool(actual_market and actual_market == expected_market)
    note = (
        f"Expected market adapter {expected_market}; packet market is {actual_market or 'missing'}."
        if not has_result
        else f"Ticker routed through {actual_market} market adapter."
    )
    return ExecutionGate(
        name="Market Adapter Gate",
        trigger=True,
        has_result=has_result,
        has_blocker=not has_result,
        severity="Critical",
        note=note,
    )


def pe_validation_gate(
    ticker: str,
    market_quote: Dict[str, Any] | None,
    financials: Dict[str, Any] | None,
    external_pe: Dict[str, float] | None = None,
) -> ExecutionGate:
    if not market_quote or not financials:
        return ExecutionGate(
            name="PE Validation Gate",
            trigger=True,
            has_result=False,
            has_blocker=True,
            severity="High",
            note="Market quote or TTM earnings inputs are missing.",
        )

    validation = validate_pe_calculation(
        ticker=ticker,
        market_quote=market_quote,
        financials=financials,
        external_pe=external_pe,
    )
    if validation.validation_status == PASS:
        status_note = f"P/E (TTM) validated at {validation.calculated_pe_ttm}x."
        return ExecutionGate(
            name="PE Validation Gate",
            trigger=True,
            has_result=True,
            has_blocker=False,
            severity="Medium",
            note=status_note,
        )
    anomaly_types = ", ".join(a.anomaly_type for a in validation.anomalies)
    return ExecutionGate(
        name="PE Validation Gate",
        trigger=True,
        has_result=validation.validation_status != BLOCKED,
        has_blocker=validation.validation_status == BLOCKED,
        severity="High" if validation.validation_status == BLOCKED else "Medium",
        note=f"P/E validation {validation.validation_status}: {anomaly_types}",
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
