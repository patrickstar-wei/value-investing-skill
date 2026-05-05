# Context Manifest

This file is a navigation index. The master skill should read this first, then load only the required files.

| Task | Load These Files |
|---|---|
| Quick stock check | `SKILL.md`, `commands/quick-check.md`, `references/context_policy/token_budget_policy.md` |
| Full research | `commands/research.md`, target market file, target industry file, `skills/valuation-router/SKILL.md`, `references/valuation_rules/company_classification_routing_policy.md`, `references/valuation_rules/valuation_model_router.md`, `references/valuation_rules/structured_assumption_policy.md` |
| Owner earnings DCF | `skills/owner-earnings-dcf/SKILL.md`, `references/valuation_rules/structured_assumption_policy.md` |
| Reverse DCF | `skills/reverse-dcf/SKILL.md`, `scripts/valuation/valuation_reverse_dcf.py` |
| Bank valuation | `skills/valuation-router/SKILL.md`, `references/valuation_rules/valuation_model_router.md`, `scripts/valuation/valuation_residual_income.py` |
| Biotech valuation | `skills/rnpv-analysis/SKILL.md`, `scripts/valuation/valuation_rnpv.py` |
| Dividend valuation | `workflows/02_dividend_compounder.md`, `scripts/valuation/valuation_ddm.py` |
| SOTP valuation | `references/valuation_rules/valuation_model_router.md`, `scripts/valuation/valuation_sotp.py` |
| Comparable multiples | `skills/comps-analysis/SKILL.md`, `scripts/valuation/valuation_comps.py` |
| Liquidation valuation | `skills/liquidation-value/SKILL.md`, `scripts/valuation/valuation_liquidation.py` |
| REIT / infrastructure valuation | `workflows/07_reit_infrastructure.md`, `scripts/valuation/valuation_reit.py`, `scripts/valuation/valuation_nav.py` |
| Cyclical valuation | `workflows/08_cyclical_commodity.md`, `scripts/valuation/valuation_cyclical.py` |
| Insurance valuation | `references/valuation_rules/specialized_company_routes_v17.md`, `scripts/valuation/valuation_insurance.py` |
| Scenario-weighted valuation | `references/valuation_rules/structured_assumption_policy.md`, `scripts/valuation/valuation_scenario.py` |
| Fintech / brokerage valuation | `workflows/10_fintech_brokerage.md`, `scripts/valuation/valuation_fintech.py`, `scripts/valuation/valuation_comps.py`, `scripts/valuation/valuation_reverse_dcf.py` |
| Unified valuation execution | `schemas/valuation_input_packet.schema.json`, `scripts/valuation/valuation_input_packet.py`, `scripts/audit/structured_assumption_audit.py`, `scripts/valuation/valuation_executor.py` |
| Risk-only analysis | `skills/risk-analysis/SKILL.md` |
| Report generation | `skills/report-generation/SKILL.md`, selected report template |
| Audit | `skills/model-audit/SKILL.md`, `scripts/audit/*` |


## v17.1 Core Philosophy / Workflow Tasks

| Task | Load These Files |
|---|---|
| Any standard investment analysis | `references/core/investment_philosophy_layer.md`, `references/core/investment_quality_gate.md`, selected workflow only |
| Master lens lookup | `references/masters/multi_master_framework.md`, selected `references/masters/*.md` lens only |
| Jin Jiancheng action lens lookup | `references/masters/multi_master_framework.md`, `references/masters/jin_jiancheng.md` |
| Full master source lookup | selected file under `references/masters/source_materials/` only |
| Workflow routing | `commands/workflow-router.md`, `workflows/00_router.md`, `scripts/routing/select_valuation_models.py` |
| Philosophy / quality gate audit | `commands/philosophy-gate.md`, `references/core/investment_philosophy_layer.md`, `references/core/investment_quality_gate.md` |
| Quality company workflow | `workflows/01_quality_company.md`, `references/core/investment_quality_gate.md` |
| Dividend workflow | `workflows/02_dividend_compounder.md`, `references/valuation_rules/dividend_compounder_valuation_policy.md`, `references/core/investment_quality_gate.md` |
| Tech platform workflow | `workflows/03_tech_platform.md`, selected platform route section only, `references/core/investment_quality_gate.md` |
| AI semiconductor workflow | `workflows/04_ai_semiconductor.md`, selected AI semiconductor route section only, `references/core/investment_quality_gate.md` |
| Healthcare managed care workflow | `workflows/05_healthcare_managed_care.md`, selected healthcare route section only, `references/core/investment_quality_gate.md` |
| Holding company workflow | `workflows/06_holding_company.md`, selected holding company route section only, `references/core/investment_quality_gate.md` |
| REIT / infrastructure workflow | `workflows/07_reit_infrastructure.md`, selected REIT route section only, `references/core/investment_quality_gate.md` |
| Cyclical / commodity workflow | `workflows/08_cyclical_commodity.md`, selected cyclical route section only, `references/core/investment_quality_gate.md` |
| Watchlist / comparison workflow | `workflows/09_watchlist_compare.md`, `references/core/investment_quality_gate.md` |

## Context Loading Rule

Use the smallest useful context packet:

```text
Master Summary → Task Command → Router → One Sub-skill → Data Packet → Report Template
```

## Company Classification / Overlay Routing Tasks

| Task | Load These Files |
|---|---|
| Company classification | `commands/classification.md`, `skills/valuation-router/SKILL.md`, `references/valuation_rules/company_classification_routing_policy.md`, `scripts/routing/select_valuation_models.py` |
| Dividend / shareholder return overlay | `commands/shareholder-return.md`, `references/valuation_rules/dividend_compounder_valuation_policy.md`, `skills/valuation-router/SKILL.md` |
| Technology optionality overlay | `commands/technology-optionality.md`, `references/valuation_rules/technology_optionality_policy.md`, `skills/valuation-router/SKILL.md` |
| Tech-enabled mature quality compounder | `references/valuation_rules/company_classification_routing_policy.md`, `references/valuation_rules/dividend_compounder_valuation_policy.md`, `references/valuation_rules/technology_optionality_policy.md`, `references/valuation_rules/valuation_model_router.md` |

## Data Freshness Tasks

| Task | Load These Files |
|---|---|
| Current valuation | `skills/data-freshness-audit/SKILL.md`, `references/data_source_policy/data_freshness_policy.md`, `references/valuation_rules/structured_assumption_policy.md`, `scripts/data/check_data_freshness.py` |
| Margin of safety calculation | `skills/data-freshness-audit/SKILL.md`, `scripts/data/check_data_freshness.py` |
| Historical trend analysis | `references/data_source_policy/data_freshness_policy.md` |

## Execution Gate Tasks

| Task | Load These Files |
|---|---|
| Gate audit | `skills/execution-gate-auditor/SKILL.md`, `references/execution_policy/execution_gate_policy.md`, `scripts/audit/execution_gate_audit.py` |
| Structured assumption gate | `references/valuation_rules/structured_assumption_policy.md`, `scripts/audit/structured_assumption_audit.py` |
| Failure mode review | `references/execution_policy/known_failure_modes.md` |

## Investor Action Tasks

| Task | Load These Files |
|---|---|
| Position-aware action plan | `skills/investor-action-framework/SKILL.md`, `references/action_policy/investor_action_framework.md`, `scripts/scoring/investor_action_framework.py` |
| Buy / add / trim / sell price zones | `references/action_policy/investor_action_framework.md`, `scripts/scoring/investor_action_framework.py` |

## Data Provenance Tasks

| Task | Load These Files |
|---|---|
| Source verification | `skills/data-provenance-audit/SKILL.md`, `references/data_source_policy/data_provenance_policy.md`, `scripts/audit/data_provenance_audit.py` |
| Data lineage creation | `scripts/data/data_provenance.py`, `schemas/data_point.schema.json` |
| Human verification mode | `references/data_source_policy/data_provenance_policy.md`, `commands/source-check.md` |
| SEC filings and XBRL facts | `scripts/connectors/sec_edgar_connector.py`, `references/data_source_policy/data_source_policy.md` |
| Current quote / market cap | `scripts/connectors/yfinance_connector.py`, `references/data_source_policy/data_source_policy.md` |
| Public IR / earnings release | `scripts/connectors/ir_release_parser.py`, `references/data_source_policy/data_source_policy.md` |
| OpenBB optional provider readiness | `config/openbb_providers.template.json`, `scripts/connectors/openbb_provider_config.py`, `references/data_source_policy/data_source_policy.md` |
| Automatic public data packet | `scripts/connectors/public_data_packet_builder.py`, `references/data_source_policy/data_source_policy.md` |
| Institutional view ingestion | `skills/institutional-view-ingestion/SKILL.md`, `references/data_source_policy/institutional_view_policy.md`, `schemas/institutional_view.schema.json`, `scripts/connectors/institutional_view_parser.py` |

## Cross-Model Consistency Tasks

| Task | Load These Files |
|---|---|
| Cross-model consistency check | `references/runtime_policy/cross_model_consistency_policy.md`, `skills/conformance-tester/SKILL.md`, `scripts/testing/conformance_tests.py` |
| Token efficiency audit | `references/runtime_policy/token_efficiency_contract.md`, `scripts/context/context_budget.py`, `scripts/context/context_router.py` |
| Model adapter planning | `references/runtime_policy/model_adapter_policy.md` |

## Mind Map Output Tasks

| Task | Load These Files |
|---|---|
| Mind map summary | `skills/mindmap-summary/SKILL.md`, `references/presentation_policy/mindmap_output_policy.md`, `scripts/presentation/mindmap_builder.py` |
| Mermaid / tree export | `commands/mindmap.md`, `scripts/presentation/mindmap_builder.py` |

## Pyramid Output Tasks

| Task | Load These Files |
|---|---|
| Pyramid principle summary | `skills/pyramid-summary/SKILL.md`, `references/presentation_policy/pyramid_output_policy.md`, `scripts/presentation/pyramid_builder.py` |
| Symbol-enhanced output | `references/presentation_policy/pyramid_output_policy.md`, `commands/pyramid-summary.md` |


## v17 Specialist Company-Type Routing Tasks

| Task | Load These Files |
|---|---|
| Company type coverage matrix | `commands/company-type-coverage.md`, `references/valuation_rules/company_type_coverage_matrix_v17.md`, `references/valuation_rules/token_efficient_routing_policy_v17.md` |
| Token-efficient broad company query | `commands/token-efficient-analysis.md`, `references/valuation_rules/token_efficient_routing_policy_v17.md`, `scripts/routing/select_valuation_models.py` |
| AI / semiconductor platform | `references/valuation_rules/specialized_company_routes_v17.md`, selected route section only, `scripts/routing/select_valuation_models.py`, `scripts/valuation/valuation_scenario.py`, `scripts/valuation/valuation_reverse_dcf.py` |
| Digital platform / cloud platform | `references/valuation_rules/specialized_company_routes_v17.md`, selected route section only, `scripts/routing/select_valuation_models.py`, `scripts/valuation/valuation_sotp.py`, `scripts/valuation/valuation_scenario.py` |
| Managed care / healthcare services | `references/valuation_rules/specialized_company_routes_v17.md`, selected route section only, `scripts/routing/select_valuation_models.py`, `scripts/valuation/valuation_owner_earnings_dcf.py`, `scripts/valuation/valuation_comps.py` |
| Insurance float-backed holding company | `references/valuation_rules/specialized_company_routes_v17.md`, selected route section only, `scripts/routing/select_valuation_models.py`, `scripts/valuation/valuation_insurance.py`, `scripts/valuation/valuation_sotp.py` |
| Commodity / REIT / SaaS / Auto / Fintech specialist route | `references/valuation_rules/specialized_company_routes_v17.md`, selected route section only, `scripts/routing/select_valuation_models.py`, `scripts/valuation/valuation_cyclical.py`, `scripts/valuation/valuation_reit.py`, `scripts/valuation/valuation_fintech.py`, `scripts/valuation/valuation_scenario.py` |


## v20.1 Output Contract Tasks

For every standard investment analysis final output, obey:

- `references/output_policy/mandatory_output_contract.md`
- `references/output_policy/workflow_payload_contract.md`
- `references/output_policy/fixed_report_renderer.md`
- `references/output_policy/output_validation_rules.md`

These files enforce fixed report order, required valuation range, required price zones, position-aware suggestions, and no calculation-trace leakage.
