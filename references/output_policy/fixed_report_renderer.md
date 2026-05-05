# Fixed Report Renderer v20.1

## Purpose

Render every workflow's structured payload into one stable Markdown report.

The renderer owns final formatting. Workflows own analysis only.

## Renderer Template

The renderer must follow `output_language` from the payload. If `output_language` is missing, infer it from the user's request before rendering. For Chinese requests, translate fixed headings, labels, and guidance into Chinese while preserving tickers, model names, and source titles where useful.

```markdown
# [Company] Investment Analysis

## 📌 Executive Conclusion

**Rating:** {{rating}}  
**Style Classification:** {{style_classification}}  
**One-line Judgment:** {{one_line_judgment}}

### Why this conclusion?

1. {{reason_1}}
2. {{reason_2}}
3. {{reason_3}}
4. {{action_implication}}

### Bottom Line

> {{bottom_line}}

## 🧭 Decision Snapshot

| Dimension | Judgment | Signal |
|---|---|---|
| Business Quality | {{business_quality}} | {{business_quality_signal}} |
| Company Classification | {{company_classification}} | {{classification_signal}} |
| Valuation | {{valuation_judgment}} | {{valuation_signal}} |
| Margin of Safety | {{margin_of_safety}} | {{mos_signal}} |
| Risk Level | {{risk_level}} | {{risk_signal}} |
| Data Confidence | {{data_confidence}} | {{data_signal}} |
| Action | {{action}} | ➡️ |

## 🧭 Company Classification

**Base Type:** {{base_type}}  
**Overlays:** {{overlays}}  
**Primary Workflow:** {{primary_workflow}}  
**Auxiliary Workflows:** {{auxiliary_workflows}}  
**Classification Confidence:** {{classification_confidence}}

**Interpretation:**  
{{classification_interpretation}}

## Master Lens Used

| Master / Framework | Why Used | Impact on Analysis |
|---|---|---|
{{master_lens_rows}}

**Downgraded / deferred lenses:**  
{{downgraded_master_lenses}}

## 🔹 Core Thesis

### Bull Case
{{bull_case}}

### Bear Case
{{bear_case}}

## 📊 Key Evidence

For each evidence item:

- 📊 Fact: {{fact}}
- 💡 Interpretation: {{interpretation}}
- ➡️ Investment Implication: {{investment_implication}}

## 🧮 Valuation Summary

| Item | Result | Interpretation |
|---|---:|---|
| Selected models | {{selected_models}} | {{model_interpretation}} |
| Bear value | {{bear_value}} | {{bear_interpretation}} |
| Base value | {{base_value}} | {{base_interpretation}} |
| Bull value | {{bull_value}} | {{bull_interpretation}} |
| Current price | {{current_price}} | {{price_interpretation}} |
| Margin of safety | {{margin_of_safety}} | {{mos_interpretation}} |
| Valuation status | {{valuation_status}} | {{valuation_status_interpretation}} |

**Key assumptions:**
{{key_assumptions}}

**Assumption confidence:** {{assumption_confidence}}

**Structured assumptions:** {{structured_assumptions}}

**Sensitivity summary:**  
{{sensitivity_summary}}

**Conclusion change triggers:**  
{{conclusion_change_triggers}}

**Blocked / low-confidence valuation items:**  
{{blocked_valuation_items}}

## ⚠️ Key Risks

{{key_risks}}

## ✅ / ❌ Execution Gate Checklist

| Gate | Status | Comment |
|---|---|---|
{{execution_gate_rows}}

## 🧭 Investor Action Framework

### Price Zones

| Zone | Price Range | Interpretation |
|---|---:|---|
| Deep Value | {{deep_value_range}} | {{deep_value_interpretation}} |
| Accumulation | {{accumulation_range}} | {{accumulation_interpretation}} |
| Watchlist | {{watchlist_range}} | {{watchlist_interpretation}} |
| Fair Value | {{fair_value_range}} | {{fair_value_interpretation}} |
| Trim | {{trim_range}} | {{trim_interpretation}} |
| Sell / Avoid | {{sell_avoid_range}} | {{sell_avoid_interpretation}} |

**Price Zone Assumption Basis:**  
{{price_zone_assumption_basis}}

### Position-Aware Suggestions

| Investor Type | Suggested Action | Rationale |
|---|---|---|
| Empty Position | {{empty_position_action}} | {{empty_position_rationale}} |
| Half Position | {{half_position_action}} | {{half_position_rationale}} |
| Full Position | {{full_position_action}} | {{full_position_rationale}} |
| Overweight Position | {{overweight_position_action}} | {{overweight_position_rationale}} |

### Tranche Plan

- Starter / first-entry range: {{starter_range}}
- Add range: {{add_range}}
- Strong-add range: {{strong_add_range}}
- Hold range: {{hold_range}}
- Trim range: {{trim_range}}
- Exit-review / sell-avoid range: {{exit_review_range}}

### Key Conditions

- Add only if: {{add_condition}}
- Hold only if: {{hold_condition}}
- Trim if: {{trim_condition}}
- Exit or avoid if: {{exit_condition}}

## 🔍 Data Provenance

**Data Confidence:** {{data_confidence}}  
**Analysis as-of:** {{analysis_as_of}}  
**Market data as-of:** {{market_data_as_of}}  
**Latest financial period used:** {{latest_financial_period}}  
**Important missing data:** {{missing_data}}

**Public data sources used / checked:**  
{{public_data_sources_used}}

**Optional user-provided data that would improve the analysis:**  
{{suggested_user_provided_inputs}}
```

## Blocked Valuation Rendering

If valuation range is blocked, still render the same sections:

- Valuation Summary: mark Bear/Base/Bull as `Blocked`.
- Price Zones: mark all ranges as `Blocked`.
- Position-Aware Suggestions: give non-price-based guidance, e.g. `Wait for valuation data`.
- Data Provenance: list missing inputs.

## Renderer Discipline

The renderer must not add formulas or model steps. It may summarize assumptions and sensitivity in plain language.
