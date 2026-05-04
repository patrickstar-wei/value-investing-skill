# Structured Assumption Policy

## Purpose

Convert valuation assumptions from vague narrative judgments into auditable, calculator-ready inputs.

The goal is not to make assumptions look certain. The goal is to make them evidence-constrained, internally consistent, and easy to stress test.

Use this policy whenever a valuation model depends on forecast growth, margins, reinvestment, discount rates, terminal growth, segment multiples, probability weights, liquidation discounts, or normalized earnings.

---

## Core Rule

Every material valuation assumption should be stated as:

```json
{
  "assumption": "string",
  "value": "number/string",
  "unit": "percent / currency / multiple / years / probability",
  "scenario": "bear / base / bull / single",
  "evidence": ["historical data", "industry constraint", "management guidance", "peer data", "reverse DCF check"],
  "confidence": "high / medium / low",
  "sensitivity": "high / medium / low",
  "source_or_reason": "string"
}
```

Do not use unsupported phrases such as "growth should be good", "reasonable multiple", or "conservative discount rate" as model inputs unless they are converted into explicit numeric assumptions.

---

## Evidence Hierarchy

Prefer assumptions constrained by multiple evidence types:

1. Historical company range, preferably 5-10 years.
2. Normalized or mid-cycle values instead of one-year peaks or troughs.
3. Industry economics and lifecycle limits.
4. Management guidance, usually haircut in the base case.
5. Peer data, adjusted for growth, margins, ROIC, leverage, and quality.
6. Reverse DCF reasonableness check.
7. Sensitivity analysis and bear-case breakpoints.

If only one evidence type is available, mark assumption confidence as medium or low.

---

## Required Normalization Checks

Before using a reported number as a forward assumption, check whether it needs normalization:

| Input | Normalization Question |
|---|---|
| Revenue growth | Is the latest year boosted by price, stimulus, acquisition, backlog, FX, or cycle recovery? |
| Margin | Is current margin above or below the 5-10 year range? |
| EBIT / EBITDA / EPS | Is the current year a cyclical high, trough, or one-off event year? |
| Free cash flow | Is working capital temporarily favorable or unfavorable? |
| Capex | Does reported capex include expansion growth capex versus maintenance capex? |
| Tax rate | Is the latest rate affected by one-time credits or jurisdiction mix? |
| Share count | Does dilution, SBC, convertibles, or buyback cancellation change per-share value? |
| Net debt | Are lease liabilities, restricted cash, minority interest, or financial subsidiaries material? |

When normalization is material, the valuation payload should show both reported and normalized inputs or list the model as low confidence.

---

## Internal Consistency Checks

The following combinations require explicit support:

- High revenue growth plus rising margins plus falling reinvestment.
- Low discount rate plus high operating volatility.
- High terminal growth plus mature industry.
- High FCF margin plus high working-capital intensity.
- Premium multiple plus below-peer growth or ROIC.
- SOTP premium plus weak or missing segment disclosure.
- rNPV success probability above stage-appropriate norms.
- Liquidation value near book value for assets with weak marketability.

If a valuation relies on one of these combinations without evidence, downgrade assumption confidence and widen the valuation range.

---

## Model-Specific Minimum Assumptions

### DCF / FCFE / Owner Earnings

- Base FCF or owner earnings.
- Forecast growth rate or explicit forecast drivers.
- Discount rate.
- Terminal growth.
- Net debt or equity bridge.
- Shares outstanding / dilution.
- Maintenance capex and working-capital treatment when using owner earnings.

### Reverse DCF

- Current market capitalization or share price and shares.
- Net debt.
- Base FCF or revenue and target FCF margin.
- Forecast period.
- Discount rate.
- Terminal growth.

### DDM

- Current dividend per share.
- Payout ratio and FCFE coverage.
- Dividend growth path.
- Cost of equity.
- Terminal growth or terminal payout assumption.

### EPV

- Normalized EBIT or NOPAT.
- Tax rate.
- WACC or cost of capital.
- Net debt.
- Shares outstanding.
- Reason for no-growth or steady-state treatment.

### SOTP / NAV

- Segment revenue, EBIT, EBITDA, FCF, assets, or NAV.
- Segment-specific multiple, cap rate, or discount rate.
- Corporate costs.
- Net debt, minority interests, and holding-company discount if applicable.
- Evidence that segment economics differ enough to justify SOTP.

### rNPV

- Pipeline asset or product list.
- Development stage.
- Probability of technical and regulatory success.
- Launch timing.
- Peak sales.
- Margin / royalty / cost assumptions.
- Patent or exclusivity duration.
- Discount rate.

### Liquidation Value

- Cash and equivalents.
- Receivables, inventory, PP&E, investments, intangibles, and other assets.
- Asset-specific recovery rates.
- Debt, leases, working-capital obligations, and senior claims.
- Liquidation costs and timing.

### Comps / Multiples

- Peer set.
- Metric definition and currency.
- Growth, margin, ROIC, leverage, and accounting comparability.
- Multiple selection rule: median, trimmed median, quality-adjusted, or scenario range.

---

## Scenario Discipline

Use Bear / Base / Bull assumptions for normal valuation work:

| Scenario | Meaning |
|---|---|
| Bear | Plausible adverse case, not disaster fantasy. |
| Base | Evidence-weighted conservative central case. |
| Bull | Upside case that still respects industry and reinvestment constraints. |

The bull case should not combine every favorable assumption unless the business has evidence for that operating leverage and reinvestment profile.

---

## Output Requirement

Final reports should not show full calculation traces by default, but they should include:

- Key assumptions.
- Assumption confidence.
- Sensitivity summary.
- Blocked or low-confidence assumptions.
- What evidence would improve confidence.

If critical assumptions are missing, mark valuation as `Blocked` or `Low-confidence`; do not silently substitute arbitrary values.
