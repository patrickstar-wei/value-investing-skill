# Token-Efficient Routing Policy v17

## Goal

Expand company coverage without turning the skill into a token-heavy monolith.

## Mandatory Lazy-Loading Contract

1. Always classify first using compact facts.
2. Activate one base route.
3. Activate no more than two overlays by default.
4. Defer all non-material routes.
5. Use scripts and schemas for deterministic calculations.
6. Output only conclusions, selected models, key assumptions, sensitivity, and deferred modules.
7. Do not show internal scorecards or valuation calculation traces by default.

## Context Budget by Depth

| Depth | Use | Route Loading |
|---|---|---|
| L0 | Quick check | SKILL + classification only |
| L1 | Standard analysis | SKILL + selected route + one or two overlays |
| L2 | Full memo | selected route + material overlays + data audit + risk framework |
| L3 | Committee pack | file-based appendices; avoid putting full calculations in chat |
| L4 | Audit package | model details allowed only by explicit request |

## Model Activation Cap

Default L1 output should activate:

- 1 primary model
- 1-2 cross-check models
- 1 downside model
- 1 implied-expectation model
- overlay models only if material

If more models are possible, list them as deferred rather than loading or explaining them.

## Broad-Coverage Query Behavior

When the user asks whether many companies can be analyzed, do not run full analysis for each company.

Return a compact coverage matrix:

```text
Company → Type → Support Level → Route → Needs Specialist Module?
```

## Missing Data Behavior

If required facts are missing, do not load every possible framework. Mark confidence as medium/low and ask for or fetch only the missing data fields needed by the selected route.
