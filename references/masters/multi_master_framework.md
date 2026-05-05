# Multi-master Value Investing Framework v20

This folder is the operating map for investor-style lenses. It is not a biography library. Each file should answer: when to use the lens, what questions to ask, what evidence is required, and how it affects valuation.

## Quick Map

| Master / Framework | File | Core Lens | Best Use |
|---|---|---|---|
| Graham | `graham.md` | Margin of safety, asset protection, downside first | Deep value, distressed, asset-heavy, low-confidence inputs |
| Buffett / Munger | `buffett_munger.md` | Moat, owner earnings, compounding, capital allocation | Quality compounders, platform businesses, capital allocators |
| Fisher | `fisher.md` | Growth quality, management quality, reinvestment runway | High-quality growth and technology-enabled businesses |
| Klarman | `klarman.md` | Risk-first thinking, permanent loss avoidance | Special situations, distressed, high uncertainty |
| Greenblatt | `greenblatt.md` | High return on capital plus cheapness | Screening, quality-at-reasonable-price, special situations |
| Howard Marks | `howard_marks.md` | Cycle awareness, risk pricing, second-level thinking | Cyclicals, semiconductors, commodities, credit-sensitive businesses |
| Greenwald | `greenwald.md` | EPV, competitive advantage, reproduction value | Mature stable businesses and moat verification |
| Mauboussin / Rappaport | `mauboussin_rappaport.md` | Expectations investing, reverse DCF | High-expectation stocks and market-implied growth analysis |
| Damodaran | `damodaran.md` | Narrative and numbers, lifecycle valuation | Model selection and story-to-number consistency |
| Jin Jiancheng | `jin_jiancheng.md` | Do not predict; prepare. Cash flow, position sizing, valuation zones, staged add/trim discipline | Translating company value into executable action plans, especially U.S. equities / ETFs and portfolio-aware decisions |

## Folder Rule

Use `references/core/investment_philosophy_layer.md` as the mandatory quality-control layer. Load files from this folder only when the selected workflow or user request needs that specific lens.

Full source materials for expanded master lenses live under `references/masters/source_materials/`. These files are for audit, learning, or source-detail lookup and should not be loaded by default.

## Default Activation

| Workflow | Load These Master Files |
|---|---|
| Quality Company | `buffett_munger.md`, `greenwald.md`, `graham.md` |
| Dividend Compounder | `buffett_munger.md`, `graham.md`, `greenwald.md` |
| Tech Platform | `buffett_munger.md`, `fisher.md`, `mauboussin_rappaport.md`, `damodaran.md` |
| AI Semiconductor | `fisher.md`, `mauboussin_rappaport.md`, `howard_marks.md`, `damodaran.md` |
| Healthcare Managed Care | `graham.md`, `buffett_munger.md`, `damodaran.md` |
| Holding Company / Insurance Float | `buffett_munger.md`, `graham.md`, `greenwald.md` |
| REIT / Infrastructure | `graham.md`, `greenwald.md`, `damodaran.md` |
| Cyclical / Commodity | `howard_marks.md`, `graham.md`, `greenwald.md` |
| Watchlist / Compare | `greenblatt.md`, `buffett_munger.md`, `graham.md` |

## Action Overlay Activation

Load `jin_jiancheng.md` as an auxiliary action lens when a stock/company report needs price zones, staged add/trim rules, cash reserve discipline, position-aware guidance, U.S. asset allocation context, or a check on whether a drawdown is a temporary shock versus a fundamental change. Keep it compact and do not load the raw `jin-jiancheng-perspective` source skill unless the user explicitly asks for that perspective or source-detail lookup.

## Output Rule

Do not dump all master lenses into the final report. Mention only the lenses that materially changed the conclusion.
