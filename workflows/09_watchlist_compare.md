# Workflow 09: Watchlist / Comparison

## Trigger Conditions

Use for peer comparisons, stock pool screening, watchlist creation, ranking, or allocation prioritization.

## Models

Use compact model stacks per company type. Do not run full valuation for every company by default.

## Required checks

- Business quality
- Valuation attractiveness
- Margin of safety
- Data confidence
- Thesis-breaking risks

## Philosophy lenses

Greenblatt, Buffett/Munger, Graham.

## Output rules

Provide ranking and next-action buckets: Buy candidate, Watch, Deep Dive, Avoid. Use compact evidence; defer full single-company memos unless requested.

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
