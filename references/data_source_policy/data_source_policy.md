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

## Default Public Data Retrieval Rule

For normal L1/L2 company analysis, use public sources proactively before asking the user for more data:

- Company official filings, annual reports, quarterly reports, earnings releases, investor presentations, and management guidance.
- Public market data for current price, market capitalization, shares outstanding, rates, and FX where material.
- Public peer, customer, supplier, capex, industry, regulatory, and news sources where they materially constrain assumptions.
- yfinance / OpenBB when available in the runtime; if unavailable, use official pages or other verifiable public web sources.

Only ask for or list user-provided inputs when they are optional quality enhancers or the analysis is blocked without them.
