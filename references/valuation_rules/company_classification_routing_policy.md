# Company Classification Routing Policy v16

## Purpose

Classify companies by economic profile, not by company name or broad industry label alone.

The routing layer should first identify the **Base Business Type**, then add relevant **Overlay Tags**. The final classification determines the valuation model stack.

```text
Base Business Type
+ Shareholder Return Overlay
+ Technology Optionality Overlay
+ Cyclicality / Risk Overlay
```

## Layer 1: Base Business Type

### Mature Quality Compounder

Classify as **Mature Quality Compounder** if most of the following are true:

- Mature operating history and stable core business
- Stable or moderately positive long-term revenue growth
- Stable earnings quality, not mainly one-off gains
- Above-industry ROE / ROIC over a cycle
- Positive operating cash flow and durable free cash flow conversion
- Competitive advantage from brand, channel, scale, cost, supply chain, customer stickiness, technology-enabled manufacturing, or distribution
- Limited need for external financing to sustain operations
- Not a pure early-stage growth stock, pure commodity cycle stock, financial institution, real estate developer, biotech pipeline company, or distressed asset

Default model stack:

| Role | Model |
|---|---|
| Primary | Owner Earnings DCF / FCFE DCF |
| Cross-check | EPV / Quality-adjusted P/E / Normalized P/E |
| Downside | No-growth EPV |
| Implied expectation | Reverse DCF |

## Layer 2: Shareholder Return Overlay

Add **Dividend / Shareholder Return Overlay** if most of the following are true:

- Continuous or credible dividend history
- Management explicitly prioritizes shareholder return
- Dividend payout is reasonable relative to normalized earnings
- Dividend is covered by FCF / FCFE / owner earnings
- Buybacks, share cancellation, or debt reduction materially affect total shareholder yield
- Balance sheet can support payout and reinvestment needs

Additional model stack:

| Role | Model |
|---|---|
| Dividend valuation | Two-stage DDM |
| Stable terminal check | Gordon Growth Model |
| Yield anchor | Dividend Yield Band |
| Shareholder return check | Dividend Yield + Net Buyback Yield + Debt Reduction Yield |
| Safety check | Dividend Safety / Payout Stress Test |
| Implied expectation | Implied Dividend Growth |

## Layer 3: Technology Optionality Overlay

Technology exposure should not automatically reclassify a mature company as a pure technology growth stock.

Add **Technology Optionality Overlay** if the company has technology-related business that is financially visible, commercially monetized, and potentially material.

### Three technology treatments

1. **Core efficiency enabler**
   - Examples: automation, AI quality control, supply-chain digitization, smart manufacturing, industrial internet.
   - Treatment: do not value separately; reflect through margin durability, FCF conversion, ROIC, and moat quality.

2. **Separable monetized segment**
   - Examples: robotics, industrial automation, energy technology, smart building systems, industrial software, medical technology equipment.
   - Treatment: use SOTP or scenario-weighted optionality only if the segment has revenue, growth, customers, margin path, and materiality.

3. **Narrative-only optionality**
   - Examples: strategic labels with no disclosed revenue, no customers, no profitability path, or immaterial financial contribution.
   - Treatment: no separate valuation premium; mention only as optional upside with low confidence.

Additional model stack:

| Evidence Level | Valuation Treatment |
|---|---|
| Efficiency-only | Reflect in core DCF / EPV assumptions |
| Separable + material | SOTP / comparable multiple / scenario-weighted optionality |
| Emerging but not material | Small optionality note, no core valuation driver |
| Narrative-only | No separate valuation premium |

## Layer 4: Cyclicality / Risk Overlay

Add **Light Cyclical Manufacturing Overlay** if the company is materially exposed to:

- Real estate cycle
- Consumer cycle
- Raw material prices
- Export demand
- FX fluctuations
- Channel inventory cycle
- Manufacturing capex cycle

Additional model stack:

| Role | Model / Check |
|---|---|
| Earnings normalization | Mid-cycle earnings |
| Margin normalization | Normalized margin |
| Downside | Stress-case FCF / No-growth EPV |
| Cross-check | Normalized EV/EBIT / EV/EBITDA |

## Internal Scorecard

The router may use 0 / 1 / 2 scoring for each dimension. Default thresholds:

### Mature Quality Compounder Score

- Stable revenue and earnings
- Strong ROE / ROIC
- Durable FCF conversion
- Competitive advantage
- Mature but positive growth

If score >= 7, classify as Mature Quality Compounder.

### Dividend / Shareholder Return Score

- Stable dividend history
- Reasonable payout ratio
- Dividend covered by FCF / FCFE
- Buyback, share cancellation, or debt reduction
- Balance sheet supports payout

If score >= 6, add Dividend / Shareholder Return Overlay.

### Technology Optionality Score

- Technology-related segment exists
- Segment revenue is disclosed
- Segment growth is above core business
- Segment has profit or credible margin path
- Technology can improve ROIC, margins, or TAM

If score >= 6, add Technology Optionality Overlay.

If score <= 3, treat as narrative only and do not assign separate valuation premium.

### Cyclicality Score

- Real estate / consumption cycle exposure
- Raw material exposure
- FX / export exposure
- Inventory or manufacturing cycle exposure

If score >= 4, add Light Cyclical Manufacturing Overlay.

## User-facing output rule

Default reports must not show the internal scorecard or score-by-score calculation. They should show:

- Base Type
- Overlay Tags
- Selected valuation model stack
- Missing evidence / blocked overlays
- Classification confidence
- Investment implication
