"""A-share public data packet adapter.

This first-pass adapter intentionally blocks financial-history dependent
valuation when A-share filings have not been parsed. It prevents CN_A tickers
from silently falling through the SEC companyfacts path.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Dict, List

from scripts.connectors.yfinance_connector import JsonFetcher as MarketJsonFetcher
from scripts.connectors.yfinance_connector import _fetch_json as market_fetch_json
from scripts.connectors.yfinance_connector import get_market_quote
from scripts.markets.registry import MARKET_CN_A, normalize_ticker

CNFinancialFetcher = Callable[[str], Dict[str, Any] | None]


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _blocked_financial_history(ticker: str, reason: str) -> Dict[str, Any]:
    return {
        "ticker": ticker,
        "created_at": _now_iso(),
        "source": "CN_A exchange/CNINFO filings",
        "coverage": {
            "status": "blocked",
            "reason": reason,
        },
        "latest_financial_period": "",
        "metrics": {},
        "missing_metrics": [
            "revenue",
            "net_income",
            "operating_cash_flow",
            "capex",
            "assets",
            "liabilities",
            "equity",
            "shares_outstanding",
        ],
        "errors": [],
    }


def build_cn_a_public_data_packet(
    ticker: str,
    market_fetcher: MarketJsonFetcher = market_fetch_json,
    prefer_yfinance_package: bool = True,
    financial_fetcher: CNFinancialFetcher | None = None,
) -> Dict[str, Any]:
    """Build an A-share packet with explicit CN_A source boundaries."""

    normalized = normalize_ticker(ticker)
    created_at = _now_iso()
    errors: List[Dict[str, str]] = []
    missing_data: List[str] = []
    sources_used: List[Dict[str, Any]] = []
    stale_data: List[str] = []

    packet: Dict[str, Any] = {
        "ticker": normalized,
        "market": MARKET_CN_A,
        "created_at": created_at,
        "sources_used": sources_used,
        "market_quote": None,
        "sec": {"filing_snapshot": None, "facts": {}},
        "financial_history": None,
        "cn_a": {
            "announcements": [],
            "financials": None,
            "restatements": [],
            "adapter_status": "partial",
        },
        "tech_cycle_applicability": None,
        "execution_gate_checklist": [
            {
                "gate": "Market Adapter Gate",
                "status": "Passed",
                "comment": "CN_A ticker routed to A-share adapter; SEC companyfacts is not used as a financial primary source.",
            }
        ],
        "ir_releases": [],
        "openbb": None,
        "missing_data": missing_data,
        "stale_data": stale_data,
        "errors": errors,
    }

    try:
        quote = get_market_quote(
            normalized,
            prefer_package=prefer_yfinance_package,
            fetcher=market_fetcher,
            analysis_as_of=created_at,
        )
        packet["market_quote"] = quote
        sources_used.append(
            {
                "name": quote.get("source_name", "Yahoo Finance"),
                "url": quote.get("source_url", ""),
                "source_tier": quote.get("source_tier"),
                "confidence": quote.get("confidence"),
            }
        )
        for field in ("price", "market_cap", "shares_outstanding", "regular_market_time"):
            if quote.get(field) in (None, ""):
                missing_data.append(f"market_quote.{field}")
        if quote.get("price") is not None and not quote.get("is_same_day"):
            stale_data.append("market_quote.price_not_same_day")
    except Exception as exc:  # pragma: no cover - callers exercise through mocks
        errors.append({"stage": "market_quote", "error": f"{type(exc).__name__}: {exc}"})
        missing_data.append("market_quote")

    financials = financial_fetcher(normalized) if financial_fetcher is not None else None
    if financials:
        packet["cn_a"]["financials"] = financials
        packet["financial_history"] = financials.get("financial_history")
        sources_used.extend(financials.get("sources_used", []))
        packet["execution_gate_checklist"].append(
            {
                "gate": "Financial History Gate",
                "status": "Passed",
                "comment": "CN_A financial packet supplied by A-share adapter.",
            }
        )
    else:
        reason = (
            "CN_A financial statement adapter is required for current valuation. "
            "Do not use SEC companyfacts or generic WebSearch snippets for A-share financial history."
        )
        packet["financial_history"] = _blocked_financial_history(normalized, reason)
        missing_data.append("cn_a.financials")
        packet["execution_gate_checklist"].append(
            {
                "gate": "Financial History Gate",
                "status": "Blocked",
                "comment": reason,
            }
        )

    return packet
