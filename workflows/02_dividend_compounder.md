# Workflow 02: Dividend / Shareholder Return Compounder

## Trigger Conditions

Use when dividends, buybacks, share cancellation, or debt reduction materially contribute to shareholder return.

## Models

- Two-stage DDM
- Gordon Growth terminal check
- Dividend Yield Band
- Shareholder Yield
- FCFE / Owner Earnings DCF cross-check
- Dividend Safety / Payout Stress Test

## Required checks

- Dividend payout ratio
- Free-cash-flow coverage
- Balance-sheet support
- Dividend growth sustainability
- Buyback quality: value-creating or value-destructive

## Philosophy lenses

Buffett/Munger, Graham, Greenwald.

## Output rules

Show dividend safety, shareholder yield attractiveness, valuation range, margin of safety, and action. Do not present DDM line-by-line calculations.

---

## v17.2 Workflow Output Rule

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
