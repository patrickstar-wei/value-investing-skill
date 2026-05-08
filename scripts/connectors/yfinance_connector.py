"""Yahoo/yfinance market data connector.

This connector uses the optional `yfinance` package when it is installed.
If not, it falls back to Yahoo Finance's public quote endpoint. Yahoo data is
third-party data and should be cross-checked for high-stakes valuation work.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from tempfile import gettempdir
from typing import Any, Callable, Dict
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


YAHOO_QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart"
JsonFetcher = Callable[[str], Dict[str, Any]]
PackageInstaller = Callable[[], bool]


@dataclass
class MarketQuote:
    ticker: str
    price: float | None
    currency: str
    market_cap: float | None
    shares_outstanding: float | None
    previous_close: float | None
    regular_market_time: str
    analysis_as_of: str
    price_date_status: str
    is_same_day: bool
    staleness_minutes: float | None
    market_session_note: str
    source_name: str
    source_url: str
    source_type: str
    source_tier: int
    confidence: str
    retrieval_timestamp: str
    notes: str = ""


def _fetch_json(url: str) -> Dict[str, Any]:
    request = Request(url, headers={"User-Agent": "value-investing-skill/0.1"})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _price_freshness_fields(regular_market_time: str, analysis_as_of: str) -> Dict[str, Any]:
    market_dt = _parse_iso_datetime(regular_market_time)
    analysis_dt = _parse_iso_datetime(analysis_as_of) or datetime.now(timezone.utc)
    if market_dt is None:
        return {
            "price_date_status": "missing_market_time",
            "is_same_day": False,
            "staleness_minutes": None,
            "market_session_note": "Market time is missing; price cannot be treated as same-day current data.",
        }

    same_day = market_dt.date() == analysis_dt.date()
    staleness_minutes = max(0.0, (analysis_dt - market_dt).total_seconds() / 60)
    if same_day:
        status = "same_day"
        note = "Price market timestamp is on the analysis date; use as same-day market data and disclose the exact timestamp."
    else:
        status = "not_same_day"
        note = "Price market timestamp is not on the analysis date; block current valuation or label price as stale."
    return {
        "price_date_status": status,
        "is_same_day": same_day,
        "staleness_minutes": round(staleness_minutes, 2),
        "market_session_note": note,
    }


def _install_yfinance_package() -> bool:
    """Best-effort install for sandboxed runtimes.

    This avoids replacing a market quote with WebSearch snippets when the
    optional yfinance package is absent. The package is installed into a
    sandbox target directory, not into system site-packages. Installation
    failures are non-fatal; callers still fall back to Yahoo endpoints with
    timestamp checks.
    """

    target_dir = _sandbox_package_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "--target",
                str(target_dir),
                "yfinance>=0.2.0",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=120,
        )
    except (subprocess.SubprocessError, OSError):
        return False
    _ensure_sandbox_package_path()
    return True


def _sandbox_package_dir() -> Path:
    configured = os.environ.get("VALUE_INVESTING_SKILL_PIP_TARGET")
    if configured:
        return Path(configured).expanduser()
    return Path(gettempdir()) / "value-investing-skill-python-packages"


def _ensure_sandbox_package_path() -> None:
    target = str(_sandbox_package_dir())
    if target not in sys.path:
        sys.path.insert(0, target)


def _coerce_utc_iso(value: Any) -> str:
    if value in (None, ""):
        return ""
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(int(value), tz=timezone.utc).isoformat()
    if hasattr(value, "to_pydatetime"):
        value = value.to_pydatetime()
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return ""
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat()


def _latest_intraday_yfinance_quote(ticker_obj: Any) -> tuple[float | None, str]:
    """Return latest 1-minute close and timestamp from yfinance history."""

    try:
        history = ticker_obj.history(period="1d", interval="1m", prepost=False)
    except Exception:
        return None, ""
    if getattr(history, "empty", True):
        return None, ""

    timestamp = _coerce_utc_iso(history.index[-1])
    close = history.iloc[-1].get("Close")
    try:
        price = float(close)
    except (TypeError, ValueError):
        price = None
    if price is not None and math.isnan(price):
        price = None
    return price, timestamp


def _quote_from_yfinance_package(
    ticker: str,
    installer: PackageInstaller | None = _install_yfinance_package,
) -> Dict[str, Any] | None:
    installed_after_attempt = False
    _ensure_sandbox_package_path()
    try:
        import yfinance as yf  # type: ignore
    except ImportError:
        if installer is None or not installer():
            return None
        installed_after_attempt = True
        try:
            import yfinance as yf  # type: ignore
        except ImportError:
            return None
    ticker_obj = yf.Ticker(ticker)
    info = ticker_obj.fast_info
    market_cap = getattr(info, "market_cap", None)
    shares = getattr(info, "shares", None)
    price = getattr(info, "last_price", None)
    previous_close = getattr(info, "previous_close", None)
    currency = getattr(info, "currency", "")
    history_price, market_time = _latest_intraday_yfinance_quote(ticker_obj)
    if price is None:
        price = history_price
    return {
        "price": price,
        "currency": currency or "",
        "market_cap": market_cap,
        "shares_outstanding": shares,
        "previous_close": previous_close,
        "regular_market_time": market_time,
        "source_name": "yfinance package / Yahoo Finance",
        "source_url": f"https://finance.yahoo.com/quote/{ticker}",
        "notes": "Fetched through optional yfinance package." + (" Installed yfinance in sandbox before fetching." if installed_after_attempt else ""),
    }


def _quote_from_yahoo_endpoint(ticker: str, fetcher: JsonFetcher = _fetch_json) -> Dict[str, Any]:
    url = f"{YAHOO_QUOTE_URL}?{urlencode({'symbols': ticker})}"
    try:
        payload = fetcher(url)
    except (HTTPError, URLError, OSError):
        return _quote_from_yahoo_chart(ticker, fetcher)
    results = payload.get("quoteResponse", {}).get("result", [])
    if not results:
        return _quote_from_yahoo_chart(ticker, fetcher)
    row = results[0]
    market_time = row.get("regularMarketTime")
    if market_time:
        market_time = datetime.fromtimestamp(int(market_time), tz=timezone.utc).isoformat()
    else:
        market_time = ""
    return {
        "price": row.get("regularMarketPrice"),
        "currency": row.get("currency", ""),
        "market_cap": row.get("marketCap"),
        "shares_outstanding": row.get("sharesOutstanding"),
        "previous_close": row.get("regularMarketPreviousClose"),
        "regular_market_time": market_time,
        "source_name": "Yahoo Finance quote endpoint",
        "source_url": url,
        "notes": "Fetched through Yahoo Finance public quote endpoint.",
    }


def _quote_from_yahoo_chart(ticker: str, fetcher: JsonFetcher = _fetch_json) -> Dict[str, Any]:
    url = f"{YAHOO_CHART_URL}/{ticker}?{urlencode({'range': '1d', 'interval': '1d'})}"
    payload = fetcher(url)
    results = payload.get("chart", {}).get("result", [])
    if not results:
        raise ValueError(f"No Yahoo Finance chart result for {ticker}")
    meta = results[0].get("meta", {})
    market_time = meta.get("regularMarketTime")
    if market_time:
        market_time = datetime.fromtimestamp(int(market_time), tz=timezone.utc).isoformat()
    else:
        market_time = ""
    return {
        "price": meta.get("regularMarketPrice"),
        "currency": meta.get("currency", ""),
        "market_cap": None,
        "shares_outstanding": None,
        "previous_close": meta.get("previousClose"),
        "regular_market_time": market_time,
        "source_name": "Yahoo Finance chart endpoint",
        "source_url": url,
        "notes": "Fetched through Yahoo Finance chart fallback; market cap and shares may be unavailable.",
    }


def get_market_quote(
    ticker: str,
    prefer_package: bool = True,
    fetcher: JsonFetcher = _fetch_json,
    analysis_as_of: str | None = None,
    package_installer: PackageInstaller | None = _install_yfinance_package,
) -> Dict[str, Any]:
    """Return a standardized market quote data packet."""

    normalized = ticker.strip().upper()
    analysis_time = analysis_as_of or _now_iso()
    raw = _quote_from_yfinance_package(normalized, installer=package_installer) if prefer_package else None
    yfinance_missing_timestamp = bool(raw is not None and not raw.get("regular_market_time"))
    if yfinance_missing_timestamp:
        raw = None
    if raw is None:
        raw = _quote_from_yahoo_endpoint(normalized, fetcher)
        raw["notes"] = raw.get("notes", "") + (
            " yfinance package unavailable, install failed, or lacked a market timestamp; did not use WebSearch price."
        )
    freshness = _price_freshness_fields(raw.get("regular_market_time", ""), analysis_time)
    quote = MarketQuote(
        ticker=normalized,
        price=raw.get("price"),
        currency=raw.get("currency", ""),
        market_cap=raw.get("market_cap"),
        shares_outstanding=raw.get("shares_outstanding"),
        previous_close=raw.get("previous_close"),
        regular_market_time=raw.get("regular_market_time", ""),
        analysis_as_of=analysis_time,
        price_date_status=freshness["price_date_status"],
        is_same_day=freshness["is_same_day"],
        staleness_minutes=freshness["staleness_minutes"],
        market_session_note=freshness["market_session_note"],
        source_name=raw.get("source_name", "Yahoo Finance"),
        source_url=raw.get("source_url", f"https://finance.yahoo.com/quote/{normalized}"),
        source_type="third_party_market_data",
        source_tier=3,
        confidence="medium",
        retrieval_timestamp=_now_iso(),
        notes=raw.get("notes", ""),
    )
    return asdict(quote)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m scripts.connectors.yfinance_connector <ticker>")
    print(json.dumps(get_market_quote(sys.argv[1]), indent=2))
