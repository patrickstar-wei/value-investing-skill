# Model Adapter Policy

## Purpose

Different AI systems have different context windows, tool access, reasoning ability, and formatting reliability. This policy defines how to adapt without changing the investment logic.

---

## Adapter Profiles

| Profile | Use Case | Behavior |
|---|---|---|
| Large Context Model | Can handle long filings and full reports | Still use context routing; avoid unnecessary loading |
| Medium Context Model | Standard workflow | Use L0/L1 by default; load only relevant modules |
| Small Context Model | Limited context | Use data packets, schemas, and scripts only |
| No Tool Model | Cannot fetch data or run scripts | Must block sourced valuation unless user provides data packet |
| No Code Model | Cannot execute calculations | Use formulas only if inputs are provided; mark as manual calculation |
| Weak JSON Model | Struggles with strict schema | Produce markdown plus compact validation table |

---

## Mandatory Fallbacks

If model cannot access data:

```text
Data Fetch Blocked
```

If model cannot run scripts:

```text
Calculation Execution Blocked
```

If model cannot verify sources:

```text
Data Provenance Blocked
```

If context budget is insufficient:

```text
Context Budget Blocked / Degraded Mode
```

---

## Consistency Rule

Adapters may change execution method, but not the required gates.

For example:

```text
A no-code model may not run Python DCF,
but it must still provide DCF Blocked or Manual Calculation mode.
```
