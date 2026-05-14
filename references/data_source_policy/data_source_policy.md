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

Route every ticker through the correct market adapter before retrieving financial statements. A-share tickers such as `000858.SZ` or `600519.SH` must not use SEC EDGAR companyfacts as a primary financial source. If the required market adapter cannot provide financial history, mark current valuation as blocked instead of filling the gap with generic web snippets.

## Default Public Data Retrieval Rule

For normal L1/L2 company analysis, use public sources proactively before asking the user for more data:

- Company official filings, annual reports, quarterly reports, earnings releases, investor presentations, and management guidance.
- Public market data for current price, market capitalization, shares outstanding, rates, and FX where material.
- Public peer, customer, supplier, capex, industry, regulatory, and news sources where they materially constrain assumptions.
- yfinance / OpenBB when available in the runtime; if unavailable, use official pages or other verifiable public web sources.

For current price, "verifiable public web source" means a source with an explicit same-day market timestamp. Undated webpage prices are blocked.

If `yfinance` is not installed in a sandbox/runtime, attempt a local sandbox-target package install before falling back to Yahoo public endpoints. The default target is `/tmp/value-investing-skill-python-packages`; set `VALUE_INVESTING_SKILL_PIP_TARGET` to override it. The connector should install with `pip --target`, add only that target to the current process `sys.path`, and avoid system `site-packages` unless the runtime explicitly points the sandbox target there.

Do not use WebSearch snippets, search-result cards, or webpage snapshots as a substitute for market quote connectors.

Only ask for or list user-provided inputs when they are optional quality enhancers or the analysis is blocked without them.

## Implemented Public Connectors

| Priority | Connector | File | Data | Cost / Access |
|---|---|---|---|---|
| Orchestrator | Public data packet builder | `scripts/connectors/public_data_packet_builder.py` | Market-routed public data packet with adapter-specific financial history, market quote, public IR release snippets, OpenBB readiness | Uses only the enabled public/local connectors below |
| P0 | Market registry | `scripts/markets/registry.py` | Ticker-to-market routing for US, CN_A, HK, unknown | Blocks wrong-market financial sources |
| P0 | SEC EDGAR | `scripts/connectors/sec_edgar_connector.py` | US official submissions, latest 10-K / 10-Q / 8-K, XBRL companyfacts | Free public SEC API; set `SEC_USER_AGENT` for production use |
| P0 | Financial history builder | `scripts/connectors/financial_history_builder.py` | US SEC companyfacts annual and quarterly history with conservative coverage status | Uses official SEC companyfacts; marks limited/blocked instead of filling missing series |
| P0 | A-share adapter | `scripts/markets/cn_a/adapter.py` | CN_A market quote packet boundary and explicit financial-history block until CN_A filings are parsed | Prevents A-share tickers from falling through SEC companyfacts |
| P1 | yfinance / Yahoo Finance | `scripts/connectors/yfinance_connector.py` | Price, market cap, shares, currency, previous close | Free third-party data; optional `yfinance` package, Yahoo fallback |
| P2 | Public IR release parser | `scripts/connectors/ir_release_parser.py` | Earnings release metrics, guidance snippets, risk/event sentences | Free public web/file parser; reconcile numbers to filings |
| P3 | OpenBB provider config | `scripts/connectors/openbb_provider_config.py` | Optional provider availability and API-key readiness | OpenBB is optional; many providers need user API keys or subscriptions |

OpenBB provider configuration:

- Commit only `config/openbb_providers.template.json`.
- Put real keys in `config/openbb_providers.local.json` or environment variables.
- The local file is ignored by git.
- Use OpenBB data only when the runtime check reports `usable=true`.
