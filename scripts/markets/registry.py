"""Market detection helpers for listed-company analysis."""

from __future__ import annotations

import re


MARKET_US = "US"
MARKET_CN_A = "CN_A"
MARKET_HK = "HK"
MARKET_UNKNOWN = "UNKNOWN"


def detect_market(ticker: str) -> str:
    """Return the market adapter key for a ticker symbol."""

    normalized = ticker.strip().upper()
    if re.fullmatch(r"\d{6}\.(SZ|SH|SZSE|SHSE)", normalized):
        return MARKET_CN_A
    if re.fullmatch(r"\d{6}", normalized):
        if normalized.startswith(("0", "3", "6")):
            return MARKET_CN_A
    if re.fullmatch(r"\d{4,5}\.(HK|HKEX)", normalized):
        return MARKET_HK
    if re.fullmatch(r"[A-Z][A-Z0-9.\-]{0,9}", normalized):
        return MARKET_US
    return MARKET_UNKNOWN


def normalize_ticker(ticker: str) -> str:
    """Normalize ticker casing without converting exchange suffixes."""

    return ticker.strip().upper()
