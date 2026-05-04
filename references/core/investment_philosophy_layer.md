# Core Investment Philosophy Layer v19

This layer is the permanent quality-control layer for every workflow. It is not an optional reference and must be applied after routing and before final output.

## Role

The Core Skill is not only a router. It is the investment-quality gatekeeper.

```text
Core Skill = investment principles + output discipline + quality gate + routing control
Workflow = domain-specific analysis process
Router = low-cost selection mechanism
```

## Non-overridable principles

All workflows must obey these principles:

1. **Business quality before valuation**
   - Assess the durability of the business before deciding whether the price is attractive.
   - Do not let low valuation multiples compensate for structurally poor economics unless the workflow is explicitly a distressed or asset-value route.

2. **Cash-flow reality over accounting appearance**
   - Earnings quality, free cash flow conversion, reinvestment needs, working capital, and capital intensity must be checked before relying on reported earnings.

3. **Valuation model must match company type**
   - DDM is appropriate only when dividends approximate distributable cash flow and are sustainable.
   - Owner Earnings DCF / FCFE DCF is appropriate for mature cash-flow companies.
   - SOTP is appropriate when business segments have materially different economics.
   - Reverse DCF is required when current valuation depends on high growth expectations.
   - Specialist routes must be used for banks, insurance, managed care, REITs, commodity cyclicals, AI semiconductors, SaaS, and holding companies when those economics dominate.

4. **Margin of safety is required**
   - A good company is not automatically a good investment.
   - The final report must separate business quality, valuation attractiveness, and margin of safety.

5. **Evidence must support every investment conclusion**
   - Each major conclusion should map to: Fact → Interpretation → Investment implication.

6. **Bear-case discipline is mandatory**
   - Every workflow must identify what would break the thesis.
   - The report must include red flags, not only supporting arguments.

7. **Calculation trace is internal by default**
   - The skill may calculate internally, but the final report should show valuation range, key assumptions, sensitivity, and confidence rather than line-by-line formulas or spreadsheet schedules.

8. **Data confidence gates the action**
   - If required data is missing, stale, or low-confidence, the action must be Watch / Deep Dive Required / Blocked rather than Buy.

## Master lenses and when to activate them

The detailed master files live in `references/masters/`. Use `references/masters/multi_master_framework.md` as the visual index, then load only the specific lens needed by the selected workflow.

| Master / Framework | File | Core Lens | Use It When |
|---|---|---|---|
| Graham | `references/masters/graham.md` | Margin of safety, asset backing, downside protection | Deep value, distressed, asset-heavy, low-confidence situations |
| Buffett / Munger | `references/masters/buffett_munger.md` | Moat, owner earnings, compounding, capital allocation | Quality compounders, mature cash-flow companies, platform businesses |
| Fisher | `references/masters/fisher.md` | Growth quality, management quality, reinvestment runway | High-quality growth, durable technology or platform businesses |
| Klarman | `references/masters/klarman.md` | Risk-first thinking, asymmetric payoff, permanent capital loss | Special situations, distressed assets, high-uncertainty valuation |
| Greenblatt | `references/masters/greenblatt.md` | High return on capital plus cheapness | Screening, quality-at-reasonable-price, special situations |
| Howard Marks | `references/masters/howard_marks.md` | Cycle awareness, risk pricing, second-level thinking | Cyclicals, semiconductors, commodities, credit-sensitive businesses |
| Greenwald | `references/masters/greenwald.md` | EPV, competitive advantage, reproduction value | Mature stable businesses and moat verification |
| Mauboussin / Rappaport | `references/masters/mauboussin_rappaport.md` | Expectations investing, reverse DCF | High-expectation stocks and market-implied growth analysis |
| Damodaran | `references/masters/damodaran.md` | Narrative and numbers, lifecycle-based valuation | Model selection across company lifecycle and story-to-number consistency |

## Workflow-specific philosophy mapping

| Workflow | Required Philosophy Lenses |
|---|---|
| Quality Company | `buffett_munger.md`, `greenwald.md`, `graham.md` |
| Dividend Compounder | `buffett_munger.md`, `graham.md`, `greenwald.md` |
| Tech Platform | `buffett_munger.md`, `fisher.md`, `mauboussin_rappaport.md`, `damodaran.md` |
| AI Semiconductor | `fisher.md`, `mauboussin_rappaport.md`, `howard_marks.md`, `damodaran.md` |
| Healthcare Managed Care | `graham.md`, `buffett_munger.md`, `damodaran.md`, regulatory risk discipline |
| Holding Company / Insurance Float | `buffett_munger.md`, `graham.md`, `greenwald.md`, capital allocation discipline |
| REIT / Infrastructure | `graham.md`, `greenwald.md`, `damodaran.md`, rate-cycle discipline |
| Cyclical / Commodity | `howard_marks.md`, `graham.md`, `greenwald.md` |
| Watchlist / Compare | `greenblatt.md`, `buffett_munger.md`, `graham.md` |

## User-facing philosophy output

Do not dump the full master framework into every report.

Default stock/company analysis must include a compact `Master Lens Used` section. It should identify only the lenses that materially shape the analysis:

```text
Master Lens Used:
- Buffett / Munger: used for moat, owner earnings, capital allocation, and margin-of-safety discipline.
- Greenwald: used for EPV and franchise-value cross-check.
```

If a specific master lens materially affects the conclusion, mention it briefly:

```text
Expectation check is central here: the current price requires growth assumptions that leave little margin of safety.
```

Do not write a long explanation of each master unless the user explicitly asks for investment philosophy, framework comparison, or learning-oriented output.
