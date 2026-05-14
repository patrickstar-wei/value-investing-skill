"""Route technology companies to the right cycle and capacity checks."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List


@dataclass(frozen=True)
class TechCycleApplicability:
    cycle_profile: str
    applicability: str
    required_context_packets: List[str] = field(default_factory=list)
    valuation_implications: List[str] = field(default_factory=list)
    required_gates: List[str] = field(default_factory=list)
    rationale: str = ""

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def _contains_any(value: str, words: List[str]) -> bool:
    lower = value.lower()
    return any(word in lower for word in words)


def select_tech_cycle_applicability(company: Any) -> TechCycleApplicability:
    """Classify whether inventory/capacity cycle analysis is required.

    The split mirrors the tech-cycle research note: physical product companies
    need inventory and capacity checks; cloud/AI infrastructure needs capex and
    compute-capacity checks; SaaS needs subscription budget checks; ad platforms
    need advertising demand checks.
    """

    industry = company.industry.lower()

    if company.is_ai_semiconductor_platform or _contains_any(
        industry,
        [
            "semiconductor",
            "chip",
            "hardware",
            "server",
            "network equipment",
            "consumer electronics",
            "storage",
            "pc",
            "phone supply chain",
        ],
    ):
        return TechCycleApplicability(
            cycle_profile="physical_inventory",
            applicability="high",
            required_context_packets=["financial_history", "inventory_cycle", "capacity_cycle"],
            valuation_implications=[
                "normalize gross margin and earnings if inventory or capacity indicators show a cycle high",
                "stress revenue growth when backlog, customer capex, or channel inventory weakens",
                "do not treat peak-cycle margins as permanent free cash flow margins",
            ],
            required_gates=["Financial History Gate", "Inventory Cycle Gate", "Capacity Cycle Gate"],
            rationale="Physical technology products expose reported margins to inventory, channel, and manufacturing capacity cycles.",
        )

    if company.is_hyperscale_cloud_platform or _contains_any(industry, ["cloud", "data center", "ai infrastructure"]):
        return TechCycleApplicability(
            cycle_profile="compute_capacity",
            applicability="medium_high",
            required_context_packets=["financial_history", "compute_capacity_cycle"],
            valuation_implications=[
                "test whether capex and depreciation convert into revenue and free cash flow",
                "lower confidence if AI infrastructure spend grows faster than utilization or segment revenue",
                "model a capex monetization lag when cloud or AI capacity is a core valuation driver",
            ],
            required_gates=["Financial History Gate", "Compute Capacity Gate"],
            rationale="Cloud and AI infrastructure companies have weak inventory signals but strong compute-capacity and depreciation-cycle exposure.",
        )

    if company.is_saas or _contains_any(industry, ["saas", "subscription software", "enterprise software", "cybersecurity", "developer tool"]):
        return TechCycleApplicability(
            cycle_profile="subscription_budget",
            applicability="medium",
            required_context_packets=["financial_history", "subscription_budget_cycle"],
            valuation_implications=[
                "constrain growth assumptions with deferred revenue, billings proxy, RPO, retention, and sales efficiency evidence",
                "distinguish temporary IT budget pressure from product competitiveness deterioration",
            ],
            required_gates=["Financial History Gate", "Subscription Budget Cycle Gate"],
            rationale="Software lacks physical inventory, but subscription and customer-budget indicators constrain durable growth assumptions.",
        )

    if company.is_digital_platform or _contains_any(industry, ["advertising", "social", "streaming", "marketplace", "internet platform"]):
        return TechCycleApplicability(
            cycle_profile="advertising_demand",
            applicability="low_medium",
            required_context_packets=["financial_history", "advertising_demand_cycle"],
            valuation_implications=[
                "stress revenue growth and operating leverage when advertising budgets or engagement weaken",
                "do not require inventory-cycle evidence for asset-light ad platforms",
            ],
            required_gates=["Financial History Gate", "Advertising Demand Cycle Gate"],
            rationale="Platform and advertising companies are more exposed to demand and operating leverage cycles than inventory cycles.",
        )

    if company.has_separable_technology_segment or company.technology_revenue_disclosed:
        return TechCycleApplicability(
            cycle_profile="emerging_technology_optional",
            applicability="low",
            required_context_packets=["financial_history"],
            valuation_implications=[
                "reflect technology only through margin durability, growth quality, and scenario optionality until segment economics are material",
            ],
            required_gates=["Financial History Gate"],
            rationale="Technology exposure is visible but not enough to require a specialist tech-cycle packet.",
        )

    return TechCycleApplicability(
        cycle_profile="not_material",
        applicability="not_applicable",
        required_context_packets=[],
        valuation_implications=[],
        required_gates=[],
        rationale="No material technology cycle exposure detected from the route profile.",
    )
