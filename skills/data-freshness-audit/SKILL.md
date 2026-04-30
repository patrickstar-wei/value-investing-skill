# Data Freshness Audit Skill

## Purpose

Ensure investment analysis reflects the current situation of the company.

## Trigger Conditions

Activate whenever:

- A current valuation is requested
- A margin of safety is calculated
- A buy / hold / avoid rating is generated
- Financial statements are used
- User asks about “current situation”, “now”, “latest”, or “today”

## Workflow

1. Identify analysis as-of date.
2. Identify source date for each critical data point.
3. Classify freshness:
   - Current
   - Recent but needs review
   - Stale
   - Historical only
   - Missing
4. Block current valuation if key data is stale.
5. Allow old data only for historical trend or normalized cycle analysis.
6. Output Data Freshness Table.
7. Add warning if current data is insufficient.

## Blocking Data for Current Valuation

Current valuation must not be finalized if any of these are stale or missing:

- Current price
- Shares outstanding
- Revenue
- EBIT / operating income
- Free cash flow
- Cash
- Debt
- Latest filing period

## Required Output

```text
Analysis as-of date:
Market data as-of:
Financial statement period:
Latest filing used:
Data freshness status:
```

## Rule

If data is stale, say explicitly:

```text
This is a historical analysis, not a current investment analysis.
```
