# Workflow 06: Holding Company / Insurance Float Allocator

## Trigger Conditions

Use for conglomerates, investment holding companies, insurance-float allocators, or Berkshire-like companies.

## Models

- SOTP
- Look-through earnings
- Investment portfolio NAV
- Insurance float value
- Adjusted book value
- Operating subsidiary earnings multiple

## Required checks

- Float cost and underwriting profitability
- Capital allocation skill
- Cash and investments
- Subsidiary quality
- Holding-company discount

## Philosophy lenses

Buffett/Munger, Graham, Greenwald, capital allocation discipline.

## Output rules

Do not use a single P/E or generic DCF for the whole company when segment economics differ materially.

---

## v18 Workflow Output Rule

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
