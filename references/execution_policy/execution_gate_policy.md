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
| Structured Assumption Gate | Any valuation model using forecasts, normalization, multiples, probabilities, or discounts | Key assumptions + confidence / blocked |
| Source Quality Gate | Financial data used | Source tier / confidence table |
| Assumption Audit Gate | DCF / scenario / rNPV used | Assumption warnings or pass |
| Formula Audit Gate | Any valuation model used | Formula suitability check |
| Deterministic Calculation Gate | Any numerical valuation output | Executed Python result or blocked / low-confidence |
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

## Structured Assumption Gate

| Gate | Trigger | Required Output |
|---|---|---|
| Structured Assumption Gate | Any valuation model uses forecast or judgment inputs | Assumption table or blocked |

### Minimum Required Fields

For every material assumption, capture:

- Assumption name
- Numeric value or explicit qualitative state
- Scenario: Bear / Base / Bull / Single
- Evidence or source/reason
- Confidence: High / Medium / Low
- Sensitivity: High / Medium / Low

### Blocking Conditions

Block or downgrade valuation confidence if:

- A critical forecast assumption has no evidence or reason.
- Reported earnings or cash flow clearly require normalization but no normalized input is provided.
- Discount rate, terminal growth, peer multiple, success probability, or liquidation discount is unsupported.
- Assumptions are internally inconsistent, such as high growth plus lower reinvestment without evidence.
- Sensitivity is high and the report provides only one point estimate.

### Required Output

```text
Structured Assumption Gate Result
```

or:

```text
Structured Assumption Gate Blocked
- Missing assumption:
- Why it matters:
- Data or evidence needed:
- Impact on valuation:
```

---

## Deterministic Calculation Gate

Assumption generation is judgment-based and may vary across analysts or models. Formula execution must not vary.

For every numerical valuation output, the report or internal execution record must be able to show one of:

```text
Python Valuation Result
- Script:
- Function / model:
- Input packet or assumptions:
- Output:
- Test / formula coverage:
```

or:

```text
Python Valuation Blocked / Low-confidence
- Missing executable script:
- Missing required input:
- Formula not covered by tests:
- Suitability concern:
- Impact on valuation:
```

Rules:

1. Identical inputs to the same valuation script must produce identical outputs.
2. Do not let LLM mental math, spreadsheet-style prompt calculations, or unstated formulas drive final valuation numbers.
3. A valuation algorithm is reliable only when its formula is documented, implemented in `scripts/valuation/`, and covered by unit or golden tests.
4. If formula suitability is uncertain for the company type, block or downgrade the model rather than presenting a precise value.

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
