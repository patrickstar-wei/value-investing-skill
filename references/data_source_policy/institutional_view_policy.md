# Institutional View Policy

## Purpose

Use institutional research and consensus data as external cross-checks without violating subscription terms, copyrights, or data provenance discipline.

## Allowed Source Types

| Source Type | Use |
|---|---|
| User-provided subscription export | Allowed for local analysis if the user has rights to use it |
| Public summary / news excerpt | Allowed with source URL and date |
| Licensed API | Allowed if credentials are provided through environment variables or local config outside git |
| User-created notes | Allowed if clearly labeled as user notes |
| Full paid report text | Do not reproduce; summarize only |

## Prohibited Behavior

- Do not bypass paywalls or access controls.
- Do not store credentials in git.
- Do not commit raw subscription exports, paid PDFs, or licensed datasets.
- Do not output long excerpts from paid research.
- Do not present institutional target prices as the model's own intrinsic value.

## Required Metadata

Each institutional view must include:

```json
{
  "provider": "string",
  "institution": "string",
  "ticker": "string",
  "as_of_date": "YYYY-MM-DD",
  "source_type": "public_summary / user_provided_export / licensed_api / user_notes",
  "source_path_or_url": "string",
  "license_scope": "public / user_subscription / internal / restricted / unknown",
  "copyright_handling": "summarize_only / structured_fields_only",
  "source_confidence": "high / medium / low / blocked"
}
```

## Use in Reports

Institutional views may support:

- Consensus check
- Variant perception
- Assumption comparison
- Target price distribution
- Earnings estimate revision context
- Bear / bull disagreement map

They must not replace:

- Company filings
- Own valuation model
- Structured assumptions
- Margin-of-safety discipline

## Default Report Language

Translate summary and interpretation into the user's requested output language. Preserve provider names, institution names, tickers, model names, and source titles as appropriate.

