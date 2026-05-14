# Specialized Company Routes v17

## Purpose

Provide concise route definitions for companies that do not fit a simple mature quality compounder model.

Each route is loaded only when classification triggers it.

---

## 1. AI / Semiconductor Hypergrowth Platform

Use for companies where value is driven by AI infrastructure demand, semiconductor cycles, high margins, and large future TAM assumptions.

Typical companies: NVIDIA, AMD, Broadcom, ASML, TSMC.

### Required checks

- Data center / AI revenue growth
- Gross margin and operating margin durability
- Customer concentration
- Supply chain and foundry dependency
- Export control / geopolitical risk
- Capex cycle and cloud customer demand
- Tech cycle profile: `physical_inventory`
- Required gates: Financial History Gate, Inventory Cycle Gate, Capacity Cycle Gate

### Model stack

- Primary: Scenario-weighted DCF
- Cross-check: EV/Sales, EV/Gross Profit, EV/EBIT
- Downside: Cycle-normalized earnings and margin stress
- Implied expectation: Reverse DCF / implied TAM penetration

### Token rule

Do not load dividend, banking, insurance, REIT, or mature-consumer frameworks unless explicitly relevant.

---

## 2. Digital Platform Compounder

Use for companies with platform economics, network effects, advertising, cloud, app stores, marketplaces, or ecosystem cash flows.

Typical companies: Alphabet, Amazon, Meta, Microsoft, Apple.

### Required checks

- Core platform cash flow
- Segment economics
- AI capex and monetization
- Cloud or advertising cyclicality
- Regulatory / antitrust risk
- Tech cycle profile: `compute_capacity` when cloud / AI infrastructure dominates; `advertising_demand` when ad demand dominates
- Required gates: Financial History Gate plus Compute Capacity Gate or Advertising Demand Cycle Gate when material

### Model stack

- Primary: Segment SOTP + Owner Earnings DCF
- Cross-check: EV/EBIT, normalized FCF yield, segment multiples
- Downside: regulatory and margin stress case
- Implied expectation: Reverse DCF

### Token rule

Load SOTP and platform route. Defer detailed SaaS, semiconductor, and REIT routes unless a segment is material.

---

## 3. Hyperscale Cloud / Digital Infrastructure Platform

Use when cloud, AI infrastructure, or digital infrastructure is a material valuation driver.

Typical companies or segments: AWS, Azure, Google Cloud.

### Required checks

- Revenue growth
- Operating margin maturity
- Capex intensity
- AI infrastructure demand
- Customer concentration and enterprise retention
- Tech cycle profile: `compute_capacity`
- Required gates: Financial History Gate and Compute Capacity Gate

### Model stack

- Primary: Segment DCF
- Cross-check: EV/EBIT, EV/Sales, peer cloud multiples
- Downside: margin normalization and capex stress
- Implied expectation: implied growth and terminal margin

---

## 4. Managed Care / Healthcare Services Compounder

Use for healthcare insurers and healthcare service platforms.

Typical companies: UnitedHealth, Cigna, Humana, CVS Health.

### Required checks

- Medical Loss Ratio / benefits ratio
- Premium growth and pricing
- Membership growth / mix
- Optum-like services economics
- Regulation, Medicare Advantage, reimbursement, litigation risk

### Model stack

- Primary: Normalized EPS / FCFE DCF
- Cross-check: P/E band, SOTP for service segments
- Downside: MLR stress and regulatory discount
- Implied expectation: implied EPS growth / margin recovery

---

## 5. Insurance Float-backed Holding Company

Use for holding companies whose value is driven by insurance float, operating subsidiaries, and investment portfolios.

Typical companies: Berkshire Hathaway, Markel, Fairfax.

### Required checks

- Insurance underwriting quality
- Cost and durability of float
- Investment portfolio NAV
- Operating subsidiaries earnings
- Cash and capital allocation policy

### Model stack

- Primary: SOTP + look-through earnings
- Cross-check: adjusted book value / NAV
- Downside: underwriting stress and market drawdown
- Implied expectation: implied return on retained capital

---

## 6. Financial Institution: Bank / Insurance / Asset Manager

Use for banks, traditional insurers, brokers, and asset managers.

### Model stack

- Banks: Residual Income, P/B-ROE, CET1, credit cycle stress
- Insurers: P/B, combined ratio, float/investment income, embedded value where applicable
- Asset managers: AUM, fee rate, operating leverage, market beta sensitivity

Do not use standard enterprise DCF as the primary model for regulated financial institutions.

---

## 7. SaaS / Subscription Software Compounder

Use for software firms where recurring revenue and retention drive value.

### Required checks

- ARR / revenue growth
- Net revenue retention
- Gross margin
- Rule of 40
- Sales efficiency
- SBC and true FCF margin
- Tech cycle profile: `subscription_budget`
- Required gates: Financial History Gate and Subscription Budget Cycle Gate

### Model stack

- Primary: Revenue build-up DCF / FCF margin path
- Cross-check: EV/Sales, EV/Gross Profit, Rule of 40
- Downside: growth deceleration and SBC dilution stress
- Implied expectation: reverse DCF

---

## 8. Commodity / Deep Cyclical Producer

Use for resource, energy, shipping, metals, and deep cyclical producers.

### Model stack

- Primary: Mid-cycle EBITDA / commodity scenario model
- Cross-check: EV/EBITDA, NAV, reserve value
- Downside: downcycle balance sheet stress
- Implied expectation: implied commodity price / cycle recovery

---

## 9. REIT / Infrastructure Yield Asset

Use for property REITs, towers, pipelines, and infrastructure yield assets.

### Model stack

- Primary: AFFO / DCF / NOI capitalization
- Cross-check: cap rate, NAV, dividend safety
- Downside: leverage, refinancing, occupancy, rate stress
- Implied expectation: implied cap rate / AFFO growth

---

## 10. Auto / EV / Mobility Platform

Use for auto manufacturers, EV platforms, and mobility companies.

### Model stack

- Primary: Normalized manufacturing earnings + optionality layer
- Cross-check: EV/EBIT, unit economics, battery/software attach rates
- Downside: auto-cycle and price-war stress
- Implied expectation: implied vehicle volume, margin, and software value

---

## 11. Fintech / Brokerage Platform

Use for fintech platforms, consumer brokerages, trading apps, crypto trading platforms, and hybrid financial platforms where value is driven by funded customers, assets under custody, transaction activity, net interest income, and regulatory constraints.

Typical companies: Robinhood, Interactive Brokers, Coinbase-like trading platforms when brokerage / transaction economics dominate.

### Required checks

- Funded customers, retention, net deposits, and assets under custody
- ARPU and revenue mix: options, equities, crypto, subscriptions, net interest income, and other revenue
- Rate-cut sensitivity for net interest income
- Transaction volume and crypto-cycle sensitivity
- SBC, dilution, and share count
- Brokerage, payment-for-order-flow, crypto, consumer protection, and capital / liquidity regulation

### Model stack

- Primary: Revenue build-up DCF / normalized earnings
- Cross-check: EV/Revenue, EV/EBITDA, AUC / funded-customer comps
- Downside: rate decline + crypto volume + regulatory stress
- Implied expectation: Reverse DCF / implied ARPU and funded customer growth

### Token rule

Load fintech / brokerage route and financial risk gates. Defer bank, insurance, REIT, and pure SaaS routes unless those economics dominate.
