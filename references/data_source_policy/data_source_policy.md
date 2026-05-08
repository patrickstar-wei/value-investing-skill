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

Do not treat generic WebSearch snippets, search-result cards, or webpage snapshots as valid current-price sources unless they include an explicit same-day market timestamp. A visible price without a market timestamp is not current market data and must not drive margin of safety, reverse DCF, or price/action zones.

## Default Public Data Retrieval Rule

For normal L1/L2 company analysis, use public sources proactively before asking the user for more data:

- Company official filings, annual reports, quarterly reports, earnings releases, investor presentations, and management guidance.
- Public market data for current price, market capitalization, shares outstanding, rates, and FX where material.
- Public peer, customer, supplier, capex, industry, regulatory, and news sources where they materially constrain assumptions.
- yfinance / OpenBB when available in the runtime; if unavailable, use official pages or other verifiable public web sources.

For current price, "verifiable public web source" means a source with an explicit same-day market timestamp. Undated webpage prices are blocked.

Only ask for or list user-provided inputs when they are optional quality enhancers or the analysis is blocked without them.

## Implemented Public Connectors

| Priority | Connector | File | Data | Cost / Access |
|---|---|---|---|---|
| Orchestrator | Public data packet builder | `scripts/connectors/public_data_packet_builder.py` | SEC filings/facts, market quote, public IR release snippets, OpenBB readiness in one packet | Uses only the enabled public/local connectors below |
| P0 | SEC EDGAR | `scripts/connectors/sec_edgar_connector.py` | Official submissions, latest 10-K / 10-Q / 8-K, XBRL companyfacts | Free public SEC API; set `SEC_USER_AGENT` for production use |
| P1 | yfinance / Yahoo Finance | `scripts/connectors/yfinance_connector.py` | Price, market cap, shares, currency, previous close | Free third-party data; optional `yfinance` package, Yahoo fallback |
| P2 | Public IR release parser | `scripts/connectors/ir_release_parser.py` | Earnings release metrics, guidance snippets, risk/event sentences | Free public web/file parser; reconcile numbers to filings |
| P3 | OpenBB provider config | `scripts/connectors/openbb_provider_config.py` | Optional provider availability and API-key readiness | OpenBB is optional; many providers need user API keys or subscriptions |

OpenBB provider configuration:

- Commit only `config/openbb_providers.template.json`.
- Put real keys in `config/openbb_providers.local.json` or environment variables.
- The local file is ignored by git.
- Use OpenBB data only when the runtime check reports `usable=true`.
