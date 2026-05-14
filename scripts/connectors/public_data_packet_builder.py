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

from scripts.audit.tech_cycle_context_audit import financial_history_gate, tech_cycle_context_gates
from scripts.connectors.financial_history_builder import build_financial_history
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
from scripts.markets.cn_a.adapter import CNFinancialFetcher, build_cn_a_public_data_packet
from scripts.markets.registry import MARKET_CN_A, detect_market
from scripts.routing.select_valuation_models import CompanyProfile
from scripts.routing.tech_cycle_applicability import select_tech_cycle_applicability


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
    include_financial_history: bool = True,
    company_profile: CompanyProfile | None = None,
    sec_fetcher: SECJsonFetcher = sec_fetch_json,
    market_fetcher: MarketJsonFetcher = market_fetch_json,
    prefer_yfinance_package: bool = True,
    openbb_config_path: str | None = None,
    cn_a_financial_fetcher: CNFinancialFetcher | None = None,
) -> Dict[str, Any]:
    """Build a unified public data packet from available connectors.

    All connector failures are captured in `errors` instead of aborting the
    entire packet. This lets the analysis continue while clearly marking which
    public evidence was unavailable.
    """

    normalized = ticker.strip().upper()
    market = detect_market(normalized)
    if market == MARKET_CN_A:
        return build_cn_a_public_data_packet(
            normalized,
            market_fetcher=market_fetcher,
            prefer_yfinance_package=prefer_yfinance_package,
            financial_fetcher=cn_a_financial_fetcher,
        )

    errors: List[Dict[str, str]] = []
    missing_data: List[str] = []
    sources_used: List[Dict[str, Any]] = []

    packet: Dict[str, Any] = {
        "ticker": normalized,
        "market": market,
        "created_at": _now_iso(),
        "sources_used": sources_used,
        "market_quote": None,
        "sec": {"filing_snapshot": None, "facts": {}},
        "financial_history": None,
        "tech_cycle_applicability": None,
        "execution_gate_checklist": [],
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

    facts_payload: Dict[str, Any] | None = None
    if include_companyfacts or include_financial_history:
        try:
            facts_payload = company_facts(normalized, fetcher=sec_fetcher)
        except Exception as exc:
            _append_error(errors, "sec_companyfacts", exc)
            missing_data.append("sec.facts")

    if include_companyfacts and facts_payload is not None:
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

    if include_financial_history:
        history = build_financial_history(normalized, facts_payload=facts_payload, fetcher=sec_fetcher)
        packet["financial_history"] = history
        packet["execution_gate_checklist"].append(financial_history_gate(history))
        if history.get("coverage", {}).get("status") == "blocked":
            missing_data.append("financial_history")
        if history.get("latest_financial_period"):
            packet["latest_financial_period"] = history["latest_financial_period"]

    if company_profile is not None:
        applicability = select_tech_cycle_applicability(company_profile).to_dict()
        packet["tech_cycle_applicability"] = applicability
        packet["execution_gate_checklist"].extend(
            tech_cycle_context_gates(applicability, packet.get("financial_history"))
        )

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
    parser.add_argument("--no-financial-history", action="store_true", help="Skip SEC companyfacts financial history builder")
    parser.add_argument("--no-yfinance-package", action="store_true", help="Use Yahoo endpoints directly")
    parser.add_argument("--openbb-config", default=None, help="Optional OpenBB provider config path")
    args = parser.parse_args()

    packet = build_public_data_packet(
        args.ticker,
        ir_sources=args.ir_url,
        include_companyfacts=not args.no_companyfacts,
        include_financial_history=not args.no_financial_history,
        prefer_yfinance_package=not args.no_yfinance_package,
        openbb_config_path=args.openbb_config,
    )
    print(json.dumps(packet, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
