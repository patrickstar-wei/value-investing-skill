# Reverse DCF Skill

## Purpose

Infer what growth, margin, and cash flow assumptions are implied by the current market price.

## Hard Rule

If this skill is selected by the valuation router, it must either:

1. Execute Reverse DCF, or
2. Explicitly block execution and list missing/stale inputs.

Never only state that Reverse DCF should be run.

## Inputs

- Current share price
- Shares outstanding
- Market cap
- Cash and marketable securities
- Total debt
- Net debt
- Base FCF or base revenue
- Current / normalized FCF margin
- Forecast period
- Discount rate
- Terminal growth rate
- Data source dates

## Modes

### FCF Growth Reverse DCF

Use when base FCF is reliable.

### Revenue-to-FCF Reverse DCF

Use when FCF is temporarily depressed due to reinvestment.

### Scenario Reverse DCF

Use when the company has high uncertainty or multiple possible futures.

## Output

```text
Reverse DCF Result:
- Market-implied EV:
- Base metric:
- Forecast period:
- Discount rate:
- Terminal growth:
- Implied growth:
- Implied FCF margin:
- Reasonableness:
```

## Blocking Output

```text
Reverse DCF Blocked:
- Missing data:
- Stale data:
- Required next data:
- Effect on investment conclusion:
```
