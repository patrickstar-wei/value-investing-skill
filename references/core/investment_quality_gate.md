# Investment Quality Gate v18

This gate runs after a workflow produces its analysis and before the user-facing report is finalized.

## Required checks

The final report must pass these checks:

1. **Business Quality Check**
   - Is the company a good business, an average business, or a poor business?
   - Are moat, economics, and reinvestment opportunities durable?

2. **Financial Quality Check**
   - Are earnings supported by cash flow?
   - Is leverage acceptable for the business model?
   - Is capital intensity properly reflected?

3. **Model-Fit Check**
   - Does the valuation model match the company type?
   - Are inappropriate models explicitly avoided or deferred?

4. **Expectation Check**
   - What does the current price appear to assume?
   - Does the market-implied scenario require aggressive growth, margin, or reinvestment assumptions?

5. **Margin-of-Safety Check**
   - Is there enough discount to conservative intrinsic value?
   - If not, the action should be Watch / Hold / Avoid rather than Buy.

6. **Bear-Case Check**
   - What facts would break the thesis?
   - Which risks are thesis-breaking versus merely monitorable?

7. **Data Confidence Check**
   - Are the sources current enough?
   - Are critical inputs missing?
   - Is the conclusion blocked or low-confidence?

## Required final labels

Every standard or full report should include these labels:

```text
Business Quality: High / Medium / Low
Valuation Attractiveness: High / Medium / Low
Margin of Safety: Sufficient / Limited / Insufficient
Data Confidence: High / Medium / Low
Action: Buy / Watch / Hold / Avoid / Deep Dive Required
```

## Blocking rules

Use **Deep Dive Required** or **Blocked** when any of these apply:

- No current price or market cap for valuation-sensitive analysis
- No reliable financial statements for the required period
- Material segment data missing for an SOTP-driven thesis
- Dividend safety cannot be checked for a dividend-driven thesis
- Regulatory or litigation exposure dominates but cannot be scoped
- The target company type is unclear and model selection would be speculative

## Token policy

The quality gate must be concise in user output. Do not expose internal checklists, scoring tables, or calculation traces unless the user explicitly requests an audit.
