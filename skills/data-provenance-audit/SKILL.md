# Data Provenance Audit Skill

## Purpose

Ensure every number used in investment analysis is traceable to a human-verifiable source.

## Trigger Conditions

Activate whenever:

- A valuation model is run
- Fundamental metrics are calculated
- A report includes current price, revenue, earnings, cash flow, debt, shares, or margins
- A scorecard uses numerical inputs
- User asks to verify sources or prevent AI-fabricated data

## Hard Rule

No orphan numbers.

Every number must be one of:

- Sourced raw data
- Derived data with formula and sourced inputs
- Explicit model assumption
- Explicit user input

Unsourced numbers must not drive valuation.

## Workflow

1. Collect all numerical inputs.
2. Assign data IDs.
3. Attach source metadata.
4. Classify raw / derived / assumption / user input.
5. Check freshness.
6. Check confidence.
7. Reconcile conflicts across sources.
8. Produce Source Annotation Table.
9. Block valuation if critical source data is missing.

## Output

```markdown
## Data Provenance Audit

### Source Annotation Table

| Data ID | Metric | Value | Period | Source | URL / Path | Confidence |
|---|---:|---:|---|---|---|---:|

### Derived Metric Table

| Data ID | Metric | Formula | Input IDs | Result |
|---|---|---|---|---:|

### Unverified / Assumption Table

| Item | Value | Reason | Impact |
|---|---:|---|---|

### Blockers

- Missing source:
- Conflicting source:
- Stale source:
```
