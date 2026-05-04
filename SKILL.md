# Value Investing Core Skill v18

## Purpose

Perform value-oriented investment research through a lightweight core skill, lazy-loaded workflows, multi-master investment philosophy, valuation model routing, data confidence checks, model audit, and margin-of-safety discipline.

## Token Discipline

This skill must not load all references, formulas, examples, or sub-skills by default.

Use:

```text
Master Summary → Task Command → Router → One Sub-skill → Data Packet → Report Template
```

Read first:

- `references/context_policy/token_budget_policy.md`
- `references/context_policy/context_manifest.md`



## v17.1 Core Philosophy and Workflow Architecture

The Core Skill must not become a monolithic library of every industry model. It acts as the investment-quality gatekeeper and workflow controller.

Default structure:

```text
Core Skill = investment philosophy + quality gate + output discipline + routing control
Workflow = domain-specific analysis process
Router = low-cost selection mechanism
```

Always load or obey these core policies before final output:

- `references/core/investment_philosophy_layer.md`
- `references/core/investment_quality_gate.md`
- `references/core/modular_workflow_architecture.md`

## v18 Mandatory Output Contract and Renderer

All workflows must use a fixed output contract. The workflow may perform specialized analysis, but it must not directly render the final report. It must return a structured payload to the core report renderer.

Always obey these output policies before final output:

- `references/output_policy/mandatory_output_contract.md`
- `references/output_policy/workflow_payload_contract.md`
- `references/output_policy/fixed_report_renderer.md`
- `references/output_policy/output_validation_rules.md`

The final report must preserve the following fields unless explicitly irrelevant or data-blocked:

- reasonable intrinsic value range: Bear / Base / Bull
- current price
- margin of safety
- valuation status
- price zones: Deep Value, Accumulation, Watchlist, Fair Value, Trim, Sell / Avoid
- position-aware suggestions for Empty Position, Half Position, Full Position, and Overweight Position investors
- tranche plan: starter, add, strong-add, hold, trim, exit-review ranges
- thesis conditions: add only if, hold only if, trim if, exit or avoid if

If valuation data is missing, do not omit the Valuation Summary or Investor Action Framework. Mark those fields as `Blocked`, explain the missing inputs, and provide non-price-based next steps.


The Core Skill must enforce these non-overridable principles:

1. Business quality before valuation.
2. Cash-flow reality over accounting appearance.
3. Valuation model must match company type.
4. Margin of safety is required.
5. Evidence must support every investment conclusion.
6. Bear-case discipline is mandatory.
7. Calculation trace is internal by default.
8. Data confidence gates the action.

For L0/L1 analysis, activate one primary workflow and no more than two auxiliary workflows. Defer all non-material workflows.

## v17.1 Modular Workflows

Use the lightweight router to select workflows instead of expanding every specialist route inside the main prompt.

Primary workflows:

- `workflows/00_router.md`
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

The final report must remain consistent across workflows: pyramid structure, valuation summary only, explicit risk checks, margin-of-safety judgment, investor action framework, and fixed price/action zones. The report must not drop reasonable valuation range, position-aware suggestions, or build/trim/sell ranges.

## Trigger Conditions

Use this skill when the user asks to:

- Analyze a stock, company, industry, or investment opportunity
- Estimate intrinsic value
- Build or audit a valuation model
- Generate an investment memo
- Review earnings
- Assess risk or margin of safety
- Track a thesis or catalyst

## Workflow

1. Classify user task and required depth: L0/L1/L2/L3/L4.
2. Use `scripts/context/context_router.py` to select the smallest useful context packet.
3. Identify target, market, industry, and lifecycle.
4. Route to the relevant value-investing style.
5. Classify the company through the company classification router:
   - Base Business Type
   - Shareholder Return Overlay
   - Technology Optionality Overlay
   - Cyclicality / Risk Overlay
6. Route to valuation models:
   - Primary
   - Cross-check
   - Downside
   - Implied expectation
   - Overlay-specific models, if triggered
7. Convert material model inputs into structured assumptions and constrain them with history, industry economics, management guidance, peer data, reverse DCF, and sensitivity checks.
8. Fetch only required data fields.
9. Use `schemas/valuation_input_packet.schema.json` to bind model inputs to data IDs, source metadata, freshness dates, and structured assumptions when executing valuation.
10. Run scripts for calculations instead of expanding formulas in prompt. Prefer `scripts/valuation/valuation_executor.py` for routed model execution.
11. Audit assumptions, formulas, data lineage, and sensitivity internally.
12. Generate output at the requested depth only.
13. Do not expose valuation model calculation process in the user-facing analysis unless the user explicitly asks for model audit, formulas, workbook-style detail, or debug output.





## v17 Multi-Company-Type Coverage Rule

The skill now supports broader company coverage without loading all valuation frameworks at once.

Default runtime pattern:

```text
Compact classification → selected company-type route → at most two material overlays → concise pyramid output
```

Do not load every route or explain every model. The router must first determine the company type, then lazy-load only the selected route.

### Supported Specialist Routes

Load `references/valuation_rules/company_type_coverage_matrix_v17.md` only when the user asks about coverage or when classification is uncertain.

Load `references/valuation_rules/specialized_company_routes_v17.md` only when the selected company type is outside the mature quality compounder family.

Specialist route families include:

- AI / Semiconductor Hypergrowth Platform
- Digital Platform Compounder
- Hyperscale Cloud / Digital Infrastructure Platform
- Managed Care / Healthcare Services Compounder
- Insurance Float-backed Holding Company
- Financial Institution: Bank / Insurance / Asset Manager
- SaaS / Subscription Software Compounder
- Mature Pharma / Pipeline Pharma
- Commodity / Deep Cyclical Producer
- REIT / Infrastructure Yield Asset
- Auto / EV / Mobility Platform
- Fintech / Brokerage Platform

### Token-Control Rule

For L0/L1 analysis, activate by default:

- one base route
- one primary model
- one or two cross-check models
- one downside model
- one implied-expectation model
- no more than two overlays unless the user asks for a full memo

All other potentially relevant models should be listed as deferred modules rather than expanded.

Load:

- `references/valuation_rules/token_efficient_routing_policy_v17.md`
- `references/valuation_rules/structured_assumption_policy.md`
- `references/runtime_policy/token_efficiency_contract.md`
- `scripts/routing/select_valuation_models.py`

## Company Classification Routing Rule

The skill must not classify a company by name alone. For v17, it must also avoid loading every possible company-type route by default. It should classify the target through a layered routing structure:

```text
Base Business Type
+ Shareholder Return Overlay
+ Technology Optionality Overlay
+ Cyclicality / Risk Overlay
```

Load when a current stock or company analysis requires valuation model selection:

- `references/valuation_rules/company_classification_routing_policy.md`
- `references/valuation_rules/dividend_compounder_valuation_policy.md`
- `references/valuation_rules/technology_optionality_policy.md`
- `skills/valuation-router/SKILL.md`
- `scripts/routing/select_valuation_models.py`

### Base Type: Mature Quality Compounder

Classify as **Mature Quality Compounder** when the company has most of the following:

- Mature operating history and stable industry position
- Stable or moderately positive long-term revenue and earnings growth
- Strong or above-industry ROE / ROIC
- Durable operating cash flow and free cash flow conversion
- A competitive advantage from brand, channel, scale, cost, supply chain, customer stickiness, or manufacturing capability
- Limited dependence on external financing to sustain operations

### Overlay: Dividend / Shareholder Return

Add **Dividend / Shareholder Return Overlay** when dividends, buybacks, or share cancellation materially contribute to shareholder return and are supported by cash flow and balance sheet strength.

Trigger additional checks:

- Two-stage DDM
- Gordon Growth terminal check
- Dividend Yield Band
- Shareholder Yield
- Dividend Safety / payout stress test

### Overlay: Technology Optionality

Add **Technology Optionality Overlay** only when technology-related businesses are financially visible, commercially monetized, and potentially material.

Technology treatment must be conservative:

1. If technology improves the core business, reflect it through margin, ROIC, cash-flow quality, and moat durability.
2. If technology is a separable and material business segment, use SOTP or scenario-weighted optionality.
3. If technology is only narrative without revenue, profit path, customers, or segment evidence, do not assign a separate valuation premium.

### Overlay: Light Cyclical Manufacturing

Add **Light Cyclical Manufacturing Overlay** when the company is exposed to real estate, consumption, raw materials, export demand, FX, channel inventory, or manufacturing capex cycles.

Trigger additional checks:

- Mid-cycle earnings
- Normalized margin
- Stress-case FCF
- No-growth EPV

### Final Classification Format

Use a combined classification instead of a single label, for example:

```text
Tech-enabled Mature Quality Compounder
+ Dividend / Shareholder Return Overlay
+ Light Cyclical Manufacturing Overlay
```

The internal scorecard may be used to classify the company, but default user-facing output should show only the classification result, model stack, missing data, confidence level, and deferred modules. Do not expose score-by-score internals unless explicitly requested.

## User-Facing Valuation Output Rule

The default user-facing valuation output must include model selection and valuation conclusions, not calculation trace. For normal stock/company analysis it must include:

- Bear / Base / Bull intrinsic value range, or explicit blocked status
- Current price, or explicit blocked status
- Margin of safety, or explicit blocked status
- Valuation status: undervalued / fair / expensive / low-confidence / blocked
- Key assumptions and sensitivity summary
- Price zones and position-aware action guidance

Do not show formulas, discounting schedules, model input tables, or internal scorecards unless explicitly requested.

The skill should know how to calculate valuation internally, but the default report must not show the step-by-step valuation model calculation process.

Default user-facing valuation output should include only:

- Valuation method selected
- Bear / base / bull intrinsic value range
- Current price vs. value range
- Margin of safety / overvaluation judgment
- Key assumptions that drive the conclusion
- Sensitivity summary in plain language
- Whether the valuation result is usable, blocked, or low-confidence

Do not include by default:

- Full formulas
- Spreadsheet-style calculation steps
- Line-by-line DCF / EPV / NAV / residual-income computation
- Intermediate discounting schedules
- Formula derivations
- Model input source tables in the main report
- Derived metric tables in the main report

Keep formula audit, source tracing, derived metric tables, valuation run manifests, and calculation logs internal unless the user explicitly asks for calculation process, model audit, assumptions table, source table, appendix, debug, or spreadsheet-style model.

If required for trust, summarize calculation transparency in one sentence: valuation was calculated internally using the selected model; the report shows the range and sensitivity summary rather than the full calculation trace.

## Output Depth

| Level | Use Case | Default Output |
|---|---|---|
| L0 | Quick check | Short judgment |
| L1 | Standard report | Concise report |
| L2 | Full memo | Detailed memo |
| L3 | Committee pack | Files / slides |
| L4 | Audit package | Model + audit logs |

## Data Freshness Rule

Current investment analysis must reflect the current situation, not a stale historical snapshot.

Before any current valuation, margin of safety, or investment rating:

1. State the analysis as-of date.
2. Check market data freshness.
3. Check latest financial statement period.
4. Check latest filing / earnings release / guidance.
5. Run `skills/data-freshness-audit/SKILL.md` when data age is uncertain.
6. If key data is stale or missing, label the output as historical analysis only.

Load:

- `references/data_source_policy/data_freshness_policy.md`
- `scripts/data/check_data_freshness.py`

## Reverse DCF Execution Gate

If the valuation model router selects Reverse DCF as the implied-expectation model, the report must not stop at “Reverse DCF should be run.”

It must include either:

```text
Reverse DCF Result
```

or

```text
Reverse DCF Blocked
```

with missing or stale inputs listed.

Load:

- `references/valuation_rules/reverse_dcf_execution_policy.md`
- `skills/reverse-dcf/SKILL.md`

## Execution Gate Rule

Important analysis steps must be executed or explicitly blocked.

If the workflow selects a valuation model, data audit, risk check, or report module, the final report must include one of:

```text
[Module] Result
```

or:

```text
[Module] Blocked
```

with missing/stale inputs and impact on conclusion.

Load:

- `references/execution_policy/execution_gate_policy.md`
- `skills/execution-gate-auditor/SKILL.md`
- `scripts/audit/execution_gate_audit.py`

The final report must include an Execution Gate Checklist before the final investment view.

## Investor Action Framework Rule

After a complete stock analysis, if the user asks for investor guidance, entry price, add price, trim price, or sell range, load:

- `skills/investor-action-framework/SKILL.md`
- `references/action_policy/investor_action_framework.md`
- `scripts/scoring/investor_action_framework.py`

The output must be conditional and position-aware:

- Empty position investor
- Half position investor
- Full position investor
- Overweight investor

Do not give absolute personalized financial advice. Use valuation-based price zones and state assumptions.

## Data Provenance Rule

Every number used for valuation, fundamental analysis, scoring, risk analysis, or investor action guidance must be traceable.

No orphan numbers are allowed.

Load:

- `references/data_source_policy/data_provenance_policy.md`
- `skills/data-provenance-audit/SKILL.md`
- `scripts/data/data_provenance.py`
- `scripts/audit/data_provenance_audit.py`

If a critical number has no source URL, local path, formula, or input data IDs, block the valuation or label it as an assumption that cannot drive the final conclusion.

## Cross-Model Consistency and Token Efficiency Rule

This Skill cannot guarantee identical prose across different AI systems, but it must enforce comparable process and outputs.

Load when needed:

- `references/runtime_policy/cross_model_consistency_policy.md`
- `references/runtime_policy/token_efficiency_contract.md`
- `references/runtime_policy/model_adapter_policy.md`
- `skills/conformance-tester/SKILL.md`
- `scripts/testing/conformance_tests.py`

Every full analysis should produce or be able to produce:

- Valuation run manifest
- Selected context files
- Data lineage file
- Execution gate checklist
- Source annotation table
- Output schema compliance result

If the runtime has limited context or tools, use the model adapter fallback and block unsupported calculations rather than silently skipping them.

## Mind Map Output Rule

When a standard stock analysis is completed, the output should support a mind-map-friendly summary layer.

Load:

- `skills/mindmap-summary/SKILL.md`
- `references/presentation_policy/mindmap_output_policy.md`
- `scripts/presentation/mindmap_builder.py`

The default final answer should preferably include:

1. A compact mind map summary
2. The detailed report below it or after it

Supported formats:

- Nested bullet format
- ASCII tree
- Mermaid mindmap (optional)

The mind map must summarize, not invent. Blocked modules must appear as blocked nodes.

## Pyramid Principle Output Rule

The default final presentation style is pyramid-principle structured output, not mind map.

Load:

- `skills/pyramid-summary/SKILL.md`
- `references/presentation_policy/pyramid_output_policy.md`
- `scripts/presentation/pyramid_builder.py`

Default output order:

1. 📌 Executive Conclusion
2. 🧭 Decision Snapshot
3. 🔹 Core Thesis
4. 📊 Key Evidence
5. 🧮 Valuation Summary
6. ⚠️ Risks
7. ✅ / ❌ Execution Gate Checklist
8. 🧭 Investor Action Framework
9. 🔍 Data Provenance

Use symbols consistently:

- ✅ supportive / passed
- ❌ negative / failed
- ⚠️ risk / uncertainty
- ➡️ action / implication
- 📌 key conclusion
- 🔹 main point
- 🔸 detail
- 💡 interpretation
- 🧮 valuation summary
- 📊 data
- 🔍 source
- 🧭 action

Mind map output is optional and should only be used when explicitly requested.

## Hard Rules

- Always state assumptions.
- Always flag missing data.
- Always distinguish good business from good price.
- Always include margin of safety.
- Always include downside risk.
- Never use a single valuation multiple as the entire conclusion.
- Never load all sub-skills unless explicitly required.


## v17 Coverage Examples

Use compact classification first:

| Company | Likely Route | Default Treatment |
|---|---|---|
| NVIDIA | AI / Semiconductor Hypergrowth Platform | Scenario DCF + TAM penetration + cycle stress; defer dividend models |
| Alphabet | Digital Platform Compounder | SOTP + platform DCF + cloud/AI optionality |
| Amazon | Digital Platform Compounder + Cloud Platform Overlay | SOTP + AWS segment valuation + retail margin recovery |
| UnitedHealth | Managed Care / Healthcare Services Compounder | Normalized EPS / FCFE + MLR and regulatory sensitivity |
| Berkshire Hathaway | Insurance Float-backed Holding Company | SOTP + look-through earnings + float value + investment NAV |
| Midea | Tech-enabled Mature Quality Compounder | Owner Earnings DCF + shareholder return + technology optionality |
| Kimberly-Clark | Dividend / Shareholder Return Compounder | DDM + dividend safety + shareholder yield |

Do not perform full valuation for all companies in a coverage query. Return only type, route, support level, and deferred modules unless the user asks for a specific company analysis.
