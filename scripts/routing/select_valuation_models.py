"""Valuation model router v19.

This router classifies a company by economic profile, not by name.
It expands coverage through lazy-loaded workflows while preserving token discipline:
classification first, one primary workflow, at most two auxiliary workflows by default,
then a core investment philosophy / quality gate before final output.
It does not expose scorecards or valuation calculation traces unless requested.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class CompanyProfile:
    industry: str

    # Legacy explicit flags retained for backward compatibility.
    is_bank: bool = False
    is_insurance: bool = False
    is_biotech: bool = False
    is_cyclical: bool = False
    is_asset_heavy: bool = False
    is_high_quality_compounder: bool = False
    is_saas: bool = False
    is_distressed: bool = False

    # v17 explicit specialist route flags.
    is_ai_semiconductor_platform: bool = False
    is_digital_platform: bool = False
    is_hyperscale_cloud_platform: bool = False
    is_managed_care: bool = False
    is_healthcare_services: bool = False
    is_holding_company: bool = False
    is_insurance_float_allocator: bool = False
    is_commodity_deep_cyclical: bool = False
    is_reit_or_infrastructure: bool = False
    is_auto_or_mobility_platform: bool = False
    is_mature_pharma: bool = False
    is_fintech_platform: bool = False
    is_brokerage_platform: bool = False

    # v16 profile scores: use 0/1/2 per factor.
    mature_quality_scores: Dict[str, int] = field(default_factory=dict)
    shareholder_return_scores: Dict[str, int] = field(default_factory=dict)
    technology_optionality_scores: Dict[str, int] = field(default_factory=dict)
    cyclicality_scores: Dict[str, int] = field(default_factory=dict)

    # v17 specialist profile scores: use 0/1/2 per factor.
    ai_semiconductor_scores: Dict[str, int] = field(default_factory=dict)
    digital_platform_scores: Dict[str, int] = field(default_factory=dict)
    cloud_platform_scores: Dict[str, int] = field(default_factory=dict)
    managed_care_scores: Dict[str, int] = field(default_factory=dict)
    holding_company_scores: Dict[str, int] = field(default_factory=dict)
    financial_institution_scores: Dict[str, int] = field(default_factory=dict)
    saas_scores: Dict[str, int] = field(default_factory=dict)
    pharma_scores: Dict[str, int] = field(default_factory=dict)
    commodity_scores: Dict[str, int] = field(default_factory=dict)
    reit_scores: Dict[str, int] = field(default_factory=dict)
    auto_mobility_scores: Dict[str, int] = field(default_factory=dict)
    fintech_scores: Dict[str, int] = field(default_factory=dict)

    # Optional explicit evidence flags.
    has_separable_technology_segment: bool = False
    technology_revenue_disclosed: bool = False
    technology_profit_path_visible: bool = False
    technology_narrative_only: bool = False

    # Optional user/runtime metadata.
    missing_data: List[str] = field(default_factory=list)
    requested_depth: str = "L1"
    max_overlays_default: int = 2


def _score(scores: Dict[str, int]) -> int:
    """Return a bounded total score from a dictionary of 0/1/2 values."""
    total = 0
    for value in scores.values():
        try:
            total += max(0, min(2, int(value)))
        except (TypeError, ValueError):
            continue
    return total


def _route_scores(company: CompanyProfile) -> Dict[str, int]:
    """Compute compact specialist route scores."""
    industry = company.industry.lower()
    scores = {
        "AI / Semiconductor Hypergrowth Platform": _score(company.ai_semiconductor_scores),
        "Digital Platform Compounder": _score(company.digital_platform_scores),
        "Hyperscale Cloud / Digital Infrastructure Platform": _score(company.cloud_platform_scores),
        "Managed Care / Healthcare Services Compounder": _score(company.managed_care_scores),
        "Insurance Float-backed Holding Company": _score(company.holding_company_scores),
        "SaaS / Subscription Software Compounder": _score(company.saas_scores),
        "Mature Pharma / Pipeline Pharma": _score(company.pharma_scores),
        "Commodity / Deep Cyclical Producer": _score(company.commodity_scores),
        "REIT / Infrastructure Yield Asset": _score(company.reit_scores),
        "Auto / EV / Mobility Platform": _score(company.auto_mobility_scores),
        "Fintech / Brokerage Platform": _score(company.fintech_scores),
    }

    # Explicit flags are strong routing evidence.
    if company.is_ai_semiconductor_platform:
        scores["AI / Semiconductor Hypergrowth Platform"] = max(scores["AI / Semiconductor Hypergrowth Platform"], 8)
    if company.is_digital_platform:
        scores["Digital Platform Compounder"] = max(scores["Digital Platform Compounder"], 8)
    if company.is_hyperscale_cloud_platform:
        scores["Hyperscale Cloud / Digital Infrastructure Platform"] = max(scores["Hyperscale Cloud / Digital Infrastructure Platform"], 8)
    if company.is_managed_care or company.is_healthcare_services:
        scores["Managed Care / Healthcare Services Compounder"] = max(scores["Managed Care / Healthcare Services Compounder"], 8)
    if company.is_holding_company or company.is_insurance_float_allocator:
        scores["Insurance Float-backed Holding Company"] = max(scores["Insurance Float-backed Holding Company"], 8)
    if company.is_saas:
        scores["SaaS / Subscription Software Compounder"] = max(scores["SaaS / Subscription Software Compounder"], 8)
    if company.is_mature_pharma or company.is_biotech:
        scores["Mature Pharma / Pipeline Pharma"] = max(scores["Mature Pharma / Pipeline Pharma"], 8 if company.is_mature_pharma else 5)
    if company.is_commodity_deep_cyclical:
        scores["Commodity / Deep Cyclical Producer"] = max(scores["Commodity / Deep Cyclical Producer"], 8)
    if company.is_reit_or_infrastructure:
        scores["REIT / Infrastructure Yield Asset"] = max(scores["REIT / Infrastructure Yield Asset"], 8)
    if company.is_auto_or_mobility_platform:
        scores["Auto / EV / Mobility Platform"] = max(scores["Auto / EV / Mobility Platform"], 8)
    if company.is_fintech_platform or company.is_brokerage_platform:
        scores["Fintech / Brokerage Platform"] = max(scores["Fintech / Brokerage Platform"], 8)

    # Industry keywords are weak evidence, used only for fallback classification.
    keyword_boosts = {
        "semiconductor": "AI / Semiconductor Hypergrowth Platform",
        "chip": "AI / Semiconductor Hypergrowth Platform",
        "platform": "Digital Platform Compounder",
        "internet": "Digital Platform Compounder",
        "cloud": "Hyperscale Cloud / Digital Infrastructure Platform",
        "managed care": "Managed Care / Healthcare Services Compounder",
        "health insurance": "Managed Care / Healthcare Services Compounder",
        "holding company": "Insurance Float-backed Holding Company",
        "reit": "REIT / Infrastructure Yield Asset",
        "infrastructure": "REIT / Infrastructure Yield Asset",
        "oil": "Commodity / Deep Cyclical Producer",
        "mining": "Commodity / Deep Cyclical Producer",
        "auto": "Auto / EV / Mobility Platform",
        "ev": "Auto / EV / Mobility Platform",
        "fintech": "Fintech / Brokerage Platform",
        "brokerage": "Fintech / Brokerage Platform",
        "broker": "Fintech / Brokerage Platform",
        "trading app": "Fintech / Brokerage Platform",
    }
    for word, route in keyword_boosts.items():
        if word in industry:
            scores[route] = max(scores[route], 4)
    return scores


def _base_type(company: CompanyProfile) -> str:
    industry = company.industry.lower()

    # Specialist routes first when explicit; they prevent generic DCF misuse.
    route_scores = _route_scores(company)
    best_route, best_score = max(route_scores.items(), key=lambda kv: kv[1])
    if best_score >= 7:
        return best_route

    # Regulated financials and special cases.
    if company.is_bank or industry == "banking":
        return "Bank"
    if company.is_insurance:
        return "Insurance"
    if company.is_biotech:
        return "Biotech"
    if company.is_distressed:
        return "Distressed"
    if company.is_asset_heavy:
        return "Asset-heavy"
    if company.is_saas:
        return "SaaS / Subscription Software Compounder"
    if company.is_cyclical and not company.is_high_quality_compounder:
        return "Cyclical"

    mature_quality_score = _score(company.mature_quality_scores)
    technology_score = _score(company.technology_optionality_scores)

    if company.is_high_quality_compounder or mature_quality_score >= 7:
        if technology_score >= 6 or company.has_separable_technology_segment:
            return "Tech-enabled Mature Quality Compounder"
        return "Mature Quality Compounder"

    if best_score >= 4:
        # Weak evidence only: return broad route with medium/low confidence.
        return best_route

    return "General Business"


def _base_models(base_type: str) -> Dict[str, str]:
    table = {
        "Bank": {
            "primary": "Residual Income / P/B-ROE",
            "cross_check": "P/E, DDM where dividends are stable",
            "downside": "Tangible Book Value / credit stress",
            "implied": "Implied ROE / credit loss expectations",
        },
        "Insurance": {
            "primary": "P/B + underwriting profitability / embedded value where applicable",
            "cross_check": "Combined ratio, investment income, DDM",
            "downside": "Adjusted Book Value / reserve stress",
            "implied": "Implied ROE / combined ratio",
        },
        "Biotech": {
            "primary": "rNPV",
            "cross_check": "Pipeline SOTP",
            "downside": "Net Cash / Cash Burn",
            "implied": "Implied Approval Probability",
        },
        "Cyclical": {
            "primary": "Mid-cycle Valuation",
            "cross_check": "Normalized EV/EBITDA",
            "downside": "Downcycle Earnings / Balance Sheet Stress",
            "implied": "Implied Cycle Recovery",
        },
        "Distressed": {
            "primary": "Liquidation Value",
            "cross_check": "SOTP / NAV",
            "downside": "Net Cash Recovery",
            "implied": "Expected Value",
        },
        "Asset-heavy": {
            "primary": "NAV / Replacement Cost",
            "cross_check": "EV/EBITDA",
            "downside": "Liquidation Value",
            "implied": "Implied Asset Discount",
        },
        "SaaS / Subscription Software Compounder": {
            "primary": "Revenue build-up DCF / long-term FCF margin path",
            "cross_check": "EV/Revenue, EV/Gross Profit, Rule of 40",
            "downside": "Growth deceleration + SBC dilution stress",
            "implied": "Reverse DCF / implied terminal FCF margin",
        },
        "Mature Quality Compounder": {
            "primary": "Owner Earnings DCF / FCFE DCF",
            "cross_check": "EPV / Quality-adjusted P/E / Normalized P/E",
            "downside": "No-growth EPV",
            "implied": "Reverse DCF",
        },
        "Tech-enabled Mature Quality Compounder": {
            "primary": "Owner Earnings DCF / FCFE DCF",
            "cross_check": "EPV / Quality-adjusted P/E / SOTP if material",
            "downside": "No-growth EPV + Stress FCF",
            "implied": "Reverse DCF",
        },
        "AI / Semiconductor Hypergrowth Platform": {
            "primary": "Scenario-weighted DCF",
            "cross_check": "EV/Sales, EV/Gross Profit, EV/EBIT, peer multiple sanity check",
            "downside": "Cycle-normalized earnings + gross margin stress + export-control stress",
            "implied": "Reverse DCF / implied TAM penetration",
        },
        "Digital Platform Compounder": {
            "primary": "Segment SOTP + Owner Earnings DCF",
            "cross_check": "EV/EBIT, normalized FCF yield, segment multiples",
            "downside": "Regulatory / margin / advertising-cycle stress case",
            "implied": "Reverse DCF / implied platform growth",
        },
        "Hyperscale Cloud / Digital Infrastructure Platform": {
            "primary": "Segment DCF for cloud / AI infrastructure",
            "cross_check": "EV/EBIT, EV/Sales, peer cloud multiple sanity check",
            "downside": "CapEx intensity + margin normalization stress",
            "implied": "Implied cloud revenue growth and terminal margin",
        },
        "Managed Care / Healthcare Services Compounder": {
            "primary": "Normalized EPS / FCFE DCF",
            "cross_check": "P/E band + SOTP for healthcare service segments",
            "downside": "Medical Loss Ratio and regulatory stress",
            "implied": "Implied EPS growth / margin recovery",
        },
        "Insurance Float-backed Holding Company": {
            "primary": "SOTP + look-through earnings",
            "cross_check": "Adjusted book value / investment portfolio NAV",
            "downside": "Underwriting stress + market drawdown stress",
            "implied": "Implied return on retained capital / float economics",
        },
        "Mature Pharma / Pipeline Pharma": {
            "primary": "Product cash-flow DCF + pipeline rNPV where material",
            "cross_check": "P/E, EV/EBITDA, patent-cliff-adjusted earnings",
            "downside": "Patent cliff / pipeline failure stress",
            "implied": "Implied product growth and pipeline success",
        },
        "Commodity / Deep Cyclical Producer": {
            "primary": "Mid-cycle EBITDA / commodity price scenario model",
            "cross_check": "EV/EBITDA, NAV, reserve value",
            "downside": "Downcycle commodity price + balance sheet stress",
            "implied": "Implied commodity price / cycle recovery",
        },
        "REIT / Infrastructure Yield Asset": {
            "primary": "AFFO / NOI capitalization / DCF",
            "cross_check": "NAV, cap rate, distribution yield",
            "downside": "Leverage, refinancing, occupancy, rate stress",
            "implied": "Implied cap rate / AFFO growth",
        },
        "Auto / EV / Mobility Platform": {
            "primary": "Normalized manufacturing earnings + software/optionality layer",
            "cross_check": "EV/EBIT, unit economics, battery/software attach-rate check",
            "downside": "Auto-cycle, price-war, and margin stress",
            "implied": "Implied vehicle volume, margin, and software value",
        },
        "Fintech / Brokerage Platform": {
            "primary": "Revenue build-up DCF / normalized earnings",
            "cross_check": "EV/Revenue, EV/EBITDA, AUC/user-based comps",
            "downside": "Rate decline + crypto volume stress + regulatory stress",
            "implied": "Reverse DCF / implied ARPU and funded customer growth",
        },
    }
    return table.get(
        base_type,
        {
            "primary": "Scenario DCF",
            "cross_check": "Relative Valuation",
            "downside": "Balance Sheet Downside",
            "implied": "Reverse DCF",
        },
    )


def _overlay_tags(company: CompanyProfile) -> List[str]:
    overlays: List[str] = []

    shareholder_return_score = _score(company.shareholder_return_scores)
    technology_score = _score(company.technology_optionality_scores)
    cyclicality_score = _score(company.cyclicality_scores)
    cloud_score = _score(company.cloud_platform_scores)

    if shareholder_return_score >= 6:
        overlays.append("Dividend / Shareholder Return Overlay")

    if company.technology_narrative_only or technology_score <= 3:
        if technology_score > 0 or company.technology_narrative_only:
            overlays.append("Technology Narrative Only - No Separate Premium")
    elif technology_score >= 6 or company.has_separable_technology_segment:
        overlays.append("Technology Optionality Overlay")
    elif technology_score > 0:
        overlays.append("Technology Efficiency / Emerging Optionality")

    if cloud_score >= 6 and not company.is_hyperscale_cloud_platform:
        overlays.append("Cloud / AI Infrastructure Overlay")

    if cyclicality_score >= 4 or (company.is_cyclical and company.is_high_quality_compounder):
        overlays.append("Light Cyclical Manufacturing Overlay")

    # Token discipline: L0/L1 default caps overlays to the most material two.
    if company.requested_depth in {"L0", "L1"}:
        return overlays[: max(0, company.max_overlays_default)]
    return overlays


def _overlay_models(overlays: List[str], company: CompanyProfile) -> Dict[str, List[str]]:
    models: Dict[str, List[str]] = {}

    if "Dividend / Shareholder Return Overlay" in overlays:
        models["dividend_models"] = [
            "Two-stage DDM",
            "Gordon Growth terminal check",
            "Dividend Yield Band",
            "Shareholder Yield: Dividend Yield + Net Buyback Yield + Debt Reduction Yield",
            "Dividend Safety / Payout Stress Test",
            "Implied Dividend Growth",
        ]

    if "Technology Optionality Overlay" in overlays:
        if company.has_separable_technology_segment or company.technology_revenue_disclosed:
            models["technology_models"] = [
                "SOTP for material separable technology segment",
                "Scenario-weighted optionality",
                "Comparable multiple cross-check if peer set is credible",
            ]
        else:
            models["technology_models"] = [
                "Scenario-weighted optionality only",
                "No core valuation premium without segment evidence",
            ]
    elif "Technology Efficiency / Emerging Optionality" in overlays:
        models["technology_models"] = [
            "Reflect in margin, FCF conversion, ROIC, and moat quality",
            "No separate SOTP unless financial contribution becomes material",
        ]
    elif "Technology Narrative Only - No Separate Premium" in overlays:
        models["technology_models"] = [
            "No separate valuation premium",
            "Mention only as low-confidence optional upside",
        ]

    if "Cloud / AI Infrastructure Overlay" in overlays:
        models["cloud_models"] = [
            "Cloud segment DCF or SOTP if material",
            "AI capex and terminal margin sensitivity",
            "EV/EBIT or EV/Sales peer sanity check",
        ]

    if "Light Cyclical Manufacturing Overlay" in overlays:
        models["cyclicality_models"] = [
            "Mid-cycle earnings",
            "Normalized margin",
            "Stress-case FCF",
            "No-growth EPV",
        ]

    return models


def _deferred_routes(base_type: str, overlays: List[str]) -> List[str]:
    all_routes = [
        "AI / Semiconductor Hypergrowth Platform",
        "Digital Platform Compounder",
        "Hyperscale Cloud / Digital Infrastructure Platform",
        "Managed Care / Healthcare Services Compounder",
        "Insurance Float-backed Holding Company",
        "Financial Institution: Bank / Insurance / Asset Manager",
        "SaaS / Subscription Software Compounder",
        "Mature Pharma / Pipeline Pharma",
        "Commodity / Deep Cyclical Producer",
        "REIT / Infrastructure Yield Asset",
        "Auto / EV / Mobility Platform",
        "Fintech / Brokerage Platform",
        "Dividend / Shareholder Return Overlay",
        "Technology Optionality Overlay",
        "Light Cyclical Manufacturing Overlay",
    ]
    active = {base_type, *overlays}
    # Keep output compact: do not list every irrelevant route for very generic cases.
    return [r for r in all_routes if r not in active][:8]


def _confidence(company: CompanyProfile, base_type: str) -> str:
    if company.missing_data:
        return "medium" if len(company.missing_data) <= 3 else "low"
    route_scores = _route_scores(company)
    if base_type in route_scores and 0 < route_scores[base_type] < 7:
        return "medium"
    return "high"


def _workflow_for_base_type(base_type: str) -> str:
    mapping = {
        "Mature Quality Compounder": "workflows/01_quality_company.md",
        "Tech-enabled Mature Quality Compounder": "workflows/01_quality_company.md",
        "Digital Platform Compounder": "workflows/03_tech_platform.md",
        "Hyperscale Cloud / Digital Infrastructure Platform": "workflows/03_tech_platform.md",
        "AI / Semiconductor Hypergrowth Platform": "workflows/04_ai_semiconductor.md",
        "Managed Care / Healthcare Services Compounder": "workflows/05_healthcare_managed_care.md",
        "Insurance Float-backed Holding Company": "workflows/06_holding_company.md",
        "REIT / Infrastructure Yield Asset": "workflows/07_reit_infrastructure.md",
        "Commodity / Deep Cyclical Producer": "workflows/08_cyclical_commodity.md",
        "Cyclical": "workflows/08_cyclical_commodity.md",
        "SaaS / Subscription Software Compounder": "workflows/03_tech_platform.md",
        "Mature Pharma / Pipeline Pharma": "workflows/05_healthcare_managed_care.md",
        "Auto / EV / Mobility Platform": "workflows/08_cyclical_commodity.md",
        "Fintech / Brokerage Platform": "workflows/10_fintech_brokerage.md",
        "Bank": "workflows/00_router.md",
        "Insurance": "workflows/06_holding_company.md",
        "Asset-heavy": "workflows/07_reit_infrastructure.md",
        "Distressed": "workflows/00_router.md",
    }
    return mapping.get(base_type, "workflows/00_router.md")


def _auxiliary_workflows(overlays: List[str], company: CompanyProfile) -> List[str]:
    aux: List[str] = []
    if "Dividend / Shareholder Return Overlay" in overlays:
        aux.append("workflows/02_dividend_compounder.md")
    if any(o in overlays for o in ["Technology Optionality Overlay", "Technology Efficiency / Emerging Optionality", "Technology Narrative Only - No Separate Premium", "Cloud / AI Infrastructure Overlay"]):
        aux.append("workflows/03_tech_platform.md")
    if "Light Cyclical Manufacturing Overlay" in overlays:
        aux.append("workflows/08_cyclical_commodity.md")
    # Preserve order and cap for L0/L1.
    unique: List[str] = []
    for item in aux:
        if item not in unique:
            unique.append(item)
    if company.requested_depth in {"L0", "L1"}:
        return unique[: max(0, company.max_overlays_default)]
    return unique


def _active_route_files(base_type: str) -> List[str]:
    files = [
        "SKILL.md",
        "references/core/investment_philosophy_layer.md",
        "references/core/investment_quality_gate.md",
        "references/core/modular_workflow_architecture.md",
        "references/output_policy/mandatory_output_contract.md",
        "references/output_policy/fixed_report_renderer.md",
        "references/output_policy/output_validation_rules.md",
        "references/valuation_rules/token_efficient_routing_policy_v17.md",
        "references/valuation_rules/structured_assumption_policy.md",
        "scripts/routing/select_valuation_models.py",
        "scripts/report/generate_markdown.py",
    ]
    if base_type in {
        "AI / Semiconductor Hypergrowth Platform",
        "Digital Platform Compounder",
        "Hyperscale Cloud / Digital Infrastructure Platform",
        "Managed Care / Healthcare Services Compounder",
        "Insurance Float-backed Holding Company",
        "SaaS / Subscription Software Compounder",
        "Mature Pharma / Pipeline Pharma",
        "Commodity / Deep Cyclical Producer",
        "REIT / Infrastructure Yield Asset",
        "Auto / EV / Mobility Platform",
        "Fintech / Brokerage Platform",
    }:
        files.append("references/valuation_rules/specialized_company_routes_v17.md:selected_section_only")
    else:
        files.append("references/valuation_rules/valuation_model_router.md")
    return files


def _valuation_algorithm_files(base_type: str, overlays: List[str]) -> List[str]:
    files_by_base_type = {
        "Bank": [
            "scripts/valuation/valuation_residual_income.py",
        ],
        "Insurance": [
            "scripts/valuation/valuation_insurance.py",
        ],
        "Biotech": [
            "scripts/valuation/valuation_rnpv.py",
        ],
        "Cyclical": [
            "scripts/valuation/valuation_cyclical.py",
        ],
        "Distressed": [
            "scripts/valuation/valuation_liquidation.py",
            "scripts/valuation/valuation_nav.py",
        ],
        "Asset-heavy": [
            "scripts/valuation/valuation_nav.py",
            "scripts/valuation/valuation_liquidation.py",
        ],
        "SaaS / Subscription Software Compounder": [
            "scripts/valuation/valuation_scenario.py",
            "scripts/valuation/valuation_reverse_dcf.py",
            "scripts/valuation/valuation_comps.py",
        ],
        "Mature Quality Compounder": [
            "scripts/valuation/valuation_owner_earnings_dcf.py",
            "scripts/valuation/valuation_epv.py",
            "scripts/valuation/valuation_reverse_dcf.py",
        ],
        "Tech-enabled Mature Quality Compounder": [
            "scripts/valuation/valuation_owner_earnings_dcf.py",
            "scripts/valuation/valuation_epv.py",
            "scripts/valuation/valuation_sotp.py",
            "scripts/valuation/valuation_reverse_dcf.py",
        ],
        "AI / Semiconductor Hypergrowth Platform": [
            "scripts/valuation/valuation_scenario.py",
            "scripts/valuation/valuation_reverse_dcf.py",
            "scripts/valuation/valuation_comps.py",
        ],
        "Digital Platform Compounder": [
            "scripts/valuation/valuation_sotp.py",
            "scripts/valuation/valuation_owner_earnings_dcf.py",
            "scripts/valuation/valuation_reverse_dcf.py",
            "scripts/valuation/valuation_comps.py",
        ],
        "Hyperscale Cloud / Digital Infrastructure Platform": [
            "scripts/valuation/valuation_scenario.py",
            "scripts/valuation/valuation_sotp.py",
            "scripts/valuation/valuation_comps.py",
        ],
        "Managed Care / Healthcare Services Compounder": [
            "scripts/valuation/valuation_owner_earnings_dcf.py",
            "scripts/valuation/valuation_comps.py",
        ],
        "Insurance Float-backed Holding Company": [
            "scripts/valuation/valuation_sotp.py",
            "scripts/valuation/valuation_insurance.py",
            "scripts/valuation/valuation_nav.py",
        ],
        "Mature Pharma / Pipeline Pharma": [
            "scripts/valuation/valuation_owner_earnings_dcf.py",
            "scripts/valuation/valuation_rnpv.py",
            "scripts/valuation/valuation_comps.py",
        ],
        "Commodity / Deep Cyclical Producer": [
            "scripts/valuation/valuation_cyclical.py",
            "scripts/valuation/valuation_nav.py",
        ],
        "REIT / Infrastructure Yield Asset": [
            "scripts/valuation/valuation_reit.py",
            "scripts/valuation/valuation_nav.py",
        ],
        "Auto / EV / Mobility Platform": [
            "scripts/valuation/valuation_cyclical.py",
            "scripts/valuation/valuation_scenario.py",
            "scripts/valuation/valuation_comps.py",
        ],
        "Fintech / Brokerage Platform": [
            "scripts/valuation/valuation_fintech.py",
            "scripts/valuation/valuation_scenario.py",
            "scripts/valuation/valuation_reverse_dcf.py",
            "scripts/valuation/valuation_comps.py",
        ],
    }
    files = ["scripts/valuation/valuation_common.py"]
    files.extend(files_by_base_type.get(base_type, ["scripts/valuation/valuation_scenario.py"]))

    if "Dividend / Shareholder Return Overlay" in overlays:
        files.append("scripts/valuation/valuation_ddm.py")
    if "Technology Optionality Overlay" in overlays or "Cloud / AI Infrastructure Overlay" in overlays:
        files.extend(["scripts/valuation/valuation_sotp.py", "scripts/valuation/valuation_scenario.py"])
    if "Light Cyclical Manufacturing Overlay" in overlays:
        files.append("scripts/valuation/valuation_cyclical.py")

    unique: List[str] = []
    for file in files:
        if file not in unique:
            unique.append(file)
    return unique


def select_valuation_models(company: CompanyProfile) -> Dict[str, object]:
    """Return a v19 token-efficient modular workflow routing decision.

    The returned dictionary preserves legacy keys: primary, cross_check,
    downside, and implied.
    """
    base_type = _base_type(company)
    base_models = _base_models(base_type)
    overlays = _overlay_tags(company)
    overlay_models = _overlay_models(overlays, company)
    route_scores = _route_scores(company)

    result: Dict[str, object] = {
        "skill_version": "v19",
        "base_type": base_type,
        "overlays": overlays,
        "primary_workflow": _workflow_for_base_type(base_type),
        "auxiliary_workflows": _auxiliary_workflows(overlays, company),
        "core_quality_gate": {
            "investment_philosophy_layer": "references/core/investment_philosophy_layer.md",
            "investment_quality_gate": "references/core/investment_quality_gate.md",
            "required_final_labels": [
                "Business Quality",
                "Valuation Attractiveness",
                "Margin of Safety",
                "Data Confidence",
                "Action",
            ],
            "show_gate_internals_by_default": False,
        },
        **base_models,
        "overlay_models": overlay_models,
        "missing_data": company.missing_data,
        "confidence": _confidence(company, base_type),
        "active_route_files": _active_route_files(base_type),
        "valuation_algorithm_files": _valuation_algorithm_files(base_type, overlays),
        "deferred_routes": _deferred_routes(base_type, overlays),
        "token_mode": "lazy_loaded_modular_workflow",
        "token_control": {
            "classification_first": True,
            "one_primary_workflow": True,
            "max_default_auxiliary_workflows": company.max_overlays_default if company.requested_depth in {"L0", "L1"} else "depth_allows_more",
            "show_internal_scorecard_by_default": False,
            "show_calculation_trace_by_default": False,
            "show_quality_gate_internals_by_default": False,
        },
        "support_level": "supported with specialized route" if base_type in route_scores and route_scores[base_type] >= 7 else "direct or general support",
        "user_facing_rule": (
            "Show classification, selected workflow, activated model stack, deferred modules, "
            "business quality, valuation attractiveness, Bear/Base/Bull valuation range, current price, "
            "margin of safety, price zones, position-aware actions, data confidence, key assumptions, "
            "sensitivity, and thesis-breaking risks only. "
            "Do not expose internal scorecards, quality-gate internals, or step-by-step calculation traces unless requested."
        ),
        "output_contract": {
            "renderer": "references/output_policy/fixed_report_renderer.md",
            "validator": "references/output_policy/output_validation_rules.md",
            "valuation_range_required": True,
            "price_zones_required": True,
            "position_aware_actions_required": True,
            "calculation_trace_visible_by_default": False,
        },
    }
    return result


if __name__ == "__main__":
    sample = CompanyProfile(
        industry="ai semiconductor",
        is_ai_semiconductor_platform=True,
        ai_semiconductor_scores={
            "ai_revenue_growth": 2,
            "margin_durability": 2,
            "tam_expansion": 2,
            "customer_concentration": 1,
        },
    )
    print(select_valuation_models(sample))
