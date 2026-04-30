# Known Failure Modes

## 1. Selected but Not Executed

Example:

```text
Reverse DCF selected but not run.
```

Fix:

```text
Every selected model must produce Result or Blocked.
```

---

## 2. Freshness Checked but Not Enforced

Example:

```text
Report states data is stale but still gives a Buy rating.
```

Fix:

```text
Critical stale data blocks current rating.
```

---

## 3. Good Company / Good Price Confusion

Example:

```text
Business quality is excellent, so rating becomes Buy without valuation support.
```

Fix:

```text
Investment rating requires both quality and price discipline.
```

---

## 4. Margin of Safety Mentioned but Not Calculated

Example:

```text
Report says “needs margin of safety” but gives no MOS range.
```

Fix:

```text
If intrinsic value is discussed, MOS must be calculated or blocked.
```

---

## 5. Single Model Overconfidence

Example:

```text
DCF alone drives conclusion.
```

Fix:

```text
Require primary + cross-check + downside model unless blocked.
```

---

## 6. Per-share Value Without Dilution Check

Example:

```text
Intrinsic value per share calculated using stale basic shares.
```

Fix:

```text
Per-share valuation requires latest diluted shares, SBC, options, convertibles where material.
```

---

## 7. EV Bridge Error

Example:

```text
Enterprise value converted to equity value without net debt / minority interest / investments.
```

Fix:

```text
Capital Structure Gate required for EV-based models.
```

---

## 8. Financial Company Model Misuse

Example:

```text
Bank valued with EV/EBITDA.
```

Fix:

```text
Banks use Residual Income / P/B-ROE / DDM.
```

---

## 9. Cyclical Earnings Trap

Example:

```text
Cyclical stock judged cheap at peak earnings P/E.
```

Fix:

```text
Cycle businesses require mid-cycle earnings.
```

---

## 10. Old Data Used as Current

Example:

```text
FY2021 annual report used for current valuation in 2026.
```

Fix:

```text
Old data can support historical trend, not current conclusion.
```

---

## 11. Source Conflict Ignored

Example:

```text
API revenue differs from 10-K, but no reconciliation.
```

Fix:

```text
Source Quality Gate must reconcile conflicts or select authoritative source.
```

---

## 12. Segment Data Missing in SOTP

Example:

```text
SOTP performed without reliable segment revenue / EBITDA.
```

Fix:

```text
SOTP blocked unless segment metrics are available or clearly estimated.
```

---

## 13. Scenario Probabilities Arbitrary

Example:

```text
Bull/Base/Bear probabilities chosen without explanation.
```

Fix:

```text
Scenario DCF requires probability rationale.
```

---

## 14. Catalyst Assumed but Not Tracked

Example:

```text
Special situation thesis depends on spin-off approval, but no timing or probability.
```

Fix:

```text
Catalyst Gate required.
```

---

## 15. No Thesis Review

Example:

```text
Follow-up report ignores what changed from the original thesis.
```

Fix:

```text
Repeat analysis requires thesis delta section.
```
