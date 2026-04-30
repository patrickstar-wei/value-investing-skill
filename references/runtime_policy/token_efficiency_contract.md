# Token Efficiency Contract

## Purpose

Ensure the Skill remains usable across different AI models without becoming a token-heavy monolith.

---

## Token Efficiency Principles

1. Master Skill must remain compact.
2. Load only the context packet required by the task.
3. Do not load all masters, all industries, all formulas, or all examples.
4. Use scripts for deterministic calculations.
5. Use schemas and data packets instead of long prose.
6. Use progressive disclosure levels.
7. Use summaries for previous work.
8. Use source tables instead of repeatedly quoting source content.
9. Cache stable instructions when runtime supports it.
10. Track selected files and token usage.

---

## Default Context Packet

```text
SKILL.md
+ token budget policy
+ context manifest
+ task command
+ valuation router
+ one or two relevant sub-skills
+ data packet
+ output schema
```

---

## Anti-Bloat Rules

Do not include by default:

- Full valuation formula encyclopedia
- Full value investor biography/history
- All industry frameworks
- All report examples
- Full annual reports
- Full news articles
- Full prior conversation history
- Repeated tool documentation

---

## Budget Modes

| Mode | Max Context Target | Output Target |
|---|---:|---:|
| L0 Quick Check | 4k | <1k |
| L1 Standard | 12k | <3k |
| L2 Full Memo | 30k | <8k |
| L3 Committee Pack | 50k | File-based |
| L4 Audit Package | Case-dependent | File-based |

---

## Over-Budget Behavior

If estimated context exceeds target:

1. Drop examples first.
2. Drop non-selected master frameworks.
3. Drop non-selected industry frameworks.
4. Replace long references with summaries.
5. Keep only source IDs and key extracted values.
6. Defer optional modules.
7. Report what was deferred.

---

## Required Output

Each run should record:

```json
{
  "skill_version": "v17.1",
  "mode": "L1",
  "selected_context_files": [],
  "estimated_input_tokens": 0,
  "output_budget": 3000,
  "deferred_files": [],
  "deferred_modules": []
}
```


## v17 Lazy-Loading Addendum

The broader v17 company coverage must not increase default context usage.

### Default Route Loading

For normal L1 analysis, load only:

```text
SKILL.md
+ token budget policy
+ classification command
+ selected company-type route
+ at most two overlays
+ report template
```

### Route Deferral

If a company could match multiple routes, activate the most material route and list the rest as deferred.

Examples:

- NVIDIA: activate AI / Semiconductor; defer Dividend, REIT, Bank, Managed Care.
- Alphabet: activate Digital Platform; add Cloud/AI overlay only if material; defer Semiconductor unless chip revenue is material.
- UnitedHealth: activate Managed Care; defer generic consumer compounder and SaaS routes.
- Berkshire Hathaway: activate Holding Company / Float; defer standard DCF-only route.

### Output Budget Protection

Do not output:

- full route scorecards
- all possible model descriptions
- valuation calculation traces
- unselected company-type frameworks

Do output:

- selected route
- activated model stack
- deferred modules
- confidence
- missing data fields


## v17.1 Modular Workflow Addendum

The broad company coverage is preserved through lazy-loaded workflows rather than an expanded monolithic prompt.

Default L1 run should load:

```text
SKILL.md
+ references/core/investment_philosophy_layer.md
+ references/core/investment_quality_gate.md
+ workflows/00_router.md
+ one selected primary workflow
+ at most two auxiliary workflows
+ selected report template
```

Do not load unrelated specialist workflows. Do not expose workflow internals, routing scorecards, or valuation calculation traces unless explicitly requested.
