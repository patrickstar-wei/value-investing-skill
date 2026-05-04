# Investor Action Framework

## Purpose

After completing valuation, quality analysis, risk analysis, and execution gate audit, the report should translate conclusions into a position-aware investor action framework.

This module should not produce absolute personalized financial advice. It should provide conditional decision guidance based on:

- Current price
- Intrinsic value range
- Margin of safety
- Business quality
- Downside risk
- Investor current position
- Investor risk tolerance
- Time horizon

---

## Investor Position Types

| Investor Type | Definition |
|---|---|
| Empty Position | Investor currently owns no shares |
| Half Position | Investor already owns a partial position |
| Full Position | Investor already has target/full allocation |
| Overweight Position | Investor position exceeds target allocation |

---

## Required Inputs

This framework requires:

| Input | Description |
|---|---|
| Current price | Latest market price |
| Intrinsic value range | Bear / Base / Bull or low / mid / high estimate |
| Margin of safety | Current price vs intrinsic value |
| Downside value | Bear case or liquidation / no-growth value |
| Business quality rating | Moat, financial quality, management |
| Risk rating | Permanent capital loss, valuation, cycle, regulatory |
| Suggested max allocation | Based on quality and risk |
| Investor position status | Empty / half / full / overweight |
| Time horizon | Short / medium / long-term |

If current price or intrinsic value range is missing, the module must be blocked.

---

## Price Zone Framework

Use valuation range to define action zones.

Let:

```text
IV_low = conservative intrinsic value
IV_mid = base intrinsic value
IV_high = optimistic intrinsic value
MOS = (IV_mid - Current Price) / IV_mid
```

Suggested price zones:

| Zone | Price Range | Meaning |
|---|---|---|
| Deep Value Zone | Price <= 70% × IV_low | Strong margin of safety |
| Accumulation Zone | 70% × IV_low < Price <= 85% × IV_mid | Attractive if thesis intact |
| Watchlist Zone | 85% × IV_mid < Price <= 100% × IV_mid | Fair to slightly undervalued |
| Fair Value Zone | 100% × IV_mid < Price <= 110% × IV_high | Limited upside |
| Trim Zone | 110% × IV_high < Price <= 130% × IV_high | Valuation risk rising |
| Sell / Avoid Zone | Price > 130% × IV_high | Expectations likely too high |

These thresholds are defaults and should be adjusted based on business quality and risk.

Every report must state the price zone assumption basis immediately after the zone table:

- Which IV_low / IV_mid / IV_high anchors were used.
- Which margin-of-safety thresholds were applied or adjusted.
- Which assumptions the zones depend on most.
- Which assumption changes would move the zones enough to change the final action.

---

## Quality Adjustment

For very high-quality compounders:

```text
Required MOS may be lower.
```

For cyclical, leveraged, low-quality, or uncertain businesses:

```text
Required MOS must be higher.
```

Default required margin of safety:

| Business Type | Required MOS |
|---|---:|
| High-quality compounder | 15%-25% |
| Average business | 25%-35% |
| Cyclical business | 35%-50% |
| Distressed / special situation | 40%-60% |
| Biotech / high uncertainty | Scenario-specific |

---

## Position-Aware Action Matrix

### Empty Position Investor

| Price Zone | Suggested Action |
|---|---|
| Deep Value Zone | Consider building position in tranches |
| Accumulation Zone | Consider starter position / gradual accumulation |
| Watchlist Zone | Add to watchlist; wait for better entry |
| Fair Value Zone | Usually wait unless quality is exceptional |
| Trim Zone | Avoid new position |
| Sell / Avoid Zone | Avoid; expectations too high |

---

### Half Position Investor

| Price Zone | Suggested Action |
|---|---|
| Deep Value Zone | Consider adding if thesis intact |
| Accumulation Zone | Consider adding gradually |
| Watchlist Zone | Hold / monitor |
| Fair Value Zone | Hold, avoid aggressive adding |
| Trim Zone | Consider trimming if position risk high |
| Sell / Avoid Zone | Consider reducing if valuation risk dominates |

---

### Full Position Investor

| Price Zone | Suggested Action |
|---|---|
| Deep Value Zone | Hold; add only if max allocation allows |
| Accumulation Zone | Hold; avoid concentration risk |
| Watchlist Zone | Hold |
| Fair Value Zone | Hold; reassess opportunity cost |
| Trim Zone | Consider trimming to target allocation |
| Sell / Avoid Zone | Consider partial exit / rebalance |

---

### Overweight Investor

| Price Zone | Suggested Action |
|---|---|
| Deep Value Zone | Hold only if risk budget allows |
| Accumulation Zone | Hold / rebalance risk |
| Watchlist Zone | Reduce concentration if needed |
| Fair Value Zone | Trim toward target allocation |
| Trim Zone | Trim / rebalance |
| Sell / Avoid Zone | Strongly consider reducing exposure |

---

## Tranche-Based Entry Framework

Avoid all-in decisions.

Example tranching:

| Trigger | Allocation |
|---|---:|
| Starter position | 20%-30% of target position |
| Price falls into Accumulation Zone | Add 20%-30% |
| Price falls into Deep Value Zone and thesis intact | Add 30%-50% |
| Thesis improves with evidence | Add cautiously |
| Thesis breaks | Stop adding / exit review |

---

## Sell / Trim Framework

Selling should be based on valuation, thesis, and opportunity cost.

Sell or trim triggers:

1. Price exceeds optimistic value range.
2. Reverse DCF implies unrealistic expectations.
3. Thesis is broken.
4. Business quality deteriorates.
5. Risk becomes asymmetric to downside.
6. Better opportunity with higher risk-adjusted return exists.
7. Position exceeds risk budget.

---

## Stop-Loss vs Thesis-Loss

Value investing should not rely only on mechanical stop-loss.

Distinguish:

```text
Price decline because market is wrong
```

from:

```text
Price decline because thesis is wrong
```

Use:

| Situation | Response |
|---|---|
| Price down, thesis intact, valuation better | Consider adding |
| Price down, thesis uncertain | Pause and review |
| Price down, thesis broken | Reduce / exit |
| Price up, valuation excessive | Trim / rebalance |

---

## Required Output Format

```markdown
## Investor Action Framework

### Price Zone

| Zone | Price Range | Interpretation |
|---|---:|---|
| Deep Value |  |  |
| Accumulation |  |  |
| Watchlist |  |  |
| Fair Value |  |  |
| Trim |  |  |
| Sell / Avoid |  |  |

### Position-Aware Suggestions

| Investor Type | Suggested Action | Rationale |
|---|---|---|
| Empty Position |  |  |
| Half Position |  |  |
| Full Position |  |  |
| Overweight |  |  |

### Tranche Plan

- Starter price:
- Add price:
- Strong add price:
- Hold range:
- Trim range:
- Exit review range:

### Key Conditions

- Add only if:
- Hold only if:
- Trim if:
- Exit if:
```

---

## Blocking Rule

If valuation range is missing, output:

```text
Investor Action Framework Blocked

Reason:
- Missing intrinsic value range
- Missing current price
- Missing downside value
- Missing risk rating

Impact:
Cannot provide price-based action zones.
```

---

## Compliance Rule

Use conditional language:

- "consider"
- "may be suitable"
- "would require"
- "if thesis remains intact"

Avoid absolute personalized instructions:

- "you must buy"
- "you should sell all"
- "guaranteed"
- "risk-free"


---

## v20 Mandatory Preservation Rule

The Investor Action Framework is mandatory in default stock/company analysis.

Do not remove this section when enforcing a shorter or fixed output format.

The section must include:

1. Price Zone table
2. Position-Aware Suggestions table
3. Tranche Plan
4. Key Conditions

If intrinsic value range or current price is missing, mark the section as blocked and list missing inputs. Do not replace it with a generic action paragraph.
