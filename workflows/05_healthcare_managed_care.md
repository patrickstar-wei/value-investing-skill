# Workflow 05: Managed Care / Healthcare Services

## Trigger Conditions

Use for health insurers, managed care, PBM, healthcare service platforms, and vertically integrated healthcare operators.

## Models

- Normalized EPS / FCFE DCF
- Segment SOTP for service platforms
- P/E band
- Medical Loss Ratio sensitivity
- Regulatory-risk discount

## Required checks

- Medical Loss Ratio trend
- Claims cost inflation
- Medicare / Medicaid / reimbursement policy exposure
- Service segment growth quality
- Regulatory and litigation risk

## Philosophy lenses

Graham, Buffett/Munger, Damodaran, risk-first regulatory discipline.

## Output rules

Do not treat managed care as a generic consumer or industrial company. Regulatory and claims-cost risks must be explicit.

---

## v20.1 Workflow Output Rule

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
