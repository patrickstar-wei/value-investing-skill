# Valuation Model Router v16

## Four-Model Structure

| Role | Meaning |
|---|---|
| Primary Model | Main model for intrinsic value |
| Cross-check Model | Sanity check through a different method |
| Downside Model | Protect against permanent capital loss |
| Implied Expectation Model | Reverse engineer market expectations |

## v16 Routing Principle

The router must not classify a company by name alone. It should first determine a base business type, then add overlay tags that change or supplement the valuation model stack.

```text
Base Business Type
+ Shareholder Return Overlay
+ Technology Optionality Overlay
+ Cyclicality / Risk Overlay
```

Default user-facing reports must show selected models and judgment only. They must not show internal scorecards or line-by-line valuation calculations unless explicitly requested.

## Base Type Routing Table

| Base Company Type | Primary | Cross-check | Downside | Implied |
|---|---|---|---|---|
| Quality compounder | Owner Earnings DCF | EPV / Quality P/E | No-growth EPV | Reverse DCF |
| Mature Quality Compounder | Owner Earnings DCF / FCFE DCF | EPV / Quality-adjusted P/E / Normalized P/E | No-growth EPV | Reverse DCF |
| Tech-enabled Mature Quality Compounder | Owner Earnings DCF / FCFE DCF | EPV / Normalized P/E / SOTP if material | No-growth EPV + Stress FCF | Reverse DCF |
| Bank | Residual Income / P/B-ROE | P/E / DDM | Tangible Book | Implied ROE |
| Insurance | Embedded Value | P/EV / DDM | Adjusted Book | Implied VNB Growth |
| Real estate / REIT | NAV / Cap Rate | P/FFO / P/B | Liquidation NAV | Implied Cap Rate |
| Biotech | rNPV | Pipeline SOTP | Net Cash / Cash Burn | Implied Approval Probability |
| Cyclical | Mid-cycle Valuation | Normalized EV/EBITDA | Downcycle Earnings | Implied Cycle Recovery |
| Distressed | Liquidation Value | SOTP / NAV | Net Cash Recovery | Expected Value |
| SaaS / software growth | Revenue Build-up DCF | EV/Revenue / Rule of 40 | Unit Economics Stress | Reverse DCF |

## Overlay Model Additions

### Dividend / Shareholder Return Overlay

Add when dividends, buybacks, share cancellation, or debt reduction are material and sustainable.

| Role | Add-on Model / Check |
|---|---|
| Dividend valuation | Two-stage DDM |
| Stable terminal check | Gordon Growth Model |
| Yield anchor | Dividend Yield Band |
| Shareholder return check | Dividend Yield + Net Buyback Yield + Debt Reduction Yield |
| Downside safety | Dividend Safety / Payout Stress Test |
| Implied expectation | Implied Dividend Growth |

DDM is allowed as a major valuation input only when dividends are covered by FCFE / owner earnings and the payout ratio is sustainable. If not, DDM becomes a risk flag.

### Technology Optionality Overlay

Add when technology-related business is financially visible, commercially monetized, and potentially material.

| Evidence Level | Treatment |
|---|---|
| Technology improves core operations only | Reflect in margin, ROIC, FCF conversion, moat quality |
| Separable segment with revenue / customers / margin path | SOTP / comparable multiple cross-check / scenario optionality |
| Emerging but not material | Low-weight scenario optionality |
| Narrative only | No separate valuation premium |

Technology exposure alone must not reclassify a mature company as a pure technology growth stock.

### Light Cyclical Manufacturing Overlay

Add when the company is exposed to real estate, consumption, raw materials, export demand, FX, channel inventory, or manufacturing capex cycles.

| Role | Add-on Model / Check |
|---|---|
| Earnings normalization | Mid-cycle earnings |
| Margin normalization | Normalized margin |
| Downside | Stress-case FCF / No-growth EPV |
| Cross-check | Normalized EV/EBIT / EV/EBITDA |

## Example Route

A company with mature consumer manufacturing cash flows, high dividend payout, buybacks, visible robotics / industrial technology business, and exposure to raw materials or FX should route as:

```text
Tech-enabled Mature Quality Compounder
+ Dividend / Shareholder Return Overlay
+ Technology Optionality Overlay
+ Light Cyclical Manufacturing Overlay
```

Selected model stack:

| Role | Model |
|---|---|
| Base value | Owner Earnings DCF / FCFE DCF |
| Quality cross-check | EPV / Quality-adjusted P/E |
| Dividend value | Two-stage DDM + Dividend Yield Band |
| Shareholder return | Dividend Yield + Net Buyback Yield |
| Technology optionality | SOTP or scenario-weighted optionality if evidence supports it |
| Downside | No-growth EPV + Dividend Safety + Stress FCF |
| Market expectation | Reverse DCF + Implied Dividend Growth |

## Default Output Contract

The valuation router returns:

- Base Type
- Overlay Tags
- Selected primary, cross-check, downside, and implied-expectation models
- Add-on models from overlays
- Missing data / blocked models
- Confidence level

The router does not return:

- Full formulas
- Internal score-by-score logic
- Line-by-line calculations
- Discounting schedules

## Python Implementation Map

The router may select valuation methods conceptually, but executable calculations should load the smallest matching Python module set:

| Method Family | Implementation File |
|---|---|
| Shared result envelope / structured assumptions | `scripts/valuation/valuation_common.py` |
| Owner Earnings DCF / FCFE-style cash flow DCF | `scripts/valuation/valuation_owner_earnings_dcf.py` |
| Reverse DCF | `scripts/valuation/valuation_reverse_dcf.py` |
| EPV / No-growth EPV | `scripts/valuation/valuation_epv.py` |
| Residual Income / P/B-ROE support | `scripts/valuation/valuation_residual_income.py` |
| NAV | `scripts/valuation/valuation_nav.py` |
| DDM / Gordon Growth / dividend yield band | `scripts/valuation/valuation_ddm.py` |
| SOTP | `scripts/valuation/valuation_sotp.py` |
| Comparable multiples | `scripts/valuation/valuation_comps.py` |
| Liquidation value | `scripts/valuation/valuation_liquidation.py` |
| rNPV | `scripts/valuation/valuation_rnpv.py` |
| REIT / NOI cap rate / AFFO | `scripts/valuation/valuation_reit.py` |
| Cyclical / mid-cycle valuation | `scripts/valuation/valuation_cyclical.py` |
| Insurance / embedded-value support | `scripts/valuation/valuation_insurance.py` |
| Scenario-weighted DCF / optionality | `scripts/valuation/valuation_scenario.py` |
| Fintech / brokerage platform economics | `scripts/valuation/valuation_fintech.py` |

Python modules handle deterministic calculation, validation, per-share conversion, and blocked/low-confidence output packaging. They do not invent unsupported inputs. Forecast growth, discount rates, normalized earnings, peer selection, segment multiples, success probabilities, liquidation discounts, and scenario weights must come from `references/valuation_rules/structured_assumption_policy.md`.

Formula provenance and confidence status are tracked in `references/valuation_rules/formula_source_registry.json`. Modules marked `heuristic_helper` are deterministic support calculations and must not be presented as complete standalone valuation models without additional source-backed assumptions and a stronger model wrapper.
