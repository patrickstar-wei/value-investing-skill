"""SEC EDGAR connector for public company filings and XBRL facts.

The SEC API is free and public. It requires a descriptive User-Agent; set
SEC_USER_AGENT for production usage.
"""

from __future__ import annotations

import json
import os
import sys
import time
import gzip
from dataclasses import asdict, dataclass
from typing import Any, Callable, Dict, List
from urllib.request import Request, urlopen


SEC_BASE = "https://data.sec.gov"
SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
DEFAULT_USER_AGENT = "value-investing-skill/0.1 contact@example.com"


JsonFetcher = Callable[[str], Dict[str, Any]]


@dataclass
class SECFiling:
    accession_number: str
    form: str
    filing_date: str
    report_date: str
    primary_document: str
    source_url: str


def _user_agent() -> str:
    return os.environ.get("SEC_USER_AGENT", DEFAULT_USER_AGENT)


def _fetch_json(url: str, sleep_seconds: float = 0.1) -> Dict[str, Any]:
    request = Request(url, headers={"User-Agent": _user_agent(), "Accept-Encoding": "gzip, deflate"})
    with urlopen(request, timeout=30) as response:
        payload = response.read()
    if payload[:2] == b"\x1f\x8b":
        payload = gzip.decompress(payload)
    if sleep_seconds:
        time.sleep(sleep_seconds)
    return json.loads(payload.decode("utf-8"))


def _cik10(cik: int | str) -> str:
    return str(cik).strip().zfill(10)


def ticker_to_cik(ticker: str, fetcher: JsonFetcher = _fetch_json) -> str:
    """Resolve a ticker to a zero-padded SEC CIK."""

    normalized = ticker.strip().upper().replace(".", "-")
    data = fetcher(SEC_TICKERS_URL)
    for entry in data.values():
        if str(entry.get("ticker", "")).upper() == normalized:
            return _cik10(entry["cik_str"])
    raise ValueError(f"Ticker not found in SEC company_tickers.json: {ticker}")


def company_submissions(ticker_or_cik: str, fetcher: JsonFetcher = _fetch_json) -> Dict[str, Any]:
    cik = ticker_to_cik(ticker_or_cik, fetcher) if not ticker_or_cik.isdigit() else _cik10(ticker_or_cik)
    return fetcher(f"{SEC_BASE}/submissions/CIK{cik}.json")


def company_facts(ticker_or_cik: str, fetcher: JsonFetcher = _fetch_json) -> Dict[str, Any]:
    cik = ticker_to_cik(ticker_or_cik, fetcher) if not ticker_or_cik.isdigit() else _cik10(ticker_or_cik)
    return fetcher(f"{SEC_BASE}/api/xbrl/companyfacts/CIK{cik}.json")


def recent_filings(submissions: Dict[str, Any], forms: List[str] | None = None, limit: int = 10) -> List[Dict[str, Any]]:
    """Return recent filing rows from a submissions payload."""

    recent = submissions.get("filings", {}).get("recent", {})
    forms_filter = {form.upper() for form in forms or []}
    rows = []
    accessions = recent.get("accessionNumber", [])
    for idx, accession in enumerate(accessions):
        form = recent.get("form", [""])[idx]
        if forms_filter and form.upper() not in forms_filter:
            continue
        cik = str(submissions.get("cik", "")).zfill(10)
        accession_clean = accession.replace("-", "")
        primary_doc = recent.get("primaryDocument", [""])[idx]
        rows.append(
            asdict(
                SECFiling(
                    accession_number=accession,
                    form=form,
                    filing_date=recent.get("filingDate", [""])[idx],
                    report_date=recent.get("reportDate", [""])[idx],
                    primary_document=primary_doc,
                    source_url=f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession_clean}/{primary_doc}",
                )
            )
        )
        if len(rows) >= limit:
            break
    return rows


def latest_filing(ticker_or_cik: str, forms: List[str] | None = None, fetcher: JsonFetcher = _fetch_json) -> Dict[str, Any]:
    filings = recent_filings(company_submissions(ticker_or_cik, fetcher), forms=forms, limit=1)
    if not filings:
        raise ValueError(f"No matching SEC filings found for {ticker_or_cik}")
    return filings[0]


def latest_us_gaap_fact(
    facts_payload: Dict[str, Any],
    tag: str,
    unit: str = "USD",
    form_filter: List[str] | None = None,
) -> Dict[str, Any] | None:
    """Extract the latest reported US-GAAP fact for a tag and unit."""

    tag_payload = facts_payload.get("facts", {}).get("us-gaap", {}).get(tag, {})
    units = tag_payload.get("units", {})
    values = units.get(unit)
    if not values:
        return None
    forms = {form.upper() for form in form_filter or []}
    candidates = [
        item
        for item in values
        if item.get("val") is not None and (not forms or str(item.get("form", "")).upper() in forms)
    ]
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item.get("end", ""), item.get("filed", "")), reverse=True)
    latest = dict(candidates[0])
    latest["taxonomy"] = "us-gaap"
    latest["tag"] = tag
    latest["unit"] = unit
    latest["source_type"] = "SEC EDGAR companyfacts"
    latest["source_tier"] = 2
    latest["confidence"] = "high"
    return latest


def filing_snapshot(ticker_or_cik: str, fetcher: JsonFetcher = _fetch_json) -> Dict[str, Any]:
    """Small public-data packet for a US-listed company."""

    submissions = company_submissions(ticker_or_cik, fetcher)
    forms = ["10-K", "10-Q", "8-K"]
    return {
        "ticker_or_cik": ticker_or_cik,
        "cik": _cik10(submissions.get("cik", "")),
        "company_name": submissions.get("name", ""),
        "latest_filings": recent_filings(submissions, forms=forms, limit=10),
        "source": "SEC EDGAR submissions API",
        "source_tier": 2,
        "confidence": "high",
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python -m scripts.connectors.sec_edgar_connector <ticker-or-cik> [form]")
    form = [sys.argv[2]] if len(sys.argv) > 2 else None
    result = latest_filing(sys.argv[1], forms=form)
    print(json.dumps(result, indent=2))
