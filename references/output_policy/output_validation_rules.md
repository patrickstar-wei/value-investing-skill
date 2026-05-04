# Output Validation Rules v19.1

## Purpose

Check the final report before it is shown to the user.

## Required Section Check

For standard L1/L2 investment analysis, the final report must contain these headings in this order:

1. `## 📌 Executive Conclusion`
2. `## 🧭 Decision Snapshot`
3. `## 🧭 Company Classification`
4. `## Master Lens Used`
5. `## 🔹 Core Thesis`
6. `## 📊 Key Evidence`
7. `## 🧮 Valuation Summary`
8. `## ⚠️ Key Risks`
9. `## ✅ / ❌ Execution Gate Checklist`
10. `## 🧭 Investor Action Framework`
11. `## 🔍 Data Provenance`

## Required Field Check

The report must include:

- Rating
- One-line judgment
- Company classification
- Master lens used, rationale, and impact
- Selected valuation models
- Bear / Base / Bull valuation range or explicit blocked status
- Current price or explicit blocked status
- Margin of safety or explicit blocked status
- Price zones or explicit blocked status
- Price zone assumption basis
- Conclusion change triggers
- Position-aware suggestions for empty, half, full, and overweight investors
- Build / add / hold / trim / exit-review ranges or explicit blocked status
- Key risks
- Data confidence

## Forbidden Content Check

Unless explicitly requested, the report must not include:

- valuation calculation trace
- year-by-year DCF schedule
- discount factor table
- formula derivation
- internal routing scores
- internal quality-gate scores
- hidden reasoning traces
- debug logs

## Auto-Repair Rule

If the report fails validation, rewrite it through the Fixed Report Renderer before returning it.

If valuation data is missing, do not delete the valuation or action sections. Render blocked placeholders and list missing inputs.
