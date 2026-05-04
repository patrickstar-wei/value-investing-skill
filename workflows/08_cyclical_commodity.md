# Workflow 08: Cyclical / Commodity Producer

## Trigger Conditions

Use for energy, mining, shipping, chemicals, commodity cyclicals, or other businesses where cycle price dominates earnings.

## Models

- Mid-cycle EBITDA / earnings
- Commodity price scenario model
- NAV / reserve value
- EV/EBITDA cross-check
- Downcycle balance-sheet stress

## Required checks

- Cycle position
- Cost curve position
- Balance-sheet durability
- Capital discipline
- Commodity price sensitivity

## Philosophy lenses

Howard Marks, Graham, Greenwald.

## Output rules

Do not annualize peak-cycle profits as normal earnings.

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
