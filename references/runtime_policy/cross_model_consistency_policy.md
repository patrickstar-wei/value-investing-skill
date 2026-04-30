# Cross-Model Consistency Policy

## Purpose

Different AI models may not produce identical prose, but the Skill should enforce consistent process, required checks, output structure, and decision logic.

The goal is not identical wording. The goal is:

```text
Same input + same data packet + same Skill version
→ same workflow
→ same gates
→ same valuation model routing
→ same required outputs
→ comparable investment conclusion
```

---

## What Can Be Standardized

| Layer | Standardizable? | Method |
|---|---|---|
| Input schema | Yes | Use JSON task manifest |
| Data provenance | Yes | Use data IDs and source tables |
| Data freshness | Yes | Use freshness thresholds |
| Valuation model routing | Mostly yes | Use deterministic routing table |
| Formula calculations | Yes | Use scripts, not free-form reasoning |
| Execution gates | Yes | Use Result / Blocked contract |
| Output structure | Yes | Use report schema |
| Final wording | No | Allow model-specific style |
| Qualitative judgment | Partially | Use scorecards and evidence tables |

---

## Deterministic Core

The following must be deterministic and should not depend on model style:

1. Task classification
2. Data freshness status
3. Data provenance status
4. Valuation model selection
5. Whether a gate is Passed / Blocked / Not Applicable
6. Formula outputs
7. Margin of safety calculation
8. Price zone classification
9. Required missing data list

---

## Non-deterministic Layer

The following may vary by AI model:

1. Natural language explanation
2. Narrative emphasis
3. Writing style
4. Length within allowed budget
5. Qualitative nuance

These are acceptable if they do not violate gates, schemas, or source constraints.

---

## Required Consistency Controls

1. Use `valuation_run_manifest.json` for every run.
2. Use `data_lineage.json` for every numerical input.
3. Use `execution_gate_checklist.json` before final conclusion.
4. Use report schema for output.
5. Run conformance tests on golden cases.
6. Keep long references outside default context.
7. Use scripts for calculations.
8. Log token usage and selected context files.
9. Pin Skill version in every report.

---

## Final Report Requirement

Every report should include:

```text
Skill version:
Run mode:
Model / AI system:
Analysis as-of date:
Context packet loaded:
Data lineage file:
Execution gate checklist:
```

## Mind Map Output Consistency

The following should also be standardized across models:

- Mind map root structure
- Main branch names
- Blocked node representation
- Final view branch
- Investor action branch
- Monitoring branch

Different AI models may phrase leaf nodes differently, but the branch structure should remain comparable.
