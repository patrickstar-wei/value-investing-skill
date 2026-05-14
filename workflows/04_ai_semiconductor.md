# Workflow 04: AI / Semiconductor Platform

## Trigger Conditions

Use for AI accelerators, semiconductor designers, equipment companies, foundries, data-center AI infrastructure suppliers, or chip-platform businesses.

## Models

- Scenario-weighted DCF
- Reverse DCF / implied TAM penetration
- EV/Sales, EV/Gross Profit, EV/EBIT sanity checks
- Cycle-normalized earnings
- Gross-margin and capex-cycle stress test

## Required checks

- AI demand durability
- Customer concentration
- Supply chain / foundry dependence
- Export control and geopolitical constraints
- Cyclicality and margin normalization
- Financial History Gate: use company filing history to anchor revenue, gross margin, FCF, inventory, CapEx, PP&E, and share-count trends.
- Inventory Cycle Gate: require inventory / revenue or related filing evidence where available; if missing, mark cycle analysis `Limited` and do not treat peak margins as permanent.
- Capacity Cycle Gate: require CapEx, PP&E, depreciation, or external capacity evidence where available; if missing, stress AI-capex monetization assumptions.

## Philosophy lenses

Fisher, Mauboussin/Rappaport, Howard Marks, Damodaran.

## Output rules

Emphasize market-implied expectations and downside if the AI capex cycle normalizes. Do not use DDM or mature-consumer valuation logic.

---

##  Workflow Output Rule

This workflow must not render the final user-facing report directly.

It must return structured analysis fields defined in:

- `references/output_policy/workflow_payload_contract.md`

The final report must be rendered through:

- `references/output_policy/fixed_report_renderer.md`

The final report must preserve:

- Bear / Base / Bull valuation range or blocked status
- price zones
- position-aware suggestions
- tranche plan
- key add / hold / trim / exit conditions

Do not expose valuation calculation trace, routing scorecards, or quality-gate internals by default.
