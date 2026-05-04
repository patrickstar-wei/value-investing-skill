# Multi-master Value Investing Framework v19.1

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

## Output Rule

Do not dump all master lenses into the final report. Mention only the lenses that materially changed the conclusion.
