"""Unified valuation execution pipeline.

This module connects routing, structured assumptions, data provenance,
freshness checks, deterministic valuation algorithms, and report-ready output.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

from scripts.audit.data_provenance_audit import can_use_for_valuation
from scripts.audit.structured_assumption_audit import audit_model_assumptions
from scripts.data.check_data_freshness import check_freshness
from scripts.routing.select_valuation_models import CompanyProfile, select_valuation_models
from scripts.valuation.valuation_common import ValuationResult
from scripts.valuation.valuation_comps import ComparableCompany, equity_value_from_multiple, peer_multiple
from scripts.valuation.valuation_cyclical import cyclical_equity_value, mid_cycle_metric
from scripts.valuation.valuation_ddm import two_stage_ddm
from scripts.valuation.valuation_epv import epv_result
from scripts.valuation.valuation_fintech import normalized_earnings_value
from scripts.valuation.valuation_input_packet import ValuationInputPacket, unwrap_input
from scripts.valuation.valuation_insurance import insurance_equity_value
from scripts.valuation.valuation_liquidation import AssetRecovery, LiabilityClaim, liquidation_equity_value
from scripts.valuation.valuation_nav import nav_result
from scripts.valuation.valuation_owner_earnings_dcf import owner_earnings_dcf_result
from scripts.valuation.valuation_reit import reit_equity_value_from_noi
from scripts.valuation.valuation_residual_income import residual_income_result
from scripts.valuation.valuation_reverse_dcf import reverse_dcf_result
from scripts.valuation.valuation_rnpv import PipelineAsset, portfolio_rnpv
from scripts.valuation.valuation_scenario import Scenario, probability_weighted_value
from scripts.valuation.valuation_sotp import SegmentInput, sotp_equity_value


DATA_CATEGORY_BY_METRIC = {
    "Current Price": "market_price",
    "Market Cap": "market_price",
    "Shares Outstanding": "market_price",
    "Revenue": "annual_financials",
    "EBIT": "annual_financials",
    "EBITDA": "annual_financials",
    "FCF": "annual_financials",
    "Cash": "annual_financials",
    "Debt": "annual_financials",
    "Segment Revenue": "segment_data",
    "Peer Multiple": "peer_group_data",
}


@dataclass
class ValuationExecution:
    routing: Dict[str, Any]
    results: List[ValuationResult] = field(default_factory=list)
    gates: List[Dict[str, str]] = field(default_factory=list)
    blocked_models: List[Dict[str, str]] = field(default_factory=list)

    def valuation_summary(self) -> Dict[str, Any]:
        usable = [result for result in self.results if not result.blocked]
        if not usable:
            reasons = [item["reason"] for item in self.blocked_models] or ["No usable model result"]
            return {
                "selected_models": self.routing.get("valuation_algorithm_files", []),
                "bear_value": "Blocked",
                "base_value": "Blocked",
                "bull_value": "Blocked",
                "current_price": "Blocked",
                "margin_of_safety": "Blocked",
                "valuation_status": "blocked",
                "key_assumptions": [],
                "structured_assumptions": [],
                "assumption_confidence": "blocked",
                "conclusion_change_triggers": [
                    {
                        "assumption": "Missing valuation inputs",
                        "change": "Required data becomes available",
                        "impact": "Would unblock valuation range and price/action zones",
                    }
                ],
                "sensitivity_summary": "Blocked: " + "; ".join(reasons),
                "blocked_or_low_confidence_items": reasons,
            }

        base_values = [result.base_value for result in usable if result.base_value is not None]
        per_share_values = [result.per_share_base for result in usable if result.per_share_base is not None]
        primary = usable[0]
        summary = primary.to_payload()
        summary["selected_models"] = [result.model_name for result in usable]
        if base_values:
            summary["bear_value"] = min(base_values)
            summary["base_value"] = base_values[0]
            summary["bull_value"] = max(base_values)
        if per_share_values:
            summary["per_share_bear"] = min(per_share_values)
            summary["per_share_base"] = per_share_values[0]
            summary["per_share_bull"] = max(per_share_values)
        summary["blocked_or_low_confidence_items"] = [item["reason"] for item in self.blocked_models]
        return summary


def _unwrap_inputs(data: Dict[str, Any]) -> Dict[str, Any]:
    return {key: unwrap_input(value) for key, value in data.items()}


def _blocked(model_key: str, reason: str) -> ValuationResult:
    return ValuationResult(model_name=model_key, blocked=True, blocked_reason=reason)


def _audit_packet(packet: ValuationInputPacket) -> List[Dict[str, str]]:
    gates: List[Dict[str, str]] = []

    provenance_ok, provenance_blockers = can_use_for_valuation(packet.data_points)
    gates.append(
        {
            "gate": "Data Provenance",
            "status": "Passed" if provenance_ok else "Blocked",
            "comment": "All data points auditable." if provenance_ok else str(provenance_blockers),
        }
    )

    freshness_results = []
    for dp in packet.data_points:
        metric = dp.get("metric", "")
        category = DATA_CATEGORY_BY_METRIC.get(metric, "annual_financials")
        freshness_results.append(
            check_freshness(
                metric=metric,
                data_category=category,
                source_date=dp.get("source_date"),
                as_of_date=packet.analysis_as_of,
            )
        )
    stale = [item for item in freshness_results if item.status in {"Missing", "Stale"}]
    gates.append(
        {
            "gate": "Data Freshness",
            "status": "Passed" if not stale else "Blocked",
            "comment": "Freshness inputs usable." if not stale else "; ".join(f"{item.metric}: {item.status}" for item in stale),
        }
    )

    missing_bindings = packet.missing_required_bindings()
    gates.append(
        {
            "gate": "Input Binding",
            "status": "Passed" if not missing_bindings else "Blocked",
            "comment": "All required inputs bound to data or assumptions." if not missing_bindings else ", ".join(missing_bindings),
        }
    )
    return gates


def _run_owner_earnings_dcf(inputs: Dict[str, Any]) -> ValuationResult:
    return owner_earnings_dcf_result(
        owner_earnings_forecast=inputs["owner_earnings_forecast"],
        discount_rate=inputs["discount_rate"],
        terminal_growth=inputs["terminal_growth"],
        net_debt=inputs.get("net_debt", 0.0),
        shares_outstanding=inputs.get("shares_outstanding"),
    )


def _run_reverse_dcf(inputs: Dict[str, Any]) -> ValuationResult:
    return reverse_dcf_result(
        market_cap=inputs["market_cap"],
        net_debt=inputs.get("net_debt", 0.0),
        base_fcf=inputs["base_fcf"],
        years=inputs.get("years", 10),
        discount_rate=inputs["discount_rate"],
        terminal_growth=inputs["terminal_growth"],
    )


def _run_epv(inputs: Dict[str, Any]) -> ValuationResult:
    return epv_result(
        normalized_ebit=inputs["normalized_ebit"],
        tax_rate=inputs["tax_rate"],
        wacc=inputs["wacc"],
        net_debt=inputs.get("net_debt", 0.0),
        shares_outstanding=inputs.get("shares_outstanding"),
    )


def _run_nav(inputs: Dict[str, Any]) -> ValuationResult:
    return nav_result(
        asset_fair_values=inputs["asset_fair_values"],
        liability_fair_values=inputs["liability_fair_values"],
        shares_outstanding=inputs.get("shares_outstanding"),
    )


def _run_residual_income(inputs: Dict[str, Any]) -> ValuationResult:
    return residual_income_result(
        current_book_value=inputs["current_book_value"],
        residual_income_forecast=inputs["residual_income_forecast"],
        cost_of_equity=inputs["cost_of_equity"],
        shares_outstanding=inputs.get("shares_outstanding"),
    )


def _run_ddm(inputs: Dict[str, Any]) -> ValuationResult:
    per_share_value = two_stage_ddm(
        current_dividend_per_share=inputs["current_dividend_per_share"],
        first_stage_growth=inputs["first_stage_growth"],
        terminal_growth=inputs["terminal_growth"],
        cost_of_equity=inputs["cost_of_equity"],
        years=inputs.get("years", 5),
    )
    return ValuationResult(model_name="DDM", per_share_base=per_share_value, base_value=per_share_value)


def _run_sotp(inputs: Dict[str, Any]) -> ValuationResult:
    segments = [SegmentInput(**segment) for segment in inputs["segments"]]
    equity_value = sotp_equity_value(
        segments=segments,
        net_debt=inputs.get("net_debt", 0.0),
        minority_interest=inputs.get("minority_interest", 0.0),
        non_operating_assets=inputs.get("non_operating_assets", 0.0),
        corporate_cost_value=inputs.get("corporate_cost_value", 0.0),
        holding_company_discount=inputs.get("holding_company_discount", 0.0),
    )
    result = ValuationResult(model_name="SOTP", base_value=equity_value)
    shares = inputs.get("shares_outstanding")
    if shares:
        result.per_share_base = equity_value / shares
    return result


def _run_comps(inputs: Dict[str, Any]) -> ValuationResult:
    peers = [ComparableCompany(**peer) for peer in inputs["peers"]]
    multiple = peer_multiple(peers, trim_fraction=inputs.get("trim_fraction", 0.1))
    equity_value = equity_value_from_multiple(
        metric=inputs["target_metric"],
        multiple=inputs.get("selected_multiple", multiple),
        net_debt=inputs.get("net_debt", 0.0),
        minority_interest=inputs.get("minority_interest", 0.0),
        non_operating_assets=inputs.get("non_operating_assets", 0.0),
    )
    result = ValuationResult(model_name="Comparable Multiples", base_value=equity_value)
    shares = inputs.get("shares_outstanding")
    if shares:
        result.per_share_base = equity_value / shares
    return result


def _run_liquidation(inputs: Dict[str, Any]) -> ValuationResult:
    assets = [AssetRecovery(**asset) for asset in inputs["assets"]]
    liabilities = [LiabilityClaim(**liability) for liability in inputs["liabilities"]]
    equity_value = liquidation_equity_value(
        assets=assets,
        liabilities=liabilities,
        liquidation_costs=inputs.get("liquidation_costs", 0.0),
    )
    return ValuationResult(model_name="Liquidation Value", base_value=equity_value)


def _run_rnpv(inputs: Dict[str, Any]) -> ValuationResult:
    assets = [PipelineAsset(**asset) for asset in inputs["assets"]]
    equity_value = portfolio_rnpv(
        assets=assets,
        discount_rate=inputs["discount_rate"],
        net_cash=inputs.get("net_cash", 0.0),
        corporate_overhead_pv=inputs.get("corporate_overhead_pv", 0.0),
    )
    return ValuationResult(model_name="rNPV", base_value=equity_value)


def _run_reit(inputs: Dict[str, Any]) -> ValuationResult:
    equity_value = reit_equity_value_from_noi(
        noi=inputs["noi"],
        cap_rate=inputs["cap_rate"],
        net_debt=inputs.get("net_debt", 0.0),
        minority_interest=inputs.get("minority_interest", 0.0),
        non_operating_assets=inputs.get("non_operating_assets", 0.0),
    )
    return ValuationResult(model_name="REIT NOI Capitalization", base_value=equity_value)


def _run_cyclical(inputs: Dict[str, Any]) -> ValuationResult:
    metric = inputs.get("normalized_metric")
    if metric is None:
        metric = mid_cycle_metric(inputs["cycle_metrics"])
    equity_value = cyclical_equity_value(
        normalized_metric=metric,
        mid_cycle_multiple=inputs["mid_cycle_multiple"],
        net_debt=inputs.get("net_debt", 0.0),
        minority_interest=inputs.get("minority_interest", 0.0),
        non_operating_assets=inputs.get("non_operating_assets", 0.0),
    )
    return ValuationResult(model_name="Mid-cycle Valuation", base_value=equity_value)


def _run_insurance(inputs: Dict[str, Any]) -> ValuationResult:
    equity_value = insurance_equity_value(
        adjusted_book_value=inputs["adjusted_book_value"],
        value_of_new_business=inputs.get("value_of_new_business", 0.0),
        underwriting_value=inputs.get("underwriting_value", 0.0),
        investment_portfolio_adjustment=inputs.get("investment_portfolio_adjustment", 0.0),
        holding_company_discount=inputs.get("holding_company_discount", 0.0),
    )
    return ValuationResult(model_name="Insurance Embedded Value", base_value=equity_value)


def _run_scenario(inputs: Dict[str, Any]) -> ValuationResult:
    scenarios = [Scenario(**scenario) for scenario in inputs["scenarios"]]
    value = probability_weighted_value(scenarios)
    return ValuationResult(model_name="Scenario-weighted Valuation", base_value=value)


def _run_fintech_brokerage(inputs: Dict[str, Any]) -> ValuationResult:
    equity_value = normalized_earnings_value(
        revenue=inputs["revenue"],
        normalized_margin=inputs["normalized_margin"],
        earnings_multiple=inputs["earnings_multiple"],
        net_debt=inputs.get("net_debt", 0.0),
        non_operating_assets=inputs.get("non_operating_assets", 0.0),
    )
    result = ValuationResult(
        model_name="Fintech / Brokerage Normalized Earnings",
        base_value=equity_value,
        key_assumptions=[
            f"Revenue: {inputs['revenue']}",
            f"Normalized margin: {inputs['normalized_margin']}",
            f"Earnings multiple: {inputs['earnings_multiple']}",
        ],
    )
    shares = inputs.get("shares_outstanding")
    if shares:
        result.per_share_base = equity_value / shares
    return result


MODEL_RUNNERS = {
    "owner_earnings_dcf": _run_owner_earnings_dcf,
    "reverse_dcf": _run_reverse_dcf,
    "epv": _run_epv,
    "nav": _run_nav,
    "residual_income": _run_residual_income,
    "ddm": _run_ddm,
    "sotp": _run_sotp,
    "comps": _run_comps,
    "liquidation": _run_liquidation,
    "rnpv": _run_rnpv,
    "reit": _run_reit,
    "cyclical": _run_cyclical,
    "insurance": _run_insurance,
    "scenario": _run_scenario,
    "fintech_brokerage": _run_fintech_brokerage,
}


def run_valuation(company: CompanyProfile, packet: ValuationInputPacket | Dict[str, Any]) -> ValuationExecution:
    if isinstance(packet, dict):
        packet = ValuationInputPacket.from_dict(packet)

    routing = select_valuation_models(company)
    execution = ValuationExecution(routing=routing)
    execution.gates.extend(_audit_packet(packet))

    blocking_gates = [gate for gate in execution.gates if gate["status"] == "Blocked"]
    if blocking_gates:
        reason = "; ".join(f"{gate['gate']}: {gate['comment']}" for gate in blocking_gates)
        for model_key in packet.model_inputs:
            execution.blocked_models.append({"model": model_key, "reason": reason})
            execution.results.append(_blocked(model_key, reason))
        return execution

    for model_key, raw_inputs in packet.model_inputs.items():
        runner = MODEL_RUNNERS.get(model_key)
        if runner is None:
            execution.blocked_models.append({"model": model_key, "reason": "No Python runner registered"})
            execution.results.append(_blocked(model_key, "No Python runner registered"))
            continue

        assumption_gate = audit_model_assumptions(model_key, packet.structured_assumptions)
        execution.gates.append(
            {
                "gate": f"Structured Assumption: {model_key}",
                "status": assumption_gate.status,
                "comment": "; ".join(assumption_gate.issues + assumption_gate.warnings) or "Assumptions usable.",
            }
        )
        if assumption_gate.status == "Blocked":
            reason = "; ".join(assumption_gate.issues)
            execution.blocked_models.append({"model": model_key, "reason": reason})
            execution.results.append(_blocked(model_key, reason))
            continue

        try:
            result = runner(_unwrap_inputs(raw_inputs))
            result.structured_assumptions = [
                assumption for assumption in packet.structured_assumptions  # type: ignore[assignment]
            ]
            result.assumption_confidence = "low" if assumption_gate.low_confidence else "medium"
            execution.results.append(result)
        except Exception as exc:  # noqa: BLE001 - executor should convert model failures to blocked output.
            reason = str(exc)
            execution.blocked_models.append({"model": model_key, "reason": reason})
            execution.results.append(_blocked(model_key, reason))

    return execution


def run_valuation_payload(company: CompanyProfile, packet: ValuationInputPacket | Dict[str, Any]) -> Dict[str, Any]:
    execution = run_valuation(company, packet)
    return {
        "routing": execution.routing,
        "valuation_summary": execution.valuation_summary(),
        "execution_gate_checklist": execution.gates,
        "blocked_models": execution.blocked_models,
        "results": [asdict(result) for result in execution.results],
    }
