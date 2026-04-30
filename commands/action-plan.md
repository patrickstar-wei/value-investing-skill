# /action-plan

Generate position-aware investor action guidance after valuation is completed.

Example:

```text
/action-plan AAPL
/action-plan GOOGL --position empty
/action-plan JPM --position half
```

Required previous outputs:

- Data freshness check
- Valuation range
- Margin of safety
- Downside case
- Risk analysis
- Execution gate checklist

Output:

- Price zones
- Empty / half / full / overweight investor suggestions
- Tranche entry framework
- Trim / sell framework
- Conditions that would change the view
