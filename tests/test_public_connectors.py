from scripts.connectors.ir_release_parser import parse_release_text
from scripts.connectors.openbb_provider_config import load_openbb_provider_config, openbb_runtime_status
from scripts.connectors.financial_history_builder import build_financial_history
from scripts.connectors.public_data_packet_builder import build_public_data_packet
from scripts.connectors.sec_edgar_connector import latest_us_gaap_fact, recent_filings, ticker_to_cik
from scripts.connectors import yfinance_connector
from scripts.connectors.yfinance_connector import get_market_quote
from scripts.routing.select_valuation_models import CompanyProfile
from urllib.error import HTTPError
from datetime import datetime, timezone
import sys


def test_sec_ticker_to_cik_with_mocked_fetcher():
    def fetcher(url):
        return {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}}

    assert ticker_to_cik("AAPL", fetcher=fetcher) == "0000320193"


def test_sec_recent_filings_builds_archive_url():
    submissions = {
        "cik": "320193",
        "filings": {
            "recent": {
                "accessionNumber": ["0000320193-26-000001"],
                "form": ["10-K"],
                "filingDate": ["2026-01-30"],
                "reportDate": ["2025-12-31"],
                "primaryDocument": ["aapl-20251231.htm"],
            }
        },
    }

    filing = recent_filings(submissions, forms=["10-K"], limit=1)[0]
    assert filing["form"] == "10-K"
    assert "Archives/edgar/data/320193/000032019326000001/aapl-20251231.htm" in filing["source_url"]


def test_sec_latest_us_gaap_fact_uses_latest_period():
    payload = {
        "facts": {
            "us-gaap": {
                "Revenues": {
                    "units": {
                        "USD": [
                            {"val": 100, "end": "2024-12-31", "filed": "2025-01-30", "form": "10-K"},
                            {"val": 120, "end": "2025-12-31", "filed": "2026-01-30", "form": "10-K"},
                        ]
                    }
                }
            }
        }
    }

    fact = latest_us_gaap_fact(payload, "Revenues", form_filter=["10-K"])
    assert fact["val"] == 120
    assert fact["source_type"] == "SEC EDGAR companyfacts"


def test_yfinance_connector_uses_yahoo_fallback_with_mocked_fetcher():
    market_time = 1_700_000_000

    def fetcher(url):
        return {
            "quoteResponse": {
                "result": [
                    {
                        "regularMarketPrice": 200.0,
                        "currency": "USD",
                        "marketCap": 5_000_000_000_000,
                        "sharesOutstanding": 25_000_000_000,
                        "regularMarketPreviousClose": 198.0,
                        "regularMarketTime": market_time,
                    }
                ]
            }
        }

    analysis_as_of = datetime.fromtimestamp(market_time, tz=timezone.utc).isoformat()
    quote = get_market_quote("NVDA", prefer_package=False, fetcher=fetcher, analysis_as_of=analysis_as_of)
    assert quote["price"] == 200.0
    assert quote["source_tier"] == 3
    assert quote["confidence"] == "medium"
    assert quote["price_date_status"] == "same_day"
    assert quote["is_same_day"] is True


def test_yfinance_connector_falls_back_to_chart_when_quote_is_blocked():
    market_time = 1_700_000_000

    def fetcher(url):
        if "/v7/finance/quote" in url:
            raise HTTPError(url, 401, "Unauthorized", hdrs=None, fp=None)
        return {
            "chart": {
                "result": [
                    {
                        "meta": {
                            "regularMarketPrice": 201.0,
                            "currency": "USD",
                            "previousClose": 199.0,
                            "regularMarketTime": market_time,
                        }
                    }
                ]
            }
        }

    analysis_as_of = datetime.fromtimestamp(market_time, tz=timezone.utc).isoformat()
    quote = get_market_quote("NVDA", prefer_package=False, fetcher=fetcher, analysis_as_of=analysis_as_of)
    assert quote["price"] == 201.0
    assert quote["market_cap"] is None
    assert "chart fallback" in quote["notes"]
    assert quote["is_same_day"] is True


def test_yfinance_connector_marks_non_same_day_price_stale():
    market_time = 1_700_000_000

    def fetcher(url):
        return {
            "quoteResponse": {
                "result": [
                    {
                        "regularMarketPrice": 200.0,
                        "currency": "USD",
                        "marketCap": 5_000_000_000_000,
                        "sharesOutstanding": 25_000_000_000,
                        "regularMarketPreviousClose": 198.0,
                        "regularMarketTime": market_time,
                    }
                ]
            }
        }

    quote = get_market_quote(
        "NVDA",
        prefer_package=False,
        fetcher=fetcher,
        analysis_as_of="2026-05-08T20:00:00+00:00",
    )
    assert quote["price_date_status"] == "not_same_day"
    assert quote["is_same_day"] is False


def test_yfinance_installer_uses_sandbox_target(tmp_path, monkeypatch):
    target = tmp_path / "packages"
    calls = {}

    def fake_run(cmd, **kwargs):
        calls["cmd"] = cmd
        calls["kwargs"] = kwargs

    monkeypatch.setenv("VALUE_INVESTING_SKILL_PIP_TARGET", str(target))
    monkeypatch.setattr(yfinance_connector.subprocess, "run", fake_run)
    if str(target) in sys.path:
        sys.path.remove(str(target))

    assert yfinance_connector._install_yfinance_package() is True
    assert "--target" in calls["cmd"]
    assert str(target) in calls["cmd"]
    assert "yfinance>=0.2.0" in calls["cmd"]
    assert calls["kwargs"]["check"] is True
    assert str(target) == sys.path[0]


def test_yfinance_connector_attempts_install_before_yahoo_fallback(monkeypatch):
    calls = {"install": 0}
    market_time = 1_700_000_000

    def fake_import_quote(ticker, installer=None):
        if installer is not None:
            calls["install"] += 1
            installer()
        return None

    def fake_installer():
        return False

    def fetcher(url):
        return {
            "quoteResponse": {
                "result": [
                    {
                        "regularMarketPrice": 200.0,
                        "currency": "USD",
                        "marketCap": 5_000_000_000_000,
                        "sharesOutstanding": 25_000_000_000,
                        "regularMarketPreviousClose": 198.0,
                        "regularMarketTime": market_time,
                    }
                ]
            }
        }

    monkeypatch.setattr(yfinance_connector, "_quote_from_yfinance_package", fake_import_quote)
    quote = get_market_quote(
        "NVDA",
        prefer_package=True,
        fetcher=fetcher,
        analysis_as_of=datetime.fromtimestamp(market_time, tz=timezone.utc).isoformat(),
        package_installer=fake_installer,
    )
    assert calls["install"] == 1
    assert quote["price"] == 200.0
    assert "did not use WebSearch price" in quote["notes"]


def test_yfinance_connector_uses_package_when_install_succeeds(monkeypatch):
    market_time = 1_700_000_000
    market_time_iso = datetime.fromtimestamp(market_time, tz=timezone.utc).isoformat()

    def fake_import_quote(ticker, installer=None):
        assert installer is not None
        assert installer() is True
        return {
            "price": 210.0,
            "currency": "USD",
            "market_cap": 5_200_000_000_000,
            "shares_outstanding": 25_000_000_000,
            "previous_close": 208.0,
            "regular_market_time": market_time_iso,
            "source_name": "yfinance package / Yahoo Finance",
            "source_url": f"https://finance.yahoo.com/quote/{ticker}",
            "notes": "Fetched through optional yfinance package. Installed yfinance in sandbox before fetching.",
        }

    monkeypatch.setattr(yfinance_connector, "_quote_from_yfinance_package", fake_import_quote)
    quote = get_market_quote(
        "NVDA",
        prefer_package=True,
        fetcher=lambda url: (_ for _ in ()).throw(AssertionError("Yahoo fallback should not be used")),
        analysis_as_of=market_time_iso,
        package_installer=lambda: True,
    )
    assert quote["price"] == 210.0
    assert quote["market_cap"] == 5_200_000_000_000
    assert "Installed yfinance in sandbox" in quote["notes"]


def test_yfinance_connector_rejects_package_quote_without_timestamp(monkeypatch):
    market_time = 1_700_000_000

    def fake_import_quote(ticker, installer=None):
        return {
            "price": 210.0,
            "currency": "USD",
            "market_cap": 5_200_000_000_000,
            "shares_outstanding": 25_000_000_000,
            "previous_close": 208.0,
            "regular_market_time": "",
            "source_name": "yfinance package / Yahoo Finance",
            "source_url": f"https://finance.yahoo.com/quote/{ticker}",
            "notes": "Fetched through optional yfinance package.",
        }

    def fetcher(url):
        return {
            "quoteResponse": {
                "result": [
                    {
                        "regularMarketPrice": 200.0,
                        "currency": "USD",
                        "marketCap": 5_000_000_000_000,
                        "sharesOutstanding": 25_000_000_000,
                        "regularMarketPreviousClose": 198.0,
                        "regularMarketTime": market_time,
                    }
                ]
            }
        }

    monkeypatch.setattr(yfinance_connector, "_quote_from_yfinance_package", fake_import_quote)
    quote = get_market_quote(
        "NVDA",
        prefer_package=True,
        fetcher=fetcher,
        analysis_as_of=datetime.fromtimestamp(market_time, tz=timezone.utc).isoformat(),
    )
    assert quote["price"] == 200.0
    assert quote["source_name"] == "Yahoo Finance quote endpoint"
    assert "lacked a market timestamp" in quote["notes"]
    assert "did not use WebSearch price" in quote["notes"]


def test_ir_release_parser_extracts_metrics_and_guidance():
    html = """
    <html><head><title>Example</title></head><body>
    <h1>Example Announces Results</h1>
    Revenue was $12.5 billion in the quarter. Free cash flow was $3.2 billion.
    Gross margin was 72.5%. The company expects revenue of $14 billion next quarter.
    Supply constraints remain a risk.
    </body></html>
    """

    parsed = parse_release_text(html, source="inline")
    assert "revenue" in parsed["metrics"]
    assert "free_cash_flow" in parsed["metrics"]
    assert parsed["guidance_sentences"]
    assert parsed["risk_sentences"]


def test_openbb_provider_config_detects_env_key(tmp_path, monkeypatch):
    config = tmp_path / "openbb.local.json"
    config.write_text(
        """
        {
          "enabled": true,
          "providers": {
            "fmp": {
              "enabled": true,
              "api_key_env": "FMP_API_KEY",
              "api_key": "",
              "use_for": ["financial_statements"]
            }
          }
        }
        """,
        encoding="utf-8",
    )
    monkeypatch.setenv("FMP_API_KEY", "test-key")

    loaded = load_openbb_provider_config(config)
    assert loaded["usable_providers"][0]["name"] == "fmp"
    assert loaded["usable_providers"][0]["api_key_source"] == "environment"


def test_openbb_runtime_status_is_safe_without_package(tmp_path):
    config = tmp_path / "openbb.local.json"
    config.write_text('{"enabled": true, "providers": {}}', encoding="utf-8")

    status = openbb_runtime_status(config)
    assert "openbb_installed" in status
    assert status["usable"] in {True, False}


def test_public_data_packet_builder_orchestrates_mocked_sources():
    def sec_fetcher(url):
        if "company_tickers" in url:
            return {"0": {"cik_str": 1045810, "ticker": "NVDA", "title": "NVIDIA Corp"}}
        if "submissions" in url:
            return {
                "cik": "1045810",
                "name": "NVIDIA Corp",
                "filings": {
                    "recent": {
                        "accessionNumber": ["0001045810-26-000021"],
                        "form": ["10-K"],
                        "filingDate": ["2026-02-25"],
                        "reportDate": ["2026-01-25"],
                        "primaryDocument": ["nvda-20260125.htm"],
                    }
                },
            }
        if "companyfacts" in url:
            return {
                "cik": 1045810,
                "facts": {
                    "us-gaap": {
                        "Revenues": {
                            "units": {
                                "USD": [
                                    {"val": 130497000000, "end": "2026-01-25", "filed": "2026-02-25", "form": "10-K"}
                                ]
                            }
                        }
                    }
                },
            }
        raise AssertionError(f"unexpected SEC URL: {url}")

    def market_fetcher(url):
        market_time = 1_774_445_400
        return {
            "quoteResponse": {
                "result": [
                    {
                        "regularMarketPrice": 198.45,
                        "currency": "USD",
                        "marketCap": 4_900_000_000_000,
                        "sharesOutstanding": 24_700_000_000,
                        "regularMarketPreviousClose": 197.0,
                        "regularMarketTime": market_time,
                    }
                ]
            }
        }

    packet = build_public_data_packet(
        "nvda",
        sec_fetcher=sec_fetcher,
        market_fetcher=market_fetcher,
        prefer_yfinance_package=False,
    )

    assert packet["ticker"] == "NVDA"
    assert packet["market_quote"]["price"] == 198.45
    assert packet["sec"]["filing_snapshot"]["latest_filings"][0]["form"] == "10-K"
    assert packet["sec"]["facts"]["Revenues"]["val"] == 130497000000
    assert packet["financial_history"]["coverage"]["status"] == "blocked"
    assert any(gate["gate"] == "Financial History Gate" for gate in packet["execution_gate_checklist"])
    assert packet["errors"] == []


def _history_payload():
    def annual(value, year, tag_form="10-K"):
        return {
            "val": value,
            "start": f"{year}-01-01",
            "end": f"{year}-12-31",
            "filed": f"{year + 1}-02-15",
            "form": tag_form,
            "frame": f"CY{year}",
            "fy": year,
            "fp": "FY",
        }

    def quarter(value, year, quarter_number):
        month_end = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}[quarter_number]
        month_start = {1: "01-01", 2: "04-01", 3: "07-01", 4: "10-01"}[quarter_number]
        filed_month = min(quarter_number * 3 + 1, 12)
        form = "10-K" if quarter_number == 4 else "10-Q"
        return {
            "val": value,
            "start": f"{year}-{month_start}",
            "end": f"{year}-{month_end}",
            "filed": f"{year}-{str(filed_month).zfill(2)}-15",
            "form": form,
            "frame": f"CY{year}Q{quarter_number}",
            "fy": year,
            "fp": f"Q{quarter_number}",
        }

    def instant(value, year, quarter_number=None):
        if quarter_number is None:
            return {
                "val": value,
                "end": f"{year}-12-31",
                "filed": f"{year + 1}-02-15",
                "form": "10-K",
                "fy": year,
                "fp": "FY",
            }
        month_end = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}[quarter_number]
        filed_month = min(quarter_number * 3 + 1, 12)
        return {
            "val": value,
            "end": f"{year}-{month_end}",
            "filed": f"{year}-{str(filed_month).zfill(2)}-15",
            "form": "10-Q",
            "fy": year,
            "fp": f"Q{quarter_number}",
        }

    return {
        "cik": 1045810,
        "facts": {
            "us-gaap": {
                "Revenues": {"units": {"USD": [annual(100 + y, y) for y in range(2020, 2026)] + [quarter(20 + q, 2025, q) for q in range(1, 5)] + [quarter(30 + q, 2026, q) for q in range(1, 5)]}},
                "NetIncomeLoss": {"units": {"USD": [annual(10 + y, y) for y in range(2020, 2026)] + [quarter(2 + q, 2025, q) for q in range(1, 5)] + [quarter(3 + q, 2026, q) for q in range(1, 5)]}},
                "NetCashProvidedByUsedInOperatingActivities": {"units": {"USD": [annual(20 + y, y) for y in range(2020, 2026)] + [quarter(5 + q, 2025, q) for q in range(1, 5)] + [quarter(6 + q, 2026, q) for q in range(1, 5)]}},
                "PaymentsToAcquirePropertyPlantAndEquipment": {"units": {"USD": [annual(5 + y, y) for y in range(2020, 2026)] + [quarter(1 + q, 2025, q) for q in range(1, 5)] + [quarter(2 + q, 2026, q) for q in range(1, 5)]}},
                "GrossProfit": {"units": {"USD": [annual(60 + y, y) for y in range(2020, 2026)] + [quarter(12 + q, 2025, q) for q in range(1, 5)] + [quarter(16 + q, 2026, q) for q in range(1, 5)]}},
                "InventoryNet": {"units": {"USD": [instant(8 + y, y) for y in range(2020, 2026)] + [instant(10 + q, 2026, q) for q in range(1, 5)]}},
                "PropertyPlantAndEquipmentNet": {"units": {"USD": [instant(30 + y, y) for y in range(2020, 2026)] + [instant(40 + q, 2026, q) for q in range(1, 5)]}},
                "ContractWithCustomerLiabilityCurrent": {"units": {"USD": [instant(4 + y, y) for y in range(2020, 2026)] + [instant(6 + q, 2026, q) for q in range(1, 5)]}},
            }
        },
    }


def test_financial_history_builder_extracts_annual_quarterly_and_derived_metrics():
    history = build_financial_history("NVDA", facts_payload=_history_payload(), annual_years=5, quarter_count=8)

    assert history["coverage"]["status"] == "passed"
    assert history["latest_financial_period"] == "FY2026-Q4"
    assert len(history["metrics"]["revenue"]["annual"]) == 5
    assert len(history["metrics"]["revenue"]["quarterly"]) == 8
    assert history["metrics"]["free_cash_flow"]["annual"]
    assert history["metrics"]["gross_margin"]["quarterly"]


def test_public_data_packet_includes_tech_cycle_gates_when_profile_is_supplied():
    def sec_fetcher(url):
        if "company_tickers" in url:
            return {"0": {"cik_str": 1045810, "ticker": "NVDA", "title": "NVIDIA Corp"}}
        if "submissions" in url:
            return {
                "cik": "1045810",
                "name": "NVIDIA Corp",
                "filings": {"recent": {"accessionNumber": [], "form": [], "filingDate": [], "reportDate": [], "primaryDocument": []}},
            }
        if "companyfacts" in url:
            return _history_payload()
        raise AssertionError(f"unexpected SEC URL: {url}")

    def market_fetcher(url):
        market_time = 1_774_445_400
        return {
            "quoteResponse": {
                "result": [
                    {
                        "regularMarketPrice": 198.45,
                        "currency": "USD",
                        "marketCap": 4_900_000_000_000,
                        "sharesOutstanding": 24_700_000_000,
                        "regularMarketPreviousClose": 197.0,
                        "regularMarketTime": market_time,
                    }
                ]
            }
        }

    packet = build_public_data_packet(
        "NVDA",
        sec_fetcher=sec_fetcher,
        market_fetcher=market_fetcher,
        prefer_yfinance_package=False,
        company_profile=CompanyProfile(industry="ai semiconductor", is_ai_semiconductor_platform=True),
    )

    gate_names = {gate["gate"]: gate["status"] for gate in packet["execution_gate_checklist"]}
    assert packet["tech_cycle_applicability"]["cycle_profile"] == "physical_inventory"
    assert gate_names["Financial History Gate"] == "Passed"
    assert gate_names["Inventory Cycle Gate"] == "Passed"
    assert gate_names["Capacity Cycle Gate"] == "Passed"
