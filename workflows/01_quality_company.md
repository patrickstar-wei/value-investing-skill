# Workflow 01: Quality Company

## Trigger Conditions

Use for mature companies with stable cash flow, durable economics, above-average ROE/ROIC, and identifiable competitive advantage.

## Models

- Owner Earnings DCF / FCFE DCF
- EPV / No-growth EPV
- Quality-adjusted P/E or normalized P/E
- Reverse DCF

## Required checks

- Moat durability
- Reinvestment runway
- Cash-flow conversion
- Capital allocation
- Margin-of-safety

## Philosophy lenses

Buffett/Munger, Greenwald, Graham.

## Output rules

Show classification, business quality, valuation summary, risk, action. Do not show calculation trace.

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
