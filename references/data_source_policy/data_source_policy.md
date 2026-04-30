# Data Source Policy

## Data Source Hierarchy

| Tier | Source Type | Use |
|---|---|---|
| Tier 1 | Licensed professional data / internal database / MCP | Primary financial and market data |
| Tier 2 | Company filings, annual reports, regulatory disclosures | Authoritative source |
| Tier 3 | Open-source financial APIs | Supplement and automation |
| Tier 4 | News, industry reports, web pages | Events, context, narrative |
| Tier 5 | User input / model estimates | Only when clearly labeled |

## Required Metadata

Each data point should store:

```json
{
  "metric": "Revenue",
  "value": null,
  "period": "FY2025",
  "source": null,
  "source_tier": null,
  "confidence": null,
  "last_updated": null
}
```

## Rule

Do not treat web summaries as primary financial statement data when official filings are available.
