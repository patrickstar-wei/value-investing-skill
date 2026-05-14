"""P/E ratio validation from source-linked market and earnings inputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


PASS = "PASS"
WARNING = "WARNING"
BLOCKED = "BLOCKED"


@dataclass
class AnomalyRecord:
    anomaly_type: str
    severity: str
    description: str
    recommended_action: str
    evidence: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TTMEarningsBreakdown:
    total: float | None
    currency: str
    periods: List[str]
    formula: str
    source_ids: List[str] = field(default_factory=list)
    restatement_status: str = "not_checked"


@dataclass
class PEValidationResult:
    validation_status: str
    confidence: str
    calculated_pe_ttm: float | None = None
    ttm_earnings_breakdown: TTMEarningsBreakdown | None = None
    anomalies: List[AnomalyRecord] = field(default_factory=list)
    source_comparison: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


def validate_pe_calculation(
    ticker: str,
    market_quote: Dict[str, Any],
    financials: Dict[str, Any],
    analysis_date: str | None = None,
    external_pe: Dict[str, float] | None = None,
    tolerance: float = 0.20,
) -> PEValidationResult:
    """Validate P/E (TTM) using auditable numerator and denominator inputs.

    `financials` accepts either:
    - `ttm_net_income`, or
    - `annual.net_income + current_quarter.net_income - prior_year_same_quarter.net_income`.

    All money values must be in base currency units, not millions or hundred
    millions. Adapters should normalize units before calling this validator.
    """

    result = PEValidationResult(validation_status=PASS, confidence="HIGH")
    market_cap = _to_float(market_quote.get("market_cap"))
    if market_cap is None or market_cap <= 0:
        _block(result, "MISSING_MARKET_CAP", "Market cap is missing or invalid.", "Fetch a valid same-day market cap.")
        return _finish(result)

    market_currency = str(market_quote.get("currency") or financials.get("currency") or "").upper()
    breakdown = _calculate_ttm_earnings(financials)
    result.ttm_earnings_breakdown = breakdown
    if breakdown.total is None or breakdown.total <= 0:
        _block(result, "INVALID_TTM_EARNINGS", "TTM net income is missing, incomplete, or non-positive.", "Build TTM earnings from source filings before calculating P/E.")
        return _finish(result)

    if market_currency and breakdown.currency and market_currency != breakdown.currency:
        _block(
            result,
            "CURRENCY_MISMATCH",
            f"Market cap currency ({market_currency}) differs from earnings currency ({breakdown.currency}).",
            "Convert market cap and earnings to one currency with an auditable FX date.",
        )
        return _finish(result)

    if breakdown.restatement_status in {"unadjusted", "affected_not_adjusted"}:
        _block(
            result,
            "UNADJUSTED_RESTATEMENT",
            "TTM earnings are affected by a restatement or accounting correction but were not adjusted.",
            "Use post-restatement figures or block current valuation.",
            {"restatement_status": breakdown.restatement_status},
        )
        return _finish(result)
    if breakdown.restatement_status == "adjusted":
        _warn(
            result,
            "RESTATEMENT_ADJUSTED",
            "TTM earnings include post-restatement adjusted figures.",
            "Disclose the restatement and keep data confidence no higher than medium.",
        )

    result.calculated_pe_ttm = round(market_cap / breakdown.total, 2)
    source_pes = external_pe or {}
    result.source_comparison = {
        "calculated_pe": result.calculated_pe_ttm,
        "source_pes": source_pes,
        "tolerance": tolerance,
    }
    for source_name, source_pe in source_pes.items():
        source_pe_float = _to_float(source_pe)
        if source_pe_float is None or source_pe_float <= 0:
            continue
        variance = abs(result.calculated_pe_ttm - source_pe_float) / source_pe_float
        if variance > tolerance:
            _warn(
                result,
                "PE_SOURCE_VARIANCE",
                f"Calculated P/E differs from {source_name} by {variance:.1%}.",
                "Investigate market cap, share count, TTM earnings, and restatement treatment.",
                {"source": source_name, "source_pe": source_pe_float, "variance": variance},
            )

    return _finish(result)


def _calculate_ttm_earnings(financials: Dict[str, Any]) -> TTMEarningsBreakdown:
    currency = str(financials.get("currency") or "").upper()
    restatement_status = str(financials.get("restatement_status") or "not_checked")

    direct_ttm = _to_float(financials.get("ttm_net_income"))
    if direct_ttm is not None:
        return TTMEarningsBreakdown(
            total=direct_ttm,
            currency=currency,
            periods=list(financials.get("periods_used", ["TTM"])),
            formula="ttm_net_income",
            source_ids=list(financials.get("source_ids", [])),
            restatement_status=restatement_status,
        )

    annual = financials.get("annual", {})
    current_quarter = financials.get("current_quarter", {})
    prior_year_same_quarter = financials.get("prior_year_same_quarter", {})
    annual_ni = _to_float(annual.get("net_income"))
    current_ni = _to_float(current_quarter.get("net_income"))
    prior_ni = _to_float(prior_year_same_quarter.get("net_income"))
    periods = [
        str(annual.get("period") or "annual"),
        str(current_quarter.get("period") or "current_quarter"),
        str(prior_year_same_quarter.get("period") or "prior_year_same_quarter"),
    ]
    source_ids = [
        value
        for value in [
            annual.get("source_id"),
            current_quarter.get("source_id"),
            prior_year_same_quarter.get("source_id"),
        ]
        if value
    ]
    if annual_ni is None or current_ni is None or prior_ni is None:
        return TTMEarningsBreakdown(
            total=None,
            currency=currency,
            periods=periods,
            formula="annual + current_quarter - prior_year_same_quarter",
            source_ids=source_ids,
            restatement_status=restatement_status,
        )
    return TTMEarningsBreakdown(
        total=annual_ni + current_ni - prior_ni,
        currency=currency,
        periods=periods,
        formula="annual + current_quarter - prior_year_same_quarter",
        source_ids=source_ids,
        restatement_status=restatement_status,
    )


def _block(
    result: PEValidationResult,
    anomaly_type: str,
    description: str,
    recommended_action: str,
    evidence: Dict[str, Any] | None = None,
) -> None:
    result.validation_status = BLOCKED
    result.confidence = BLOCKED
    result.anomalies.append(
        AnomalyRecord(
            anomaly_type=anomaly_type,
            severity="CRITICAL",
            description=description,
            recommended_action=recommended_action,
            evidence=evidence or {},
        )
    )


def _warn(
    result: PEValidationResult,
    anomaly_type: str,
    description: str,
    recommended_action: str,
    evidence: Dict[str, Any] | None = None,
) -> None:
    if result.validation_status != BLOCKED:
        result.validation_status = WARNING
        result.confidence = "MEDIUM"
    result.anomalies.append(
        AnomalyRecord(
            anomaly_type=anomaly_type,
            severity="WARNING",
            description=description,
            recommended_action=recommended_action,
            evidence=evidence or {},
        )
    )


def _finish(result: PEValidationResult) -> PEValidationResult:
    if result.validation_status == BLOCKED:
        result.recommendations.append("BLOCKED: do not use P/E or current valuation until critical inputs are fixed.")
    elif result.validation_status == WARNING:
        result.recommendations.append("WARNING: disclose anomalies and downgrade confidence.")
    else:
        result.recommendations.append("PASS: P/E (TTM) inputs are internally consistent.")
    return result


def _to_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
