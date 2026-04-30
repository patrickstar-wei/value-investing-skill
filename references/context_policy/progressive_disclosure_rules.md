# Progressive Disclosure Rules

## Classification

Each section of documentation should be classified as:

| Tier | Meaning | Loaded When |
|---|---|---|
| Essential | Required every run | Master skill only |
| Router | Needed to choose path | Before model/data selection |
| Reference | Needed for a specific model or industry | After routing |
| Example | Useful for implementation or testing | Only when requested |
| Archive | Historical or rarely used | Never by default |

## Extraction Pattern

Keep this inline:

```text
What this module does
When to use it
Inputs
Outputs
Path to details
```

Move this out:

```text
Long examples
Full formulas
Full templates
Detailed implementation notes
Long industry descriptions
Historical commentary
```

## Recommended Master Skill Structure

```text
1. Purpose
2. Trigger conditions
3. Routing workflow
4. Context budget policy
5. File manifest pointer
6. Critical safety / accuracy rules
7. Output depth levels
```
