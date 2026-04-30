# Investor Action Framework Skill

## Purpose

Translate completed investment analysis into position-aware action guidance.

## Trigger Conditions

Activate after:

- A full stock analysis is completed
- Intrinsic value range is estimated
- Margin of safety is calculated
- Risk analysis is completed
- User asks what empty / half / full position investors should do
- User asks what price is suitable for entry, adding, trimming, or selling

## Inputs

- Current price
- Intrinsic value low / mid / high
- Margin of safety
- Downside value
- Business quality rating
- Risk rating
- Investor position status
- Time horizon
- Max allocation guideline

## Hard Rule

This module must not be executed before valuation and risk analysis are complete.

If valuation range or current price is missing, output:

```text
Investor Action Framework Blocked
```

## Output

1. Price zone table
2. Empty-position investor suggestion
3. Half-position investor suggestion
4. Full-position investor suggestion
5. Overweight investor suggestion
6. Tranche-based entry plan
7. Trim / sell framework
8. Conditions that would change the view

## Language Rule

Use conditional decision language, not absolute personalized financial advice.
