# Execution Gate Policy

## Purpose

Convert important analysis requirements from “should do” into mandatory execution gates.

A report is incomplete if it selects a module, model, or audit step but does not either:

1. Execute it, or
2. Explicitly block it and explain missing/stale inputs.

---

## General Rule

For every selected module, the final report must include one of:

```text
[Module] Result
```

or:

```text
[Module] Blocked
- Missing inputs:
- Stale inputs:
- Data source issue:
- Impact on conclusion:
- Required next data:
```

---

## Mandatory Execution Gates

| Gate | Trigger | Required Output |
|---|---|---|
| Data Freshness Gate | Any current valuation or rating | Freshness table or blocked |
| Valuation Model Gate | Any selected valuation model | Model result or blocked |
| Reverse DCF Gate | Market expectations matter | Reverse DCF result or blocked |
| Margin of Safety Gate | Intrinsic value discussed | MOS result or blocked |
| Downside Case Gate | Any investment view | Downside case or blocked |
| Source Quality Gate | Financial data used | Source tier / confidence table |
| Assumption Audit Gate | DCF / scenario / rNPV used | Assumption warnings or pass |
| Formula Audit Gate | Any valuation model used | Formula suitability check |
| Sensitivity Gate | DCF / rNPV / scenario used | Sensitivity table or blocked |
| Dilution Gate | Per-share valuation used | Share count / SBC / dilution check |
| Capital Structure Gate | EV / equity bridge used | Net debt bridge or blocked |
| Segment Gate | SOTP or multi-business company | Segment data or blocked |
| Financials Gate | Bank / insurance / broker | Financial-sector-specific model or blocked |
| Currency Gate | Cross-market valuation | Reporting currency and FX date |
| Restatement Gate | Latest filings used | Restatement / accounting change check |
| Catalyst Gate | Special situation thesis | Catalyst probability / timing or blocked |
| Thesis Review Gate | Repeat analysis | What changed since last analysis |

---

## Blocker Severity

| Severity | Meaning | Effect |
|---|---|---|
| Critical | Cannot form current conclusion | Block rating |
| High | Can analyze but not value confidently | Block price target / MOS |
| Medium | Requires caution | Add warning |
| Low | Non-core issue | Note in appendix |

---

## Final Report Requirement

Before the final investment view, include:

```text
Execution Gate Checklist
```

with status:

- Passed
- Blocked
- Not Applicable
- Deferred

## Investor Action Gate

| Gate | Trigger | Required Output |
|---|---|---|
| Investor Action Gate | User asks what to do / buy price / sell price / position guidance | Price zones + position-aware suggestions or blocked |

### Blocking Conditions

Block investor action guidance if:

- Current price is missing or stale
- Intrinsic value range is missing
- Downside value is missing
- Risk analysis is missing
- Margin of safety is missing

### Required Output

```text
Investor Action Framework Result
```

or:

```text
Investor Action Framework Blocked
```

## Data Provenance Gate

| Gate | Trigger | Required Output |
|---|---|---|
| Data Provenance Gate | Any numerical input used in valuation, fundamentals, scoring, or action framework | Source Annotation Table + Derived Metric Table or blocked |

### Blocking Conditions

Block valuation if:

- A critical number lacks source metadata.
- A critical derived metric lacks formula.
- A critical derived metric lacks input data IDs.
- AI-generated estimates are used as raw data.
- Official and third-party data conflict without reconciliation.
- Source URL / local path is missing for raw data.

### Required Output

```text
Data Provenance Result
```

or:

```text
Data Provenance Blocked
```
