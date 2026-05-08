# Data Freshness Policy

## Purpose

Investment analysis must reflect the current situation of the company, not a stale historical snapshot.

A valuation or investment report is not considered valid unless it states:

```text
Analysis as-of date:
Market data as-of:
Financial statement period:
Latest filing used:
Latest earnings release used:
Latest guidance / management commentary used:
Data freshness status:
```

---

## Core Rule

Do not use financial statements from several years ago to make a current investment conclusion.

Old financial statements may be used for historical trend analysis, but not as the primary basis for current valuation unless clearly labeled as historical.

---

## Freshness Requirements by Data Type

| Data Type | Preferred Freshness | If Stale |
|---|---:|---|
| Current price | Same trading day or latest available close | Do not calculate current margin of safety |
| Market cap / EV | Same trading day or latest available close | Mark valuation as stale |
| Shares outstanding | Latest filing / latest diluted share count | Flag dilution risk |
| Revenue / EBIT / Net income | Latest quarterly / semiannual / annual report | Use only as historical trend |
| Cash flow / FCF | Latest cash flow statement and TTM if possible | Do not rely on old FCF as current cash generation |
| Debt / cash | Latest balance sheet | Do not calculate net debt from old filings |
| Guidance | Latest earnings call / company update | Mark forward assumptions as unverified |
| Segment data | Latest filing or investor presentation | Mark segment valuation as low confidence |
| Peer multiples | Recent market data | Do not use old peer multiples for current relative valuation |
| Regulatory / clinical data | Latest regulator / trial database update | Mark rNPV probability assumptions as stale |
| Commodity / interest rates / FX | Recent market data | Stress-test or defer conclusion |

---

## Freshness Status

Each analysis must classify data as one of:

| Status | Meaning |
|---|---|
| Current | Suitable for current valuation |
| Recent but needs review | Usable with caution |
| Stale | Not suitable for current valuation conclusion |
| Historical only | Only suitable for trend analysis |
| Missing | Must request or fetch data |

---

## Default Staleness Thresholds

These are internal operating thresholds, not accounting rules.

| Data Category | Stale If Older Than |
|---|---:|
| Market price | 5 trading days |
| Market multiples | 10 trading days |
| Quarterly financials | 150 calendar days |
| Semiannual financials | 240 calendar days |
| Annual financials | 450 calendar days |
| Earnings call / guidance | 180 calendar days |
| Segment data | 450 calendar days |
| Peer group data | 30 calendar days |
| Clinical / regulatory data | 90 calendar days |
| Macro rates / FX / commodity prices | 10 trading days |

---

## Current Situation Rule

To analyze “current situation”, the system should combine:

```text
Latest financial statements
+ latest earnings release
+ latest management guidance
+ latest major filings / announcements
+ current market price
+ recent industry / macro context
```

A report that only uses historical annual reports is a historical analysis, not a current investment analysis.

---

## Required Output Warning

If data is stale, output:

```text
Data Freshness Warning:
The latest available financial data used in this analysis is from [period/date].
This may not reflect the company's current situation.
Current valuation and margin of safety should not be treated as reliable until updated data is fetched.
```

---

## Valuation Impact

If current price is missing or stale:

```text
Do not calculate current margin of safety.
```

For market price freshness, "current" requires same-day market data:

```text
Current Price must include a regular-market timestamp on the same calendar date as the analysis timestamp.
If the quote is delayed but same-day, disclose the exact timestamp.
If the quote timestamp is missing or from a prior date, block current margin of safety, reverse DCF, and price-zone conclusions until a same-day quote is available.
Generic WebSearch snippets, search-result cards, and webpage snapshots are not valid current-price sources unless they include an explicit same-day market timestamp.
```

If latest balance sheet is stale:

```text
Do not calculate reliable net debt or enterprise value.
```

If latest revenue / EBIT / FCF is stale:

```text
Do not run current DCF as final conclusion.
Use historical trend analysis only.
```

If guidance is stale or missing:

```text
Forward assumptions must be explicitly labeled as analyst assumptions.
```

---

## Audit Requirement

Every report should include a Data Freshness Table:

| Metric | Value | Period | Source | Source Date | Freshness Status |
|---|---:|---|---|---|---|
| Current Price |  |  |  |  |  |
| Revenue |  |  |  |  |  |
| EBIT |  |  |  |  |  |
| FCF |  |  |  |  |  |
| Cash |  |  |  |  |  |
| Debt |  |  |  |  |  |
| Shares Outstanding |  |  |  |  |  |

---

## Rule for Old Data

Old data is allowed for:

- 5-year / 10-year trend analysis
- Cycle analysis
- Normalized earnings
- ROIC stability
- Margin stability
- Historical capital allocation review

Old data is not allowed for:

- Current intrinsic value conclusion
- Current margin of safety
- Current net debt
- Current peer multiple comparison
- Current investment rating
