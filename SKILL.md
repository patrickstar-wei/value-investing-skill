---
name: value-investing-research
description: Use for value-oriented company or stock analysis, intrinsic value estimation, reverse DCF, margin-of-safety checks, investment memos, earnings reviews, valuation model routing, structured assumption audits, and investor action price zones. Supports Codex and Claude skill usage with lazy-loaded references, executable Python valuation scripts, and fixed bilingual report output.
---

# Value Investing Core Skill v19.2

## Purpose

Perform value-oriented investment research with business-quality discipline, valuation model routing, structured assumptions, executable Python valuation, data provenance checks, master-investor lenses, and fixed decision-oriented output.

This file is the compact entrypoint for both Codex and Claude. Detailed rules live in `references/`, workflows live in `workflows/`, and deterministic calculations live in `scripts/`.

## Trigger Conditions

Use this skill when the user asks to:

- analyze a stock, company, industry, or investment opportunity
- estimate intrinsic value or margin of safety
- run reverse DCF, DCF, SOTP, EPV, NAV, DDM, residual-income, rNPV, REIT, insurance, cyclical, fintech, or scenario valuation
- build, audit, or explain a valuation model
- generate an investment memo, earnings review, thesis update, risk review, or price/action framework
- compare companies or check whether a company type is supported

## Progressive Loading Rule

Do not load all references, formulas, workflows, master files, or source materials by default.

Default context pattern:

```text
Request -> Context Manifest -> Router -> One Primary Workflow -> Needed Policies -> Scripts -> Fixed Renderer
```

Read first for normal analysis:

- `references/context_policy/token_budget_policy.md`
- `references/context_policy/context_manifest.md`

Use the context manifest as the navigation index for task-specific files.

## Non-Overridable Investment Principles

Every stock/company analysis must obey:

1. Business quality before valuation.
2. Cash-flow reality over accounting appearance.
3. Valuation model must match company type.
4. Margin of safety is required.
5. Evidence must support every investment conclusion.
6. Bear-case discipline is mandatory.
7. Calculation trace is internal by default.
8. Data confidence gates the action.
9. Good business and good price must be judged separately.
10. Missing or stale data must be flagged or blocked.

Load for the core philosophy and quality gate:

- `references/core/investment_philosophy_layer.md`
- `references/core/investment_quality_gate.md`
- `references/core/modular_workflow_architecture.md`

## Standard Workflow

For L1/L2 current company analysis:

1. Infer output language from the user's latest request unless explicitly overridden.
2. Classify task depth: L0 quick check, L1 standard report, L2 full memo, L3 committee pack, L4 audit package.
3. Identify target, ticker, market, industry, lifecycle, and likely business type.
4. Use `scripts/context/context_router.py` and `references/context_policy/context_manifest.md` to select the smallest useful context packet.
5. Route to one primary workflow and no more than two auxiliary workflows for L0/L1.
6. Classify the company by evidence, not name alone:
   - Base Business Type
   - Shareholder Return Overlay
   - Technology Optionality Overlay
   - Cyclicality / Risk Overlay
7. Route valuation models:
   - primary model
   - cross-check model
   - downside model
   - implied-expectation / reverse DCF model
   - material overlay models only
8. Proactively fetch or verify public data that does not require user credentials or files.
9. Convert important inputs into structured assumptions with evidence, confidence, and sensitivity.
10. Bind model inputs to source metadata where possible with `schemas/valuation_input_packet.schema.json`.
11. Run Python valuation scripts instead of expanding formulas in the prompt. Prefer `scripts/valuation/valuation_executor.py` when a routed model execution is possible.
12. Audit assumptions, formulas, data lineage, freshness, and sensitivity internally.
13. Render through the fixed report contract. Workflows must not directly create custom final reports.
14. End the report with optional user-provided data suggestions that would improve assumption quality.

## Public Data Default

For normal L1/L2 analysis, do not wait for user-provided data before doing the public-data version unless the analysis is blocked.

Proactively use or check:

- official filings, annual reports, 10-K / 10-Q, exchange filings, earnings releases, IR pages, presentations, and management guidance
- current price, market capitalization, shares, rates, and FX where material
- public peer, customer, supplier, capex, industry, regulatory, and news sources where material
- public market data helpers such as yfinance / OpenBB only if the runtime has a working connector; otherwise use verifiable web or official sources

Available public-data connectors:

- Public-data orchestrator: `scripts/connectors/public_data_packet_builder.py` builds one auditable packet from the available free/public connectors before valuation.
- P0 SEC EDGAR: `scripts/connectors/sec_edgar_connector.py` for free official SEC submissions, latest filings, and XBRL companyfacts.
- P1 yfinance / Yahoo Finance: `scripts/connectors/yfinance_connector.py` for free third-party quotes, market cap, shares, and basic market data. Treat as Tier 3 and cross-check when material.
- P2 public IR release parser: `scripts/connectors/ir_release_parser.py` for public earnings releases, guidance snippets, and event evidence. Reconcile key numbers to official filings when available.

When a ticker is compatible with these connectors, run or emulate the public-data orchestrator first and use its `sources_used`, `missing_data`, and `errors` fields to drive the data provenance and final optional-data suggestions.

At the end of the report, suggest optional user-provided inputs only as quality enhancers:

- Bloomberg / FactSet / Refinitiv consensus exports
- broker paid-research summaries or structured exports
- the user's cost basis, position size, risk budget, and time horizon
- private notes or internal materials
- Wind / Choice / Morningstar exports
- licensed datasets or local files

OpenBB optional provider template:

- Template: `config/openbb_providers.template.json`
- Local secrets file: `config/openbb_providers.local.json` (ignored by git)
- Runtime check: `scripts/connectors/openbb_provider_config.py`
- Use OpenBB data only when the package is installed and at least one enabled provider has a key from the local config or environment.

Do not bypass paywalls, store credentials in git, commit paid exports, reproduce long paid-report excerpts, or treat institutional target prices as intrinsic value.

Claude package / copy installs exclude expanded master source materials by default. Use the compact `references/masters/*.md` cards during normal analysis; load source materials only when explicitly needed or when the user opts into packaging them.

Load if institutional views are actually provided:

- `skills/institutional-view-ingestion/SKILL.md`
- `references/data_source_policy/institutional_view_policy.md`
- `schemas/institutional_view.schema.json`
- `scripts/connectors/institutional_view_parser.py`

## Routing Files

Use these routers and policies when a current stock/company analysis needs classification or valuation model selection:

- `workflows/00_router.md`
- `skills/valuation-router/SKILL.md`
- `references/valuation_rules/company_classification_routing_policy.md`
- `references/valuation_rules/token_efficient_routing_policy_v17.md`
- `references/valuation_rules/structured_assumption_policy.md`
- `references/valuation_rules/company_type_coverage_matrix_v17.md` when coverage is uncertain or requested
- `references/valuation_rules/specialized_company_routes_v17.md` only for specialist company types
- `scripts/routing/select_valuation_models.py`

Primary workflows:

- `workflows/01_quality_company.md`
- `workflows/02_dividend_compounder.md`
- `workflows/03_tech_platform.md`
- `workflows/04_ai_semiconductor.md`
- `workflows/05_healthcare_managed_care.md`
- `workflows/06_holding_company.md`
- `workflows/07_reit_infrastructure.md`
- `workflows/08_cyclical_commodity.md`
- `workflows/09_watchlist_compare.md`
- `workflows/10_fintech_brokerage.md`

Default L0/L1 route cap:

- one base route
- one primary workflow
- no more than two auxiliary workflows
- one primary model
- one or two cross-check models
- one downside model
- one implied-expectation model
- defer non-material modules instead of expanding them

## Master Lenses

Use `references/masters/multi_master_framework.md` as the index. Load individual files under `references/masters/` only when materially relevant to the selected workflow or explicitly requested.

Default lens mapping:

- Quality / dividend / holding company: Buffett-Munger, Graham, Greenwald as relevant
- Tech platform: Buffett-Munger, Fisher, Mauboussin-Rappaport, Damodaran
- AI semiconductor: Fisher, Mauboussin-Rappaport, Howard Marks, Damodaran
- Cyclical / commodity: Howard Marks, Graham, Greenwald
- Action / position overlay: Jin Jiancheng when the analysis needs price zones, staged add/trim rules, cash reserve discipline, U.S. equity / ETF context, or a check on whether a drawdown is temporary shock versus fundamental change

The final report must include a compact `Master Lens Used` section with rationale and impact. Do not dump every master framework.

## Output Contract

Every standard stock/company report must obey:

- `references/output_policy/mandatory_output_contract.md`
- `references/output_policy/workflow_payload_contract.md`
- `references/output_policy/fixed_report_renderer.md`
- `references/output_policy/output_validation_rules.md`

Required final fields unless irrelevant or data-blocked:

- Bear / Base / Bull intrinsic value range
- current price
- margin of safety
- valuation status
- selected models
- key assumptions
- structured assumptions where material
- sensitivity summary
- conclusion change triggers
- price zones: Deep Value, Accumulation, Watchlist, Fair Value, Trim, Sell / Avoid
- price zone assumption basis
- position-aware suggestions: Empty, Half, Full, Overweight
- tranche plan: starter, add, strong-add, hold, trim, exit-review
- thesis conditions: add only if, hold only if, trim if, exit or avoid if
- execution gate checklist
- data provenance
- public data sources used / checked
- optional user-provided data suggestions

If valuation data is missing, keep the Valuation Summary and Investor Action Framework, mark affected fields as `Blocked`, explain missing inputs, and provide non-price-based next steps.

Do not show formulas, spreadsheet-style steps, internal routing scorecards, quality-gate internals, discount schedules, derived metric tables, or debug traces unless explicitly requested.

## Execution Gates

Important modules must be executed or explicitly blocked. If a selected valuation model, reverse DCF, data audit, risk check, or report module cannot run, state:

```text
[Module] Blocked: [missing/stale input and impact]
```

Load when needed:

- `references/execution_policy/execution_gate_policy.md`
- `references/valuation_rules/reverse_dcf_execution_policy.md`
- `skills/execution-gate-auditor/SKILL.md`
- `scripts/audit/execution_gate_audit.py`

## Data Rules

Every material number must be sourced, derived from sourced inputs, clearly user-provided, or explicitly labeled as an assumption. Unsourced numbers must not drive the final conclusion.

Load when needed:

- `references/data_source_policy/data_source_policy.md`
- `references/data_source_policy/data_freshness_policy.md`
- `references/data_source_policy/data_provenance_policy.md`
- `scripts/data/check_data_freshness.py`
- `scripts/audit/data_provenance_audit.py`

For current analysis, state analysis date, market data date, latest financial period, and important missing data.

## Investor Action

When the user asks for buy/add/hold/trim/sell guidance, or when a standard stock report is produced, include valuation-based and position-aware action guidance.

Load:

- `skills/investor-action-framework/SKILL.md`
- `references/action_policy/investor_action_framework.md`
- `scripts/scoring/investor_action_framework.py`

Use conditional language: consider, wait for, monitor, add only if, trim if, reassess if. Do not give absolute personalized financial advice.

## Optional Presentation Layers

Default final presentation is pyramid-principle structured output through the fixed renderer.

Load only when needed:

- `skills/pyramid-summary/SKILL.md`
- `references/presentation_policy/pyramid_output_policy.md`
- `skills/mindmap-summary/SKILL.md`
- `references/presentation_policy/mindmap_output_policy.md`
- `scripts/presentation/pyramid_builder.py`
- `scripts/presentation/mindmap_builder.py`

Mind map output is optional and should be used only when requested.

## Platform Compatibility

This repository is dual-use:

- Claude discovers this skill from `SKILL.md` frontmatter and this compact body.
- Codex can use the same `SKILL.md` plus repo/plugin metadata such as `.codex-plugin/plugin.json` and `plugin.json`.
- Claude install/package scripts should exclude Codex-only metadata.
- Codex install scripts should preserve the repo/plugin shape.

## Hard Rules

- Always state assumptions.
- Always flag missing data.
- Always distinguish good business from good price.
- Always include margin of safety for valuation work.
- Always include downside risk.
- Always include price zone assumption basis and conclusion change triggers.
- Never use a single valuation multiple as the whole conclusion.
- Never load all sub-skills or master source materials unless explicitly required.
- Never let optional paid or private data block a normal public-data L1/L2 analysis.
