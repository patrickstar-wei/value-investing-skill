"""Public data packet orchestrator for company analysis.

The builder gathers free or locally configured evidence into one auditable
packet. It does not estimate intrinsic value; valuation models should consume
the packet and still disclose assumptions separately.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Iterable, List

from scripts.connectors.ir_release_parser import parse_release
from scripts.connectors.openbb_provider_config import openbb_runtime_status
from scripts.connectors.sec_edgar_connector import (
    JsonFetcher as SECJsonFetcher,
    _fetch_json as sec_fetch_json,
    company_facts,
    filing_snapshot,
    latest_us_gaap_fact,
)
from scripts.connectors.yfinance_connector import JsonFetcher as MarketJsonFetcher
from scripts.connectors.yfinance_connector import _fetch_json as market_fetch_json
from scripts.connectors.yfinance_connector import get_market_quote


KEY_FACTS = (
    ("RevenueFromContractWithCustomerExcludingAssessedTax", "USD"),
    ("Revenues", "USD"),
    ("SalesRevenueNet", "USD"),
    ("NetIncomeLoss", "USD"),
    ("NetCashProvidedByUsedInOperatingActivities", "USD"),
    ("PaymentsToAcquirePropertyPlantAndEquipment", "USD"),
    ("Assets", "USD"),
    ("Liabilities", "USD"),
    ("StockholdersEquity", "USD"),
    ("EntityCommonStockSharesOutstanding", "shares"),
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append_error(errors: List[Dict[str, str]], stage: str, exc: Exception) -> None:
    errors.append({"stage": stage, "error": f"{type(exc).__name__}: {exc}"})


def _key_facts_from_companyfacts(payload: Dict[str, Any]) -> Dict[str, Any]:
    facts: Dict[str, Any] = {}
    for tag, unit in KEY_FACTS:
        fact = latest_us_gaap_fact(payload, tag, unit=unit, form_filter=["10-K", "10-Q"])
        if fact:
            facts[tag] = fact
    return facts


def build_public_data_packet(
    ticker: str,
    ir_sources: Iterable[str] | None = None,
    include_companyfacts: bool = True,
    sec_fetcher: SECJsonFetcher = sec_fetch_json,
    market_fetcher: MarketJsonFetcher = market_fetch_json,
    prefer_yfinance_package: bool = True,
    openbb_config_path: str | None = None,
) -> Dict[str, Any]:
    """Build a unified public data packet from available connectors.

    All connector failures are captured in `errors` instead of aborting the
    entire packet. This lets the analysis continue while clearly marking which
    public evidence was unavailable.
    """

    normalized = ticker.strip().upper()
    errors: List[Dict[str, str]] = []
    missing_data: List[str] = []
    sources_used: List[Dict[str, Any]] = []

    packet: Dict[str, Any] = {
        "ticker": normalized,
        "created_at": _now_iso(),
        "sources_used": sources_used,
        "market_quote": None,
        "sec": {"filing_snapshot": None, "facts": {}},
        "ir_releases": [],
        "openbb": None,
        "missing_data": missing_data,
        "stale_data": [],
        "errors": errors,
    }

    try:
        quote = get_market_quote(
            normalized,
            prefer_package=prefer_yfinance_package,
            fetcher=market_fetcher,
            analysis_as_of=packet["created_at"],
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
        if quote.get("market_cap") is None:
            missing_data.append("market_quote.market_cap")
        if quote.get("shares_outstanding") is None:
            missing_data.append("market_quote.shares_outstanding")
        if quote.get("price") is None:
            missing_data.append("market_quote.price")
        if not quote.get("regular_market_time"):
            missing_data.append("market_quote.regular_market_time")
        if quote.get("price") is not None and not quote.get("is_same_day"):
            packet["stale_data"].append("market_quote.price_not_same_day")
    except Exception as exc:  # pragma: no cover - exercised through mocked failure paths by callers
        _append_error(errors, "market_quote", exc)
        missing_data.append("market_quote")

    try:
        snapshot = filing_snapshot(normalized, fetcher=sec_fetcher)
        packet["sec"]["filing_snapshot"] = snapshot
        sources_used.append(
            {
                "name": "SEC EDGAR submissions API",
                "url": f"https://data.sec.gov/submissions/CIK{snapshot.get('cik', '')}.json",
                "source_tier": snapshot.get("source_tier"),
                "confidence": snapshot.get("confidence"),
            }
        )
    except Exception as exc:
        _append_error(errors, "sec_filings", exc)
        missing_data.append("sec.filing_snapshot")

    if include_companyfacts:
        try:
            facts_payload = company_facts(normalized, fetcher=sec_fetcher)
            facts = _key_facts_from_companyfacts(facts_payload)
            packet["sec"]["facts"] = facts
            sources_used.append(
                {
                    "name": "SEC EDGAR companyfacts API",
                    "url": f"https://data.sec.gov/api/xbrl/companyfacts/CIK{str(facts_payload.get('cik', '')).zfill(10)}.json",
                    "source_tier": 2,
                    "confidence": "high",
                }
            )
            if not facts:
                missing_data.append("sec.facts.key_us_gaap_tags")
        except Exception as exc:
            _append_error(errors, "sec_companyfacts", exc)
            missing_data.append("sec.facts")

    for source in ir_sources or []:
        try:
            parsed = parse_release(source)
            packet["ir_releases"].append(parsed)
            sources_used.append(
                {
                    "name": "Public IR release",
                    "url": source,
                    "source_tier": parsed.get("source_tier"),
                    "confidence": parsed.get("confidence"),
                }
            )
        except Exception as exc:
            _append_error(errors, f"ir_release:{source}", exc)

    try:
        packet["openbb"] = openbb_runtime_status(openbb_config_path)
    except Exception as exc:
        _append_error(errors, "openbb_runtime_status", exc)
        missing_data.append("openbb.status")

    return packet


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a public data packet for company analysis.")
    parser.add_argument("ticker", help="Company ticker, e.g. NVDA")
    parser.add_argument("--ir-url", action="append", default=[], help="Public IR release URL or local HTML/text file")
    parser.add_argument("--no-companyfacts", action="store_true", help="Skip SEC companyfacts retrieval")
    parser.add_argument("--no-yfinance-package", action="store_true", help="Use Yahoo endpoints directly")
    parser.add_argument("--openbb-config", default=None, help="Optional OpenBB provider config path")
    args = parser.parse_args()

    packet = build_public_data_packet(
        args.ticker,
        ir_sources=args.ir_url,
        include_companyfacts=not args.no_companyfacts,
        prefer_yfinance_package=not args.no_yfinance_package,
        openbb_config_path=args.openbb_config,
    )
    print(json.dumps(packet, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
