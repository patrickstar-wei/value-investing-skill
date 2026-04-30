# Reverse DCF Execution Policy

## Purpose

Reverse DCF is not just a suggested cross-check. If the valuation router selects Reverse DCF as the implied-expectation model, the system must either:

1. Execute Reverse DCF, or
2. Explicitly block execution and list the missing/stale inputs.

It is not acceptable to only say “Reverse DCF should be run” in the final report.

---

## Mandatory Trigger Conditions

Reverse DCF must be executed or blocked when any of the following is true:

- Current valuation appears demanding.
- The company trades at a premium multiple.
- The investment thesis depends on long-term growth.
- AI / cloud / biotech / SaaS / platform optionality is a major part of valuation.
- The report says “market has priced in high expectations”.
- The valuation router selects Reverse DCF as the implied-expectation model.
- User explicitly asks whether current price is reasonable.

---

## Minimum Required Inputs

Reverse DCF requires:

| Input | Description |
|---|---|
| Current share price | Latest available price |
| Shares outstanding | Prefer latest diluted share count |
| Net debt | Total debt minus cash and marketable securities |
| Base revenue or base FCF | Starting point for forecast |
| Current or normalized FCF margin | If using revenue-to-FCF method |
| Forecast period | Usually 5-10 years |
| Discount rate | WACC or cost of equity depending model |
| Terminal growth | Conservative long-term growth assumption |
| Tax / reinvestment assumptions | If using revenue build-up |
| Data as-of dates | Required for freshness audit |

---

## Execution Modes

### Mode A: FCF Growth Reverse DCF

Use when reliable base FCF is available.

```text
Market-implied EV = Market Cap + Net Debt

Solve for g such that:

Market-implied EV =
Σ [FCF_0 × (1 + g)^t / (1 + WACC)^t]
+ Terminal Value / (1 + WACC)^n
```

Terminal value:

```text
Terminal Value =
FCF_n × (1 + terminal_g) / (WACC - terminal_g)
```

Output:

```text
Implied FCF CAGR
```

---

### Mode B: Revenue-to-FCF Reverse DCF

Use when FCF is temporarily depressed by investment cycle.

```text
Revenue_t = Revenue_0 × (1 + revenue_growth)^t
FCF_t = Revenue_t × target_FCF_margin
```

Solve for:

```text
Implied revenue CAGR
or
Implied terminal FCF margin
```

Output:

```text
Implied revenue growth
Implied FCF margin
Implied FCF in terminal year
```

---

### Mode C: Scenario Reverse DCF

Use when business has high uncertainty.

Output three implied cases:

| Case | Revenue Growth | FCF Margin | WACC | Terminal Growth |
|---|---:|---:|---:|---:|
| Bear |  |  |  |  |
| Base |  |  |  |  |
| Bull |  |  |  |  |

---

## Blocking Rule

If required data is missing or stale, output:

```text
Reverse DCF Execution Blocked

Reason:
- Missing / stale input:
- Required data:
- How to obtain:
- Analysis impact:
```

Do not silently skip Reverse DCF.

---

## Report Requirement

Every report that selects Reverse DCF must include one of:

```text
Reverse DCF Result:
- Market-implied EV:
- Base FCF / Revenue:
- WACC:
- Terminal growth:
- Forecast period:
- Implied growth:
- Reasonableness judgment:
```

or:

```text
Reverse DCF Blocked:
- Missing inputs:
- Stale inputs:
- Data needed:
```
