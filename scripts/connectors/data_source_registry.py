"""Data source registry for value investing research."""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class DataSource:
    name: str
    tier: int
    description: str
    preferred_for: List[str]


DATA_SOURCES: Dict[str, DataSource] = {
    "company_filings": DataSource(
        name="company_filings",
        tier=2,
        description="Annual reports, 10-K, 10-Q, prospectus, exchange filings.",
        preferred_for=["financial_statements", "segments", "risk_factors"],
    ),
    "sec_edgar": DataSource(
        name="sec_edgar",
        tier=2,
        description="Free official SEC EDGAR submissions and companyfacts APIs.",
        preferred_for=["financial_statements", "segments", "risk_factors", "filings"],
    ),
    "public_data_packet": DataSource(
        name="public_data_packet",
        tier=2,
        description="Automatic packet built from SEC EDGAR, public market data, IR releases, and OpenBB readiness.",
        preferred_for=["analysis_packet", "financial_statements", "market_data", "management_guidance"],
    ),
    "company_ir_release": DataSource(
        name="company_ir_release",
        tier=2,
        description="Public company investor-relations pages, earnings releases, and presentations.",
        preferred_for=["earnings_release", "management_guidance", "events"],
    ),
    "openbb": DataSource(
        name="openbb",
        tier=3,
        description="Optional OpenBB data platform. Requires local install and provider keys for many datasets.",
        preferred_for=["market_data", "financial_data", "macro_data"],
    ),
    "yfinance": DataSource(
        name="yfinance",
        tier=3,
        description="Free market and financial data via Yahoo Finance.",
        preferred_for=["price", "market_cap", "basic_financials"],
    ),
    "news_web": DataSource(
        name="news_web",
        tier=4,
        description="News and web research.",
        preferred_for=["events", "sentiment", "background"],
    ),
    "user_input": DataSource(
        name="user_input",
        tier=5,
        description="User-provided assumptions or estimates.",
        preferred_for=["custom_assumptions"],
    ),
}


def get_source(name: str) -> Optional[DataSource]:
    return DATA_SOURCES.get(name)


def rank_sources(metric_type: str) -> List[DataSource]:
    candidates = []
    for source in DATA_SOURCES.values():
        if metric_type in source.preferred_for:
            candidates.append(source)
    return sorted(candidates, key=lambda s: s.tier)


if __name__ == "__main__":
    for src in rank_sources("financial_data"):
        print(src)
