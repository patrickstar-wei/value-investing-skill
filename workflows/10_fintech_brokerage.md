# Workflow 10: Fintech / Brokerage Platform

## Trigger Conditions

Use for fintech platforms, consumer brokerages, trading apps, market-data-driven brokers, crypto trading platforms, and hybrid financial platforms where value is driven by funded customers, assets under custody, transaction activity, net interest income, and regulatory constraints.

## Models

- Revenue build-up DCF / normalized earnings
- EV/Revenue, EV/EBITDA, and AUC / user-based comps
- Net interest income sensitivity
- Rate decline + crypto volume + transaction activity stress
- Reverse DCF / implied ARPU and funded customer growth

## Required checks

- Funded customers and customer growth
- Assets under custody / net deposits
- ARPU by revenue stream
- Options / equities / crypto transaction revenue mix
- Net interest income sensitivity to rate cuts
- SBC and dilution
- Brokerage, payment-for-order-flow, crypto, and consumer-finance regulatory risk
- Liquidity, capital requirements, and counterparty risk where material

## Output rules

Show classification, model stack, customer/AUC economics, rate and volume sensitivity, regulatory downside, valuation range, and action. Do not show calculation trace by default.

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
