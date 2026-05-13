# Workflow 09: Watchlist / Comparison

## Trigger Conditions

Used for peer comparisons, stock pool screening, watchlist creation, ranking, or allocation prioritization.

## Mandatory Relative Analysis Rule

For L1+ public-company analysis in peer-comparable competitive industries, include a relative perspective. Absolute valuation alone is insufficient when a credible peer set exists. If peers are not comparable, market data is stale, or the company is structurally unique, mark the peer check as `blocked`, `low-confidence`, or `not applicable` instead of forcing a multiple conclusion.

### 1. Peer Anchor Rule

When analyzing a peer-comparable company in a competitive industry:

1. **Identify the industry's moat benchmark**
   - Not necessarily the largest company, but the one with the deepest moat
   - Benchmark characteristics: highest ROIC in industry, strongest pricing power, most stable cash flow, deepest moat

2. **Compare core dimensions**

| Comparison Dimension | Meaning | Why Compare |
|---------------------|---------|-------------|
| ROIC Gap | Subject ROIC vs Benchmark ROIC | ROIC gap reflects true moat depth difference |
| Net Margin Gap | Subject Net Margin vs Benchmark Net Margin | Reflects pricing power difference |
| Growth Gap | Subject Growth vs Benchmark Growth | Growth quality comparison |
| Moat Depth Gap | Multi-dimensional moat score comparison | Qualitative assessment quantified |

3. **Relative Valuation Assessment**

```
Relative Valuation Premium/Discount = (Subject PE / Benchmark PE) - 1

Default sanity bands, not mechanical rules:
- Moat deeper than benchmark → Acceptable PE premium (up to +20%)
- Moat similar to benchmark → PE should be similar (±10%)
- Moat weaker than benchmark → PE should trade at discount (at least -20%)
- Moat narrowing trend → Discount should be larger (-30%+)
```

Use the most relevant metric for the business model. PE is not sufficient for loss-making, cyclical, financial, REIT, or high-growth companies; consider EV/EBITDA, EV/Revenue, P/B, P/FFO, P/FCF, growth-adjusted multiples, or normalized-cycle multiples as appropriate.

### 2. Moat Quant Comparison Rule

When comparing peers, moat gaps must be quantified:

```
Convert moat categories to an ordinal scale:
Wide = 3, Narrow = 2, Weak/No Moat = 1

Moat Gap = Subject Moat Score - Benchmark Moat Score

Margin of Safety Adjustment:
- Moat 1 level weaker than benchmark → MOS requirement +10%
- Moat 2 levels weaker than benchmark → MOS requirement +20%
- Narrowing moat trend → Additional +10%
```

---

## Required Outputs for Comparison Analysis

When conducting this workflow or a material L1+ peer check, output the following fields. For compact reports, summarize the matrix in 2-4 rows and mark missing fields as blocked.

### 1. Peer Selection Logic

```
- Criteria for selecting the benchmark and 2-4 comparable companies where feasible
- Why these companies are comparable
- Relationship between subject and peers (direct competition/substitute/reference)
```

### 2. Moat Comparison Matrix

| Company | ROIC | Inferred Moat Rating | AFOS / ROIC Spread | Five Forces Resilience | Moat Trend |
|---------|------|-------------------|----------------|------------------------|------------|
| Benchmark | XX% | Wide/Narrow | A+ | XX | Widening/Stable |
| Subject A | XX% | Wide/Narrow | X | XX | XXX |
| Subject B | XX% | Wide/Narrow | X | XX | XXX |

### 3. Relative Valuation Comparison

| Company | PE | PB | PS | EV/EBITDA | Dividend Yield |
|---------|----|----|----|-----------|----------------|
| Benchmark | Xx | Xx | Xx | Xx | X% |
| Subject A | Xx | Xx | Xx | Xx | X% |
| Subject B | Xx | Xx | Xx | Xx | X% |

**Analysis Conclusions**:
- Which peer percentile does current valuation fall in?
- Is the valuation premium/discount appropriate given the moat gap?

### 4. Investment Conclusion

```
Relative Valuation Verdict:
- Is it cheaper than peers? Cheap/Reasonable/Expensive
- Why cheap/expensive? (Temporary issue or structural issue?)
- Is the valuation discount/premium sufficient to cover the moat gap vs benchmark?

Final Recommendation:
- Buy candidate: Cheaper than peers with comparable moat
- Watch: Reasonable vs peers, but waiting for better entry
- Deep Dive: Expensive vs peers, but special catalysts exist
- Avoid: Insufficient margin of safety
```

---

## Models

Use compact model stacks per company type. Do not run full valuation for every company by default.

## Required Checks

- Business quality
- Valuation attractiveness
- Margin of safety
- **Relative valuation vs peers where applicable**
- Data confidence
- Thesis-breaking risks

## Philosophy Lenses

Greenblatt, Buffett/Munger, Graham.

---

##  Workflow Output Rule

This workflow must not render the final user-facing report directly.

It must return structured analysis fields defined in:

- `references/output_policy/workflow_payload_contract.md`

The final report must be rendered through:

- `references/output_policy/fixed_report_renderer.md`

The final report must preserve:

- Bear / Base / Bull valuation range or blocked status
- **Peer comparison valuation verdict**
- **Moat gap vs benchmark**
- Price zones
- Position-aware suggestions
- Tranche plan
- Key add / hold / trim / exit conditions

Do not expose valuation calculation trace, routing scorecards, or quality-gate internals by default.
