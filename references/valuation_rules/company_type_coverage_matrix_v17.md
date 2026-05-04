# Company Type Coverage Matrix v17

## Purpose

Expand the skill beyond mature quality compounders while keeping token usage controlled.

The skill should not load every valuation framework. It should first classify the company using compact routing signals, then lazy-load only the selected route and material overlays.

## Default Support Levels

| Support Level | Meaning |
|---|---|
| Direct | v16/v17 can analyze with existing route and compact context. |
| Supported with specialized route | v17 has a route, but only load it when classification triggers it. |
| Limited | Can provide high-level analysis, but valuation confidence should be marked lower unless extra data is provided. |
| Not recommended | Do not force a generic DCF; use a specialist route or block valuation. |

## Core Company Types

| Company Type | Typical Companies | Route | Support |
|---|---|---|---|
| Mature Quality Compounder | Midea, P&G, Coca-Cola, Unilever | Owner Earnings DCF / EPV / Reverse DCF | Direct |
| Dividend / Shareholder Return Compounder | Kimberly-Clark, P&G, Midea | DDM + Shareholder Yield + Dividend Safety | Direct |
| Tech-enabled Mature Quality Compounder | Midea, Schneider, Siemens, Honeywell | Core DCF + Technology Optionality + SOTP if material | Direct |
| Digital Platform Compounder | Alphabet, Meta, Microsoft, Amazon | SOTP + platform cash-flow DCF + AI/cloud optionality | Specialized route |
| Hyperscale Cloud / Digital Infrastructure Platform | AWS, Azure, Google Cloud segments | Segment DCF / EV/EBIT / capex sensitivity | Specialized route |
| AI / Semiconductor Hypergrowth Platform | NVIDIA, AMD, Broadcom, ASML, TSMC | Scenario DCF + TAM penetration + cycle/margin stress | Specialized route |
| Managed Care / Healthcare Services | UnitedHealth, Cigna, Humana, CVS | Normalized EPS + MLR + SOTP + regulatory discount | Specialized route |
| Insurance Float-backed Holding Company | Berkshire Hathaway, Markel, Fairfax | SOTP + look-through earnings + float value + NAV | Specialized route |
| Bank / Financial Institution | JPMorgan, Bank of America | Residual Income / P/B-ROE / CET1 / credit cycle | Specialized route |
| Insurance Underwriter | Chubb, Progressive, AIG | P/B + combined ratio + float/investment income | Specialized route |
| SaaS / Subscription Software Compounder | Salesforce, Adobe, ServiceNow | ARR / NRR / Rule of 40 / FCF margin / EV/Revenue | Specialized route |
| Mature Pharma / Pipeline Pharma | Eli Lilly, Novo Nordisk, Merck | Product cash flows + pipeline rNPV + patent cliff | Specialized route |
| Commodity / Deep Cyclical Producer | Exxon, Chevron, BHP, Rio Tinto | Mid-cycle EBITDA + commodity price scenarios + reserves | Specialized route |
| REIT / Infrastructure Yield Asset | Realty Income, Prologis, AMT | AFFO / NOI / cap rate / leverage / distribution safety | Specialized route |
| Auto / EV / Mobility Platform | Tesla, BYD, Toyota | Manufacturing normalized margin + software optionality + cycle stress | Specialized route |
| Fintech / Brokerage Platform | Robinhood, Interactive Brokers | Revenue build-up / normalized earnings + AUC-user comps + rate/crypto/regulatory stress | Specialized route |

## Token-Efficient Routing Rule

Default analysis must load only:

```text
SKILL.md
+ token efficiency contract
+ classification route
+ selected company-type route
+ at most two material overlays
+ output template
```

Do not load unselected specialist routes.

## Route Activation Examples

- NVIDIA: AI / Semiconductor Hypergrowth Platform.
- Alphabet: Digital Platform Compounder + Cloud / AI Optionality.
- Amazon: Digital Platform Compounder + Cloud + Retail Margin Recovery.
- UnitedHealth: Managed Care / Healthcare Services.
- Robinhood: Fintech / Brokerage Platform.
- Berkshire Hathaway: Insurance Float-backed Holding Company.
- Midea: Tech-enabled Mature Quality Compounder + Shareholder Return + Light Cyclical Manufacturing.
- Kimberly-Clark: Dividend / Shareholder Return Compounder.

## Default User-Facing Rule

Show:

- selected company type
- selected route
- activated models
- deferred models
- confidence
- valuation implication

Do not show:

- full scorecard
- route calculations
- valuation formulas
- detailed model traces
