import unittest

from scripts.valuation.valuation_common import ValuationResult, StructuredAssumption
from scripts.valuation.valuation_comps import ComparableCompany, peer_multiple, equity_value_from_multiple
from scripts.valuation.valuation_cyclical import commodity_scenario_ebitda, mid_cycle_metric
from scripts.valuation.valuation_ddm import gordon_growth_value, two_stage_ddm
from scripts.valuation.valuation_executor import run_valuation, run_valuation_payload
from scripts.valuation.valuation_fintech import normalized_earnings_value
from scripts.valuation.valuation_input_packet import ValuationInputPacket
from scripts.valuation.valuation_insurance import combined_ratio, float_cost
from scripts.valuation.valuation_liquidation import AssetRecovery, LiabilityClaim, liquidation_equity_value
from scripts.valuation.valuation_reit import noi_capitalized_value, distribution_coverage
from scripts.valuation.valuation_rnpv import PipelineAsset, build_peak_sales_cash_flows, portfolio_rnpv
from scripts.valuation.valuation_scenario import Scenario, probability_weighted_value
from scripts.valuation.valuation_sotp import SegmentInput, sotp_equity_value
from scripts.context.context_router import route_context
from scripts.audit.structured_assumption_audit import audit_model_assumptions
from scripts.routing.select_valuation_models import CompanyProfile, select_valuation_models


class ValuationModelTests(unittest.TestCase):
    def test_ddm_gordon_growth(self):
        self.assertAlmostEqual(gordon_growth_value(3.0, 0.08, 0.02), 50.0)

    def test_two_stage_ddm_is_above_no_growth_for_positive_growth(self):
        no_growth = two_stage_ddm(2.0, 0.0, 0.02, 0.08, years=5)
        growth = two_stage_ddm(2.0, 0.05, 0.02, 0.08, years=5)
        self.assertGreater(growth, no_growth)

    def test_sotp_equity_value(self):
        segments = [
            SegmentInput("core", metric=100.0, multiple=8.0),
            SegmentInput("growth", explicit_value=300.0, ownership=0.8),
        ]
        value = sotp_equity_value(segments, net_debt=100.0, corporate_cost_value=40.0)
        self.assertAlmostEqual(value, 900.0)

    def test_comps_trimmed_peer_multiple(self):
        peers = [
            ComparableCompany("a", 10.0),
            ComparableCompany("b", 12.0),
            ComparableCompany("c", 14.0),
        ]
        self.assertAlmostEqual(peer_multiple(peers, trim_fraction=0.0), 12.0)
        self.assertAlmostEqual(equity_value_from_multiple(100.0, 12.0, net_debt=200.0), 1000.0)

    def test_liquidation_value(self):
        assets = [
            AssetRecovery("cash", 100.0, 1.0),
            AssetRecovery("inventory", 100.0, 0.5),
        ]
        liabilities = [LiabilityClaim("debt", 80.0)]
        self.assertAlmostEqual(liquidation_equity_value(assets, liabilities, liquidation_costs=10.0), 60.0)

    def test_rnpv_portfolio_value(self):
        asset = PipelineAsset(
            "drug-a",
            cash_flows=[100.0, 100.0],
            success_probability=0.5,
            development_costs=[20.0],
        )
        value = portfolio_rnpv([asset], discount_rate=0.1, net_cash=10.0)
        self.assertGreater(value, 70.0)
        self.assertEqual(len(build_peak_sales_cash_flows(1000.0, 0.2, 2, 1, decline_years=1)), 4)

    def test_reit_helpers(self):
        self.assertAlmostEqual(noi_capitalized_value(50.0, 0.05), 1000.0)
        self.assertAlmostEqual(distribution_coverage(120.0, 100.0), 1.2)

    def test_cyclical_helpers(self):
        self.assertAlmostEqual(mid_cycle_metric([80.0, 100.0, 120.0]), 100.0)
        self.assertAlmostEqual(commodity_scenario_ebitda(10.0, 50.0, 30.0, fixed_costs=50.0), 150.0)

    def test_insurance_helpers(self):
        self.assertAlmostEqual(combined_ratio(60.0, 30.0, 100.0), 0.9)
        self.assertAlmostEqual(float_cost(5.0, 100.0), -0.05)

    def test_scenario_probabilities(self):
        scenarios = [Scenario("bear", 80.0, 0.25), Scenario("base", 100.0, 0.5), Scenario("bull", 140.0, 0.25)]
        self.assertAlmostEqual(probability_weighted_value(scenarios), 105.0)

    def test_common_payload_shape(self):
        result = ValuationResult(
            model_name="Test Model",
            base_value=100.0,
            key_assumptions=["Base case"],
            structured_assumptions=[
                StructuredAssumption(
                    assumption="growth",
                    value=0.03,
                    unit="percent",
                    evidence=["history"],
                    confidence="medium",
                    sensitivity="high",
                )
            ],
        )
        payload = result.to_payload()
        self.assertEqual(payload["selected_models"], ["Test Model"])
        self.assertEqual(payload["structured_assumptions"][0]["assumption"], "growth")

    def test_context_router_points_to_real_rnpv_script(self):
        files = route_context("full_research", "biotech")
        self.assertIn("scripts/valuation/valuation_rnpv.py", files)
        self.assertNotIn("scripts/valuation/valuation_biotech_rnpv.py", files)

    def test_valuation_router_exposes_algorithm_files(self):
        models = select_valuation_models(
            CompanyProfile(
                industry="consumer staples",
                is_high_quality_compounder=True,
                shareholder_return_scores={"stable": 2, "covered": 2, "buyback": 2},
            )
        )
        self.assertIn("scripts/valuation/valuation_common.py", models["valuation_algorithm_files"])
        self.assertIn("scripts/valuation/valuation_ddm.py", models["valuation_algorithm_files"])

    def test_fintech_brokerage_route_for_hood_like_company(self):
        models = select_valuation_models(
            CompanyProfile(industry="consumer brokerage fintech trading app", is_brokerage_platform=True)
        )
        self.assertEqual(models["base_type"], "Fintech / Brokerage Platform")
        self.assertEqual(models["primary_workflow"], "workflows/10_fintech_brokerage.md")
        self.assertIn("scripts/valuation/valuation_fintech.py", models["valuation_algorithm_files"])

    def test_fintech_normalized_earnings_value(self):
        self.assertAlmostEqual(
            normalized_earnings_value(
                revenue=1000.0,
                normalized_margin=0.25,
                earnings_multiple=20.0,
                net_debt=-100.0,
            ),
            5100.0,
        )

    def test_structured_assumption_gate_blocks_missing_required(self):
        result = audit_model_assumptions("ddm", [])
        self.assertEqual(result.status, "Blocked")
        self.assertIn("current_dividend_per_share", result.required_missing)

    def test_unified_executor_runs_owner_earnings_dcf(self):
        assumptions = [
            {
                "assumption": name,
                "value": 1,
                "unit": "mixed",
                "scenario": "base",
                "evidence": ["test evidence", "policy constraint"],
                "confidence": "medium",
                "sensitivity": "medium",
                "source_or_reason": "unit test",
            }
            for name in [
                "base_owner_earnings_or_fcf",
                "forecast_growth",
                "discount_rate",
                "terminal_growth",
                "net_debt",
                "shares_outstanding",
            ]
        ]
        packet = ValuationInputPacket(
            company="Sample",
            ticker="SMP",
            analysis_as_of="2026-05-03",
            model_inputs={
                "owner_earnings_dcf": {
                    "owner_earnings_forecast": [100.0, 105.0, 110.0],
                    "discount_rate": 0.08,
                    "terminal_growth": 0.02,
                    "net_debt": 0.0,
                    "shares_outstanding": 10.0,
                }
            },
            structured_assumptions=assumptions,
            data_points=[
                {
                    "data_id": "fcf_1",
                    "metric": "FCF",
                    "value": 100.0,
                    "unit": "USD",
                    "period": "FY2025",
                    "source_name": "Annual report",
                    "source_type": "filing",
                    "source_url": "https://example.com/report",
                    "source_path": None,
                    "source_date": "2026-04-01",
                    "source_tier": 1,
                    "confidence": 0.9,
                    "raw_or_derived": "raw",
                }
            ],
        )
        execution = run_valuation(CompanyProfile(industry="consumer", is_high_quality_compounder=True), packet)
        self.assertTrue(any(result.model_name == "Owner Earnings DCF" and not result.blocked for result in execution.results))
        self.assertNotEqual(execution.valuation_summary()["base_value"], "Blocked")

    def test_unified_executor_blocks_unauditable_data(self):
        packet = ValuationInputPacket(
            company="Sample",
            ticker="SMP",
            analysis_as_of="2026-05-03",
            model_inputs={"scenario": {"scenarios": [{"name": "base", "value": 100.0, "probability": 1.0}]}},
            structured_assumptions=[
                {
                    "assumption": "scenario_values",
                    "value": 100.0,
                    "scenario": "base",
                    "evidence": ["test"],
                    "confidence": "medium",
                    "sensitivity": "medium",
                },
                {
                    "assumption": "scenario_probabilities",
                    "value": 1.0,
                    "scenario": "base",
                    "evidence": ["test"],
                    "confidence": "medium",
                    "sensitivity": "medium",
                },
                {
                    "assumption": "scenario_rationale",
                    "value": "test case",
                    "scenario": "base",
                    "evidence": ["test"],
                    "confidence": "medium",
                    "sensitivity": "medium",
                },
            ],
            data_points=[
                {
                    "data_id": "revenue_1",
                    "metric": "Revenue",
                    "value": 100.0,
                    "unit": "USD",
                    "period": "FY2025",
                    "source_name": "No link",
                    "source_type": "filing",
                    "source_url": None,
                    "source_path": None,
                    "source_date": "2026-04-01",
                    "source_tier": 1,
                    "confidence": 0.9,
                    "raw_or_derived": "raw",
                }
            ],
        )
        payload = run_valuation_payload(CompanyProfile(industry="platform", is_digital_platform=True), packet)
        self.assertEqual(payload["valuation_summary"]["valuation_status"], "blocked")
        self.assertTrue(payload["blocked_models"])


if __name__ == "__main__":
    unittest.main()
