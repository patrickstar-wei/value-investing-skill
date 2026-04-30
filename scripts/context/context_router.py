"""Context router.

Given a task type and target classification, return the minimum set of files
that should be loaded into context.
"""

from typing import Dict, List


BASE_CONTEXT = [
    "SKILL.md",
    "references/context_policy/token_budget_policy.md",
    "references/context_policy/context_manifest.md",
]


TASK_CONTEXT: Dict[str, List[str]] = {
    "quick_check": [
        "commands/quick-check.md",
        "skills/valuation-router/SKILL.md",
    ],
    "full_research": [
        "commands/research.md",
        "skills/value-investing-master/SKILL.md",
        "skills/investment-style-router/SKILL.md",
        "skills/valuation-router/SKILL.md",
        "references/valuation_rules/valuation_model_router.md",
        "references/report_templates/value_investing_report_template.md",
    ],
    "reverse_dcf": [
        "commands/reverse-dcf.md",
        "skills/reverse-dcf/SKILL.md",
        "scripts/valuation/valuation_reverse_dcf.py",
    ],
    "risk": [
        "commands/risk.md",
        "skills/risk-analysis/SKILL.md",
    ],
    "audit": [
        "skills/model-audit/SKILL.md",
        "scripts/audit/assumption_audit.py",
        "scripts/audit/formula_audit.py",
        "scripts/audit/sensitivity_audit.py",
    ],
}


INDUSTRY_CONTEXT: Dict[str, List[str]] = {
    "banking": [
        "references/valuation_rules/valuation_model_router.md",
        "scripts/valuation/valuation_residual_income.py",
    ],
    "biotech": [
        "skills/rnpv-analysis/SKILL.md",
        "scripts/valuation/valuation_biotech_rnpv.py",
    ],
    "quality_compounder": [
        "skills/owner-earnings-dcf/SKILL.md",
        "skills/epv-analysis/SKILL.md",
        "scripts/valuation/valuation_owner_earnings_dcf.py",
        "scripts/valuation/valuation_epv.py",
    ],
}


def route_context(task_type: str, industry_type: str | None = None) -> List[str]:
    files = list(BASE_CONTEXT)
    files.extend(TASK_CONTEXT.get(task_type, []))
    if industry_type:
        files.extend(INDUSTRY_CONTEXT.get(industry_type, []))

    # Deduplicate while preserving order.
    seen = set()
    deduped = []
    for f in files:
        if f not in seen:
            seen.add(f)
            deduped.append(f)
    return deduped


if __name__ == "__main__":
    print(route_context("full_research", "quality_compounder"))
