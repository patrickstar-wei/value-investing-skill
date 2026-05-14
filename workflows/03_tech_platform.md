# Workflow 03: Digital / Technology Platform

## Trigger Conditions

Use for digital advertising, cloud, app store, marketplace, software ecosystem, or platform companies with mature cash flow and technology optionality.

## Models

- Segment SOTP
- Owner Earnings DCF
- Cloud / advertising / marketplace segment DCF or multiple sanity check
- Reverse DCF
- AI capex sensitivity where material

## Required checks

- Platform moat and network effects
- Segment economics
- AI disruption or enhancement
- Regulatory risk
- CapEx and FCF impact
- Financial History Gate for all L1+ technology-platform analysis.
- Compute Capacity Gate when cloud, AI infrastructure, or data-center CapEx is a material valuation driver.
- Subscription Budget Cycle Gate for SaaS / subscription software: use deferred revenue, RPO / billings disclosures, retention, sales efficiency, and operating cash flow where available.
- Advertising Demand Cycle Gate for ad-supported platforms: use revenue growth, ARPU / engagement where disclosed, cost structure, and operating leverage; inventory-cycle evidence is not required.

## Philosophy lenses

Buffett/Munger, Fisher, Mauboussin/Rappaport, Damodaran.

## Output rules

Separate core cash-flow engine from technology optionality. Do not automatically assign a tech premium unless monetization evidence exists.

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
