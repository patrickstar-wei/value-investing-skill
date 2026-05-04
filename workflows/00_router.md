# Workflow 00: Lightweight Router

## Purpose

Select the minimum necessary workflow set for the user's task.

## Procedure

1. Identify task type: company analysis, valuation, dividend check, thesis update, watchlist, industry, or comparison.
2. Identify company type using economic characteristics rather than company name.
3. Select one primary workflow.
4. Add at most two auxiliary workflows for L0/L1.
5. Defer the rest.
6. Run Investment Quality Gate before final output.

## Output

Default router output should be compact:

```text
Primary workflow: [name]
Auxiliary workflows: [up to two]
Deferred workflows: [only if relevant]
Reason: [one sentence]
```

---

## v19.1 Workflow Output Rule

This workflow must not render the final user-facing report directly.

It must return structured analysis fields defined in:

- `references/output_policy/workflow_payload_contract.md`

The final report must be rendered through:

- `references/output_policy/fixed_report_renderer.md`

The final report must preserve:

- Bear / Base / Bull valuation range or blocked status
- price zones
- position-aware suggestions
- tranche plan
- key add / hold / trim / exit conditions

Do not expose valuation calculation trace, routing scorecards, or quality-gate internals by default.
