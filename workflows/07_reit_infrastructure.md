# Workflow 07: REIT / Infrastructure Yield Asset

## Trigger Conditions

Use for REITs, tower assets, logistics real estate, regulated infrastructure, or income-producing asset platforms.

## Models

- AFFO / FFO yield
- NOI capitalization / cap rate
- NAV
- Distribution safety
- Rate and refinancing stress

## Required checks

- Occupancy and rent growth
- Lease duration
- Debt maturity schedule
- Interest-rate sensitivity
- Distribution coverage

## Philosophy lenses

Graham, Greenwald, Damodaran, rate-cycle discipline.

## Output rules

Do not rely on accounting EPS as the main valuation metric for REITs.

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
