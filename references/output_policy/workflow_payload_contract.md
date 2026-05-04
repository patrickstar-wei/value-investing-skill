# Workflow Payload Contract v18

## Purpose

Ensure all workflows return consistent structured fields to the fixed report renderer.

## Required Payload Fields

```json
{
  "output_language": "zh-CN / en / auto",
  "executive_conclusion": {
    "rating": "Buy / Watchlist / Hold / Avoid / Blocked",
    "style_classification": "string",
    "one_line_judgment": "string",
    "key_reasons": ["string"],
    "bottom_line": "string"
  },
  "decision_snapshot": [
    {"dimension": "Business Quality", "judgment": "string", "signal": "✅ / ⚠️ / ❌"}
  ],
  "company_classification": {
    "base_type": "string",
    "overlays": ["string"],
    "primary_workflow": "string",
    "auxiliary_workflows": ["string"],
    "classification_confidence": "high / medium / low / blocked",
    "classification_interpretation": "string"
  },
  "core_thesis": {
    "bull_case": ["string"],
    "bear_case": ["string"]
  },
  "key_evidence": [
    {"fact": "string", "interpretation": "string", "investment_implication": "string"}
  ],
  "valuation_summary": {
    "selected_models": ["string"],
    "bear_value": "number/string/blocked",
    "base_value": "number/string/blocked",
    "bull_value": "number/string/blocked",
    "current_price": "number/string/blocked",
    "margin_of_safety": "number/string/blocked",
    "valuation_status": "undervalued / fair / expensive / blocked / low-confidence",
    "key_assumptions": ["string"],
    "structured_assumptions": [
      {
        "assumption": "string",
        "value": "number/string",
        "unit": "string",
        "scenario": "bear / base / bull / single",
        "evidence": ["string"],
        "confidence": "high / medium / low",
        "sensitivity": "high / medium / low",
        "source_or_reason": "string"
      }
    ],
    "assumption_confidence": "high / medium / low / blocked",
    "sensitivity_summary": "string",
    "blocked_or_low_confidence_items": ["string"]
  },
  "risks": ["string"],
  "execution_gate_checklist": [
    {"gate": "string", "status": "✅ / ⚠️ / ❌", "comment": "string"}
  ],
  "investor_action_framework": {
    "price_zones": [
      {"zone": "Deep Value", "range": "string", "interpretation": "string"}
    ],
    "position_aware_suggestions": [
      {"investor_type": "Empty Position", "suggested_action": "string", "rationale": "string"}
    ],
    "tranche_plan": {
      "starter_range": "string",
      "add_range": "string",
      "strong_add_range": "string",
      "hold_range": "string",
      "trim_range": "string",
      "exit_review_range": "string"
    },
    "key_conditions": {
      "add_only_if": "string",
      "hold_only_if": "string",
      "trim_if": "string",
      "exit_or_avoid_if": "string"
    }
  },
  "data_provenance": {
    "data_confidence": "high / medium / low / blocked",
    "analysis_as_of": "string",
    "market_data_as_of": "string",
    "latest_financial_period": "string",
    "missing_data": ["string"]
  }
}
```

## Workflow Rule

A workflow must not render the final report directly. It must populate these fields and let the fixed renderer produce the user-facing report.
