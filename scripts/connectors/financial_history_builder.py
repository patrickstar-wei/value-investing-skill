"""Build normalized financial history from SEC companyfacts.

The builder is intentionally conservative. SEC XBRL facts are noisy across
companies, tags, fiscal calendars, and period frames, so this module prefers a
clearly sourced limited history over silently manufacturing complete series.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Sequence

from scripts.connectors.sec_edgar_connector import JsonFetcher, _fetch_json, company_facts


MetricSpec = Dict[str, Any]


METRIC_SPECS: Dict[str, MetricSpec] = {
    "revenue": {
        "tags": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"],
        "unit": "USD",
        "kind": "duration",
    },
    "cost_of_revenue": {
        "tags": ["CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfGoodsSold"],
        "unit": "USD",
        "kind": "duration",
    },
    "gross_profit": {"tags": ["GrossProfit"], "unit": "USD", "kind": "duration"},
    "operating_income": {"tags": ["OperatingIncomeLoss"], "unit": "USD", "kind": "duration"},
    "net_income": {"tags": ["NetIncomeLoss"], "unit": "USD", "kind": "duration"},
    "operating_cash_flow": {
        "tags": ["NetCashProvidedByUsedInOperatingActivities"],
        "unit": "USD",
        "kind": "duration",
    },
    "capex": {
        "tags": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
        "unit": "USD",
        "kind": "duration",
    },
    "depreciation_amortization": {
        "tags": ["DepreciationDepletionAndAmortization", "DepreciationDepletionAndAmortizationExpense"],
        "unit": "USD",
        "kind": "duration",
    },
    "inventory": {"tags": ["InventoryNet"], "unit": "USD", "kind": "instant"},
    "receivables": {
        "tags": ["AccountsReceivableNetCurrent", "AccountsReceivableNet"],
        "unit": "USD",
        "kind": "instant",
    },
    "ppe": {"tags": ["PropertyPlantAndEquipmentNet"], "unit": "USD", "kind": "instant"},
    "deferred_revenue": {
        "tags": ["ContractWithCustomerLiabilityCurrent", "ContractWithCustomerLiability"],
        "unit": "USD",
        "kind": "instant",
    },
    "assets": {"tags": ["Assets"], "unit": "USD", "kind": "instant"},
    "liabilities": {"tags": ["Liabilities"], "unit": "USD", "kind": "instant"},
    "equity": {"tags": ["StockholdersEquity"], "unit": "USD", "kind": "instant"},
    "shares_outstanding": {
        "tags": ["EntityCommonStockSharesOutstanding"],
        "unit": "shares",
        "kind": "instant",
    },
}


DERIVED_METRICS = {
    "free_cash_flow": {
        "inputs": ["operating_cash_flow", "capex"],
        "formula": "operating_cash_flow - capex",
        "unit": "USD",
    },
    "gross_margin": {
        "inputs": ["gross_profit", "revenue"],
        "formula": "gross_profit / revenue",
        "unit": "ratio",
    },
    "capex_to_revenue": {
        "inputs": ["capex", "revenue"],
        "formula": "capex / revenue",
        "unit": "ratio",
    },
    "inventory_to_revenue": {
        "inputs": ["inventory", "revenue"],
        "formula": "inventory / revenue",
        "unit": "ratio",
    },
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_year(value: Any) -> str:
    if value in (None, ""):
        return ""
    try:
        return str(int(value))
    except (TypeError, ValueError):
        return str(value)


def _frame_period(item: Dict[str, Any]) -> str:
    frame = str(item.get("frame") or "")
    if frame.startswith("CY"):
        period = frame.replace("CY", "FY", 1)
        if "Q" in period and "-Q" not in period:
            period = period.replace("Q", "-Q", 1)
        return period
    fy = _normalize_year(item.get("fy"))
    fp = str(item.get("fp") or "")
    if fy and fp:
        return f"FY{fy}" if fp == "FY" else f"FY{fy}-{fp}"
    if item.get("end"):
        return str(item["end"])
    return "unknown"


def _duration_days(item: Dict[str, Any]) -> int | None:
    try:
        start = datetime.fromisoformat(str(item.get("start"))).date()
        end = datetime.fromisoformat(str(item.get("end"))).date()
    except (TypeError, ValueError):
        return None
    return (end - start).days + 1


def _is_annual_fact(item: Dict[str, Any], kind: str) -> bool:
    form = str(item.get("form", "")).upper()
    if form != "10-K":
        return False
    frame = str(item.get("frame") or "")
    if frame.startswith("CY") and "Q" not in frame:
        return True
    fp = str(item.get("fp") or "")
    if fp == "FY":
        return True
    if kind == "instant" and item.get("end"):
        return True
    days = _duration_days(item)
    return days is not None and days >= 300


def _is_quarter_fact(item: Dict[str, Any], kind: str) -> bool:
    form = str(item.get("form", "")).upper()
    if form not in {"10-Q", "10-K"}:
        return False
    frame = str(item.get("frame") or "")
    if "Q" in frame:
        return True
    fp = str(item.get("fp") or "")
    if fp in {"Q1", "Q2", "Q3", "Q4"}:
        return True
    if kind == "instant" and form == "10-Q":
        return True
    days = _duration_days(item)
    return days is not None and 60 <= days <= 120


def _dedupe_latest(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_period: Dict[str, Dict[str, Any]] = {}
    for item in items:
        if item.get("val") is None or not item.get("end"):
            continue
        period = _frame_period(item)
        current = by_period.get(period)
        if current is None or (str(item.get("filed", "")), str(item.get("end", ""))) > (
            str(current.get("filed", "")),
            str(current.get("end", "")),
        ):
            by_period[period] = dict(item)
    return sorted(by_period.values(), key=lambda row: (str(row.get("end", "")), str(row.get("filed", ""))), reverse=True)


def _values_for_tag(facts_payload: Dict[str, Any], tag: str, unit: str) -> Sequence[Dict[str, Any]]:
    tag_payload = facts_payload.get("facts", {}).get("us-gaap", {}).get(tag, {})
    return tag_payload.get("units", {}).get(unit, [])


def _extract_metric_series(
    facts_payload: Dict[str, Any],
    metric: str,
    spec: MetricSpec,
    annual_years: int,
    quarter_count: int,
) -> Dict[str, Any]:
    unit = str(spec["unit"])
    kind = str(spec["kind"])
    selected_tag = ""
    raw_values: Sequence[Dict[str, Any]] = []
    for tag in spec["tags"]:
        values = _values_for_tag(facts_payload, tag, unit)
        if values:
            selected_tag = tag
            raw_values = values
            break

    annual = _dedupe_latest(item for item in raw_values if _is_annual_fact(item, kind))[:annual_years]
    quarterly = _dedupe_latest(item for item in raw_values if _is_quarter_fact(item, kind))[:quarter_count]

    def convert(item: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "period": _frame_period(item),
            "end": item.get("end", ""),
            "filed": item.get("filed", ""),
            "form": item.get("form", ""),
            "fy": item.get("fy", ""),
            "fp": item.get("fp", ""),
            "value": item.get("val"),
            "unit": unit,
            "tag": selected_tag,
            "kind": kind,
            "source_type": "SEC EDGAR companyfacts",
            "source_tier": 2,
            "confidence": "high",
        }

    return {
        "metric": metric,
        "tag": selected_tag,
        "kind": kind,
        "unit": unit,
        "annual": [convert(item) for item in annual],
        "quarterly": [convert(item) for item in quarterly],
        "missing": not bool(selected_tag),
    }


def _by_end(series: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(item.get("end", "")): item for item in series if item.get("end")}


def _derive_binary_metric(
    metrics: Dict[str, Dict[str, Any]],
    metric_name: str,
    left_metric: str,
    right_metric: str,
    formula: str,
    unit: str,
) -> Dict[str, Any]:
    result = {
        "metric": metric_name,
        "tag": "",
        "kind": "derived",
        "unit": unit,
        "annual": [],
        "quarterly": [],
        "missing": False,
        "formula": formula,
    }
    for bucket in ("annual", "quarterly"):
        left_by_end = _by_end(metrics.get(left_metric, {}).get(bucket, []))
        right_by_end = _by_end(metrics.get(right_metric, {}).get(bucket, []))
        rows = []
        for end, left in left_by_end.items():
            right = right_by_end.get(end)
            if right is None:
                continue
            try:
                left_value = float(left["value"])
                right_value = float(right["value"])
            except (TypeError, ValueError):
                continue
            if metric_name in {"gross_margin", "capex_to_revenue", "inventory_to_revenue"}:
                if right_value == 0:
                    continue
                value = left_value / right_value
            else:
                value = left_value - right_value
            rows.append(
                {
                    "period": left.get("period", end),
                    "end": end,
                    "filed": max(str(left.get("filed", "")), str(right.get("filed", ""))),
                    "form": left.get("form", right.get("form", "")),
                    "value": value,
                    "unit": unit,
                    "kind": "derived",
                    "formula": formula,
                    "input_metrics": [left_metric, right_metric],
                    "source_type": "derived_from_SEC_EDGAR_companyfacts",
                    "source_tier": 2,
                    "confidence": "medium",
                }
            )
        result[bucket] = sorted(rows, key=lambda row: (str(row.get("end", "")), str(row.get("filed", ""))), reverse=True)
    result["missing"] = not result["annual"] and not result["quarterly"]
    return result


def _derive_metrics(metrics: Dict[str, Dict[str, Any]]) -> None:
    for metric_name, spec in DERIVED_METRICS.items():
        inputs = spec["inputs"]
        metrics[metric_name] = _derive_binary_metric(
            metrics,
            metric_name,
            inputs[0],
            inputs[1],
            spec["formula"],
            spec["unit"],
        )


def _coverage(metrics: Dict[str, Dict[str, Any]], annual_target: int, quarter_target: int) -> Dict[str, Any]:
    core = ["revenue", "net_income", "operating_cash_flow", "capex"]
    annual_counts = {metric: len(metrics.get(metric, {}).get("annual", [])) for metric in core}
    quarter_counts = {metric: len(metrics.get(metric, {}).get("quarterly", [])) for metric in core}
    annual_min = min(annual_counts.values()) if annual_counts else 0
    quarter_min = min(quarter_counts.values()) if quarter_counts else 0

    if annual_min >= min(5, annual_target) and quarter_min >= min(8, quarter_target):
        status = "passed"
    elif annual_min >= 3 or quarter_min >= 4:
        status = "limited"
    else:
        status = "blocked"

    return {
        "status": status,
        "annual_target_years": annual_target,
        "quarter_target_count": quarter_target,
        "core_annual_periods_min": annual_min,
        "core_quarterly_periods_min": quarter_min,
        "core_annual_counts": annual_counts,
        "core_quarterly_counts": quarter_counts,
    }


def _latest_period(metrics: Dict[str, Dict[str, Any]]) -> str:
    candidates = []
    for metric in ("revenue", "net_income", "operating_cash_flow"):
        candidates.extend(metrics.get(metric, {}).get("quarterly", []))
        candidates.extend(metrics.get(metric, {}).get("annual", []))
    if not candidates:
        return ""
    latest = max(candidates, key=lambda item: (str(item.get("end", "")), str(item.get("filed", ""))))
    return str(latest.get("period") or latest.get("end") or "")


def build_financial_history(
    ticker: str,
    facts_payload: Dict[str, Any] | None = None,
    annual_years: int = 10,
    quarter_count: int = 12,
    fetcher: JsonFetcher = _fetch_json,
) -> Dict[str, Any]:
    """Return a conservative financial history packet for a US-listed company."""

    normalized = ticker.strip().upper()
    errors: List[Dict[str, str]] = []
    if facts_payload is None:
        try:
            facts_payload = company_facts(normalized, fetcher=fetcher)
        except Exception as exc:  # noqa: BLE001 - caller needs a blocker instead of a crash.
            return {
                "ticker": normalized,
                "created_at": _now_iso(),
                "source": "SEC EDGAR companyfacts",
                "coverage": {
                    "status": "blocked",
                    "annual_target_years": annual_years,
                    "quarter_target_count": quarter_count,
                    "core_annual_periods_min": 0,
                    "core_quarterly_periods_min": 0,
                },
                "latest_financial_period": "",
                "metrics": {},
                "missing_metrics": sorted(METRIC_SPECS),
                "errors": [{"stage": "sec_companyfacts", "error": f"{type(exc).__name__}: {exc}"}],
            }

    metrics: Dict[str, Dict[str, Any]] = {}
    for metric, spec in METRIC_SPECS.items():
        metrics[metric] = _extract_metric_series(facts_payload, metric, spec, annual_years, quarter_count)
    _derive_metrics(metrics)

    missing = sorted(metric for metric, payload in metrics.items() if payload.get("missing"))
    return {
        "ticker": normalized,
        "created_at": _now_iso(),
        "source": "SEC EDGAR companyfacts",
        "source_tier": 2,
        "confidence": "high" if not missing else "medium",
        "coverage": _coverage(metrics, annual_years, quarter_count),
        "latest_financial_period": _latest_period(metrics),
        "metrics": metrics,
        "missing_metrics": missing,
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build SEC companyfacts financial history.")
    parser.add_argument("ticker", help="Ticker, e.g. NVDA")
    parser.add_argument("--annual-years", type=int, default=10)
    parser.add_argument("--quarters", type=int, default=12)
    args = parser.parse_args()
    print(
        json.dumps(
            build_financial_history(args.ticker, annual_years=args.annual_years, quarter_count=args.quarters),
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
