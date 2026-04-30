# Dividend Compounder Valuation Policy v16

## Definition

A **Dividend Compounder** or **High Shareholder Return Compounder** is a mature company where dividends, buybacks, share cancellation, or debt reduction are material contributors to long-term shareholder return.

This policy applies only when shareholder return is supported by sustainable earnings, FCF / FCFE / owner earnings, and balance-sheet capacity.

## Detection Rules

Add the Dividend / Shareholder Return Overlay if most of the following are true:

- Stable dividend history
- Explicit payout or shareholder-return policy
- Reasonable payout ratio versus normalized earnings
- Dividends covered by operating cash flow and free cash flow
- Buybacks or share cancellation reduce share count over time
- Balance sheet supports both payout and necessary reinvestment
- Dividend is not mainly funded by debt, asset sales, or temporary one-off gains

## Model Stack

| Role | Model / Check | Purpose |
|---|---|---|
| Primary cash-flow model | Owner Earnings DCF / FCFE DCF | Estimate intrinsic value from distributable cash flow |
| Dividend model | Two-stage DDM | Value future dividends when payout is durable |
| Stable terminal check | Gordon Growth Model | Check stable-state dividend valuation |
| Yield anchor | Dividend Yield Band | Compare current yield to historical valuation range |
| Shareholder return check | Dividend Yield + Net Buyback Yield + Debt Reduction Yield | Capture full shareholder yield |
| Downside check | No-growth EPV + Dividend Safety | Avoid high-yield traps |
| Implied expectation | Reverse DCF / Implied Dividend Growth | Identify market-implied growth or payout expectations |

## DDM Use Rules

Use DDM as a major valuation input only when:

- Dividend policy is stable
- Dividend is covered by FCFE / owner earnings
- Long-term payout ratio is economically sustainable
- Leverage is not being used to maintain an artificial dividend

If dividends are high but not cash-flow-covered, DDM should be downgraded to a risk flag, not used as a valuation anchor.

## Dividend Safety Checks

Assess:

- Earnings payout ratio
- Cash payout ratio
- FCFE coverage
- Net debt / EBITDA or equivalent leverage measure
- Interest coverage
- CapEx needs
- Working capital volatility
- Cyclicality of earnings
- Whether dividends depend on one-off gains or asset sales

## User-facing output rule

Default reports should show only:

- Dividend Safety: Safe / Watch / Unsafe
- Shareholder Yield: High / Moderate / Low
- DDM relevance: Primary support / Cross-check only / Blocked
- Dividend Yield Band judgment
- Margin-of-safety implication

Do not show dividend model calculation steps unless explicitly requested.
