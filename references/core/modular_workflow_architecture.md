# Modular Workflow Architecture v17.2

## Purpose

Preserve broad investment-analysis capability without turning the core skill into a token-heavy monolith.

## Architecture

```text
Core Skill
├── Investment Philosophy Layer
├── Investment Quality Gate
├── Lightweight Router
├── Shared Output Policy
└── Lazy-loaded Workflows
```

## Runtime rule

Default runtime pattern:

```text
Classify task → classify company → select 1 primary workflow → add at most 2 auxiliary workflows → run quality gate → output concise pyramid report
```

## Workflow activation cap

For L0/L1 analysis:

- exactly one primary workflow
- maximum two auxiliary workflows
- no calculation trace
- no internal scorecard
- list deferred workflows only if material

For L2/L3/L4 analysis, more workflows may be activated only when the user asks for a full memo, model audit, or multi-company comparison.

## Primary workflows

| Workflow | Use When |
|---|---|
| `01_quality_company.md` | Mature high-quality cash-flow businesses |
| `02_dividend_compounder.md` | Dividends, buybacks, or shareholder yield materially drive return |
| `03_tech_platform.md` | Search, ads, cloud, app stores, marketplaces, or multi-segment digital platforms |
| `04_ai_semiconductor.md` | AI accelerators, semiconductor platforms, equipment, foundry or AI infrastructure suppliers |
| `05_healthcare_managed_care.md` | Managed care, health insurance, PBM, healthcare services platforms |
| `06_holding_company.md` | Insurance float, conglomerates, investment holding companies |
| `07_reit_infrastructure.md` | REITs, infrastructure yield assets, rate-sensitive asset owners |
| `08_cyclical_commodity.md` | Deep cyclicals, commodities, shipping, mining, energy producers |
| `09_watchlist_compare.md` | Watchlists, multi-company ranking, peer comparison |

## Core Skill boundaries

The Core Skill should not contain full domain-specific valuation logic. It should contain:

- philosophy
- router rules
- model-fit discipline
- output policy
- data confidence policy
- no-calculation-trace policy
- workflow activation cap

Domain details live in workflow files.
