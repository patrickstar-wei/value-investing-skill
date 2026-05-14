from datetime import datetime, timezone

import pytest

from scripts.audit.execution_gate_audit import audit_gates, market_adapter_gate, pe_validation_gate
from scripts.connectors.public_data_packet_builder import build_public_data_packet
from scripts.markets.cn_a.restatement_detector import detect_restatements_from_announcements, restatement_status_for_ttm
from scripts.markets.registry import MARKET_CN_A, MARKET_HK, MARKET_US, detect_market
from scripts.validation.pe_validator import BLOCKED, WARNING, validate_pe_calculation


def test_detect_market_routes_us_cn_a_and_hk_tickers():
    assert detect_market("AAPL") == MARKET_US
    assert detect_market("000858.SZ") == MARKET_CN_A
    assert detect_market("600519.SH") == MARKET_CN_A
    assert detect_market("0700.HK") == MARKET_HK


def test_cn_a_packet_uses_a_share_adapter_and_blocks_missing_financials():
    market_time = int(datetime(2026, 5, 14, 7, 0, tzinfo=timezone.utc).timestamp())

    def market_fetcher(url):
        return {
            "quoteResponse": {
                "result": [
                    {
                        "regularMarketPrice": 88.99,
                        "currency": "CNY",
                        "marketCap": 345_424_296_364.95,
                        "sharesOutstanding": 3_881_608_005,
                        "regularMarketPreviousClose": 89.07,
                        "regularMarketTime": market_time,
                    }
                ]
            }
        }

    def sec_fetcher(url):
        raise AssertionError("CN_A ticker must not call SEC companyfacts")

    packet = build_public_data_packet(
        "000858.SZ",
        sec_fetcher=sec_fetcher,
        market_fetcher=market_fetcher,
        prefer_yfinance_package=False,
    )

    assert packet["market"] == MARKET_CN_A
    assert packet["sec"]["facts"] == {}
    assert packet["financial_history"]["coverage"]["status"] == "blocked"
    assert "cn_a.financials" in packet["missing_data"]
    gate_statuses = {gate["gate"]: gate["status"] for gate in packet["execution_gate_checklist"]}
    assert gate_statuses["Market Adapter Gate"] == "Passed"
    assert gate_statuses["Financial History Gate"] == "Blocked"


def test_wuliangye_pe_ttm_golden_case_uses_adjusted_q1():
    result = validate_pe_calculation(
        ticker="000858.SZ",
        market_quote={
            "market_cap": 3454e8,
            "currency": "CNY",
            "regular_market_time": "2026-05-14T07:00:00+00:00",
        },
        financials={
            "currency": "CNY",
            "annual": {
                "period": "2025FY",
                "net_income": 89.54e8,
                "source_id": "wly-2025-annual-report",
            },
            "current_quarter": {
                "period": "2026Q1",
                "net_income": 80.6276494078e8,
                "source_id": "wly-2026-q1-report",
            },
            "prior_year_same_quarter": {
                "period": "2025Q1 adjusted",
                "net_income": 44.1631304841e8,
                "source_id": "wly-2026-restatement",
            },
            "restatement_status": "adjusted",
        },
        external_pe={"eastmoney": 27.41},
    )

    assert result.validation_status == WARNING
    assert result.confidence == "MEDIUM"
    assert result.calculated_pe_ttm == 27.41
    assert result.ttm_earnings_breakdown.total == pytest.approx(126.0045189237e8)
    assert any(a.anomaly_type == "RESTATEMENT_ADJUSTED" for a in result.anomalies)


def test_pe_validator_blocks_restatement_affected_unadjusted_earnings():
    result = validate_pe_calculation(
        ticker="000858.SZ",
        market_quote={"market_cap": 3454e8, "currency": "CNY"},
        financials={
            "currency": "CNY",
            "ttm_net_income": 235e8,
            "restatement_status": "affected_not_adjusted",
        },
    )

    assert result.validation_status == BLOCKED
    assert any(a.anomaly_type == "UNADJUSTED_RESTATEMENT" for a in result.anomalies)


def test_cn_a_restatement_detector_marks_ttm_adjusted_when_affected_period_has_adjusted_figures():
    events = detect_restatements_from_announcements(
        [
            {
                "announcement_date": "2026-04-30",
                "title": "关于前期会计差错更正的公告",
                "periods_affected": ["2025Q1", "2025Q2", "2025Q3"],
                "adjusted_figures_available": True,
            }
        ]
    )

    assert len(events) == 1
    assert restatement_status_for_ttm(events, ["2025Q1", "2025FY", "2026Q1"]) == "adjusted"


def test_market_and_pe_gates_convert_validation_to_execution_results():
    packet = {"market": MARKET_CN_A}
    market_gate = market_adapter_gate("000858.SZ", packet)
    pe_gate = pe_validation_gate(
        "000858.SZ",
        market_quote={"market_cap": 3454e8, "currency": "CNY"},
        financials={
            "currency": "CNY",
            "annual": {"period": "2025FY", "net_income": 89.54e8},
            "current_quarter": {"period": "2026Q1", "net_income": 80.6276494078e8},
            "prior_year_same_quarter": {"period": "2025Q1 adjusted", "net_income": 44.1631304841e8},
            "restatement_status": "adjusted",
        },
        external_pe={"eastmoney": 27.41},
    )

    audited = audit_gates([market_gate, pe_gate])
    assert audited[0].status == "Passed"
    assert audited[1].status == "Passed"
