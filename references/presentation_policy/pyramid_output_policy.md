# Pyramid Principle Output Policy

## Purpose

The final investment analysis should be easy to understand, decision-oriented, and structured according to the pyramid principle.

This is not a mind map.

The output should follow:

```text
Conclusion first
↓
Key reasons
↓
Evidence
↓
Risks / caveats
↓
Action framework
```

The goal is to help the user quickly understand:

- What is the conclusion?
- Why is this the conclusion?
- What evidence supports it?
- What could invalidate it?
- What should different investors do?

---

## Default Output Order

Every standard stock analysis should follow this order:

1. Executive Conclusion
2. Decision Snapshot
3. Company Classification
4. Core Thesis
5. Key Evidence
6. Valuation Summary
7. Risk Warnings
8. Execution Gate Checklist
9. Investor Action Framework
10. Data Provenance / Source Notes
11. Detailed Appendix, if needed

---

## Symbol System

Use symbols to make the report easier to read.

| Symbol | Meaning |
|---|---|
| ✅ | Positive / passed / supportive evidence |
| ❌ | Negative / failed / thesis-breaking issue |
| ⚠️ | Risk / warning / uncertainty |
| ➡️ | Action / implication / next step |
| 📌 | Key conclusion / important point |
| 🔹 | Main supporting point |
| 🔸 | Sub-point / detail |
| 💡 | Insight / interpretation |
| 🧮 | Valuation summary / intrinsic value judgment |
| 📊 | Data / metrics |
| 🔍 | Source / verification |
| 🧱 | Moat / business quality |
| 🛡️ | Downside protection / risk control |
| 🧭 | Investor action / decision guidance |

---

## Pyramid Principle Rules

### Rule 1: Conclusion First

Start with the answer.

Bad:

```text
First, we analyze revenue...
```

Good:

```text
📌 Final View: Watchlist / Hold. The company is excellent, but the current price lacks sufficient margin of safety.
```

---

### Rule 2: Group Reasons into 3-5 Buckets

Use 3-5 core reasons, not a long flat list.

Example:

```text
Why:
1. ✅ Business quality is excellent
2. ⚠️ Valuation already prices in strong growth
3. ⚠️ AI CapEx creates FCF uncertainty
4. ➡️ Action: wait for better entry or clearer FCF conversion
```

---

### Rule 3: Separate Fact, Judgment, and Action

Use labels:

```text
📊 Fact:
💡 Interpretation:
➡️ Action:
```

---

### Rule 4: Keep Each Section Short

Default L1 report:

- Executive conclusion: 5-8 lines
- Core reasons: 3-5 bullets
- Evidence: 1 table
- Investor actions: 1 table
- Detailed appendix optional

---

### Rule 5: Blocked Items Must Be Visible

If a module is blocked, show it explicitly.

```text
⚠️ Reverse DCF: Blocked
🔸 Reason: Missing current FCF
➡️ Impact: Cannot judge market-implied growth reliably
```

---


---

## Company Classification Disclosure Policy

The pyramid output should show the company classification result before the valuation summary when classification materially affects model selection.

Default user-facing output should show:

```markdown
## 🧭 Company Classification

**Base Type:** Mature Quality Compounder / Tech-enabled Mature Quality Compounder / Other  
**Overlays:** Dividend / Shareholder Return; Technology Optionality; Light Cyclical Manufacturing  
**Classification Confidence:** High / Medium / Low / Blocked

**Interpretation:**  
[One or two sentences explaining why this company should be valued through this stack.]
```

Do not show internal route scores, scorecard details, or company-name-specific hardcoding unless explicitly requested.

---

## Valuation Disclosure Policy

The pyramid output is a decision summary, not a model workbook.

The skill may calculate DCF, reverse DCF, EPV, NAV, residual income, rNPV, comps, liquidation value, or other models internally, but the default user-facing report must not reveal the step-by-step calculation process.

### Default Valuation Section Should Show

```markdown
## 🧮 Valuation Summary

| Item | Result | Interpretation |
|---|---:|---|
| Company type |  |  |
| Primary model |  |  |
| Dividend / shareholder return model |  |  |
| Technology optionality treatment |  | SOTP / scenario optionality / reflected in core model / no premium |
| Bear value |  |  |
| Base value |  |  |
| Bull value |  |  |
| Current price |  |  |
| Margin of safety |  | ✅ / ⚠️ / ❌ |

**Key assumptions:**
- Assumption 1
- Assumption 2
- Assumption 3

**Shareholder return:** Dividend safety, shareholder yield, and DDM relevance if the Dividend / Shareholder Return Overlay is triggered.

**Technology optionality:** Monetized / emerging / efficiency-only / narrative-only, and whether it deserves SOTP, scenario optionality, core-model treatment, or no premium.

**Sensitivity:** [Plain-language summary of what must be true for the thesis to work.]
```

### Do Not Show by Default

- Full formulas
- Discounting schedules
- Year-by-year projection tables
- Intermediate model line items
- Formula derivations
- Spreadsheet-style calculation process
- Model input source table
- Derived metric table
- Valuation run manifest
- Internal company classification scorecard

### Optional Appendix Only

Detailed valuation mechanics may appear only when the user explicitly asks for calculation detail, formula audit, model audit, appendix, reproducibility package, or debug output. In that case, put them under:

```markdown
## Appendix: Valuation Calculation Detail
```

Do not put calculation detail in the Executive Conclusion, Decision Snapshot, Core Thesis, or main Valuation Summary.

---

## Required Executive Summary Template

```markdown
## 📌 Executive Conclusion

**Rating:**  
**Style Classification:**  
**One-line Judgment:**  

### Why this conclusion?

1. ✅ / ⚠️ / ❌ Reason 1
2. ✅ / ⚠️ / ❌ Reason 2
3. ✅ / ⚠️ / ❌ Reason 3
4. ➡️ Action implication

### Bottom Line

> [One sentence that summarizes business quality, valuation, risk, and action.]
```

---

## Required Decision Snapshot

```markdown
## 🧭 Decision Snapshot

| Dimension | Judgment | Signal |
|---|---|---|
| Business Quality |  | ✅ / ⚠️ / ❌ |
| Company Classification |  | ✅ / ⚠️ / ❌ |
| Valuation |  | ✅ / ⚠️ / ❌ |
| Data Freshness |  | ✅ / ⚠️ / ❌ |
| Data Provenance |  | ✅ / ⚠️ / ❌ |
| Reverse DCF |  | ✅ / ⚠️ / ❌ |
| Margin of Safety |  | ✅ / ⚠️ / ❌ |
| Risk Level |  | ✅ / ⚠️ / ❌ |
| Action |  | ➡️ |
```

---

## Required Core Thesis Format

```markdown
## 🔹 Core Thesis

### 1. ✅ Business Quality
- 📊 Fact:
- 💡 Interpretation:
- ➡️ Implication:

### 2. ⚠️ Valuation
- 🧮 Fact:
- 💡 Interpretation:
- ➡️ Implication:

### 3. ⚠️ Key Risk
- 📊 Fact:
- 💡 Interpretation:
- ➡️ Implication:
```

---

## Required Investor Action Format

```markdown
## 🧭 Investor Action Framework

| Investor Type | Suggested Action | Reason |
|---|---|---|
| Empty Position |  |  |
| Half Position |  |  |
| Full Position |  |  |
| Overweight |  |  |
```

Use conditional language:

- "consider"
- "wait for"
- "monitor"
- "trim if"
- "add only if"

Avoid absolute instructions:

- "must buy"
- "must sell"
- "guaranteed"
- "risk-free"

---

## Compression Mode

For short answers, use this compact format:

```markdown
📌 Conclusion:
✅ Supports:
⚠️ Risks:
🧮 Valuation:
➡️ Action:
🔍 Data confidence:
```

---

## Detailed Mode

For full reports, use:

```markdown
# [Company] Investment Analysis

## 📌 Executive Conclusion
## 🧭 Decision Snapshot
## 🔹 Core Thesis
## 📊 Key Evidence
## 🧮 Valuation Summary
## ⚠️ Risks
## ✅ / ❌ Execution Gate Checklist
## 🧭 Investor Action Framework
## 🔍 Data Provenance
## Appendix
```

---

## Relationship to Mind Map Output

Mind map output is optional.

Pyramid output is the default final presentation style.

Mind map may be used only when the user explicitly asks for mind map, tree, or visual outline.


---

## v19.1 Fixed Output Contract Compatibility

The pyramid output policy is now governed by the Mandatory Output Contract.

Every standard report must include:

- Bear / Base / Bull valuation range, or explicit blocked status
- Current price, or explicit blocked status
- Margin of safety, or explicit blocked status
- Price zones: Deep Value, Accumulation, Watchlist, Fair Value, Trim, Sell / Avoid
- Position-aware suggestions for Empty Position, Half Position, Full Position, and Overweight Position investors
- Tranche plan: starter, add, strong-add, hold, trim, exit-review ranges

Do not shorten away the valuation range or investor action framework. If data is unavailable, render the field as `Blocked` and show missing inputs.
