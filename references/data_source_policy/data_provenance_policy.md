# Data Provenance and Source Annotation Policy

## Purpose

Every number used in valuation, fundamental analysis, scoring, risk analysis, or investor action guidance must be traceable to a source.

The goal is to make it easy for a human reviewer to verify that data was not fabricated by AI.

---

## Core Rule: No Orphan Numbers

No orphan numbers are allowed.

An orphan number is any number in the report or model that does not have:

1. Source name
2. Source type
3. Source URL or local file path
4. Source date
5. Reporting period
6. Extraction timestamp
7. Data field name
8. Confidence score
9. Whether it is raw or derived
10. If derived, formula and input source IDs

If a number lacks provenance, it must be labeled:

```text
Unverified / Assumption / User-provided / Requires source
```

and must not drive the final valuation conclusion.

Current price has an additional provenance requirement: generic WebSearch snippets, search-result cards, and webpage snapshots are not valid current-price sources unless they include an explicit same-day market timestamp. A timestamp-free page price must be labeled `Requires source` / `Blocked` and must not drive margin of safety, reverse DCF, or price/action zones.

---

## Data Classes

| Class | Meaning | Can Drive Valuation? |
|---|---|---|
| Raw Official Data | Company filing, annual report, regulator filing | Yes |
| Raw Market Data | Price, market cap, rates, FX from data API or exchange | Yes, if fresh |
| Raw Third-party Data | yfinance, OpenBB, FMP, Alpha Vantage, etc. | Yes with confidence warning |
| Derived Data | Calculated from sourced inputs | Yes if formula and inputs are traceable |
| Model Assumption | Analyst/model assumption | Yes only if clearly labeled and sensitivity tested |
| User Input | User-provided data or assumption | Yes only if labeled |
| AI Estimate | Generated estimate without source | No; must not drive valuation |

---

## Source Tiering

| Tier | Source Type | Examples | Priority |
|---|---|---|---|
| Tier 1 | Licensed / internal data | Bloomberg, Refinitiv, FactSet, internal database | Highest if available |
| Tier 2 | Official disclosures | SEC filings, company IR, exchange announcements, regulator databases | Highest open/public priority |
| Tier 3 | Open financial APIs | OpenBB, yfinance, Alpha Vantage, FMP | Useful but must be cross-checked |
| Tier 4 | News / research / industry reports | Reuters, company press, industry reports | Context only unless data is primary |
| Tier 5 | User input / assumptions | User-provided numbers | Must be labeled |
| Tier 6 | AI-generated estimates | Model-created numbers without source | Not allowed as data |

---

## Recommended Open / Public Source Types

Use public and human-verifiable sources where possible:

- Company investor relations pages
- Annual reports and quarterly reports
- SEC EDGAR filings for US-listed companies
- Exchange disclosures for non-US markets
- Regulator databases
- Central bank / government statistics
- Company earnings releases and presentations
- ClinicalTrials.gov / FDA / EMA for biotech and pharma
- OpenBB / yfinance / Alpha Vantage / FMP as convenience APIs, preferably cross-checked with official filings

---

## Required Source Annotation Format

Every raw data point should be stored as:

```json
{
  "data_id": "TSLA_Q1_2026_REVENUE",
  "metric": "Revenue",
  "value": 22387000000,
  "unit": "USD",
  "period": "Q1 2026",
  "company": "Tesla Inc.",
  "ticker": "TSLA",
  "source_name": "Tesla Q1 2026 Update",
  "source_type": "Company IR earnings release",
  "source_url": "https://...",
  "source_date": "2026-04-22",
  "extraction_timestamp": "2026-04-30T09:00:00-07:00",
  "page_or_table": "Financial Statements / Consolidated Statements of Operations",
  "source_tier": 2,
  "freshness_status": "Current",
  "confidence": 0.95,
  "raw_or_derived": "raw"
}
```

Derived metrics should be stored as:

```json
{
  "data_id": "TSLA_Q1_2026_FCF",
  "metric": "Free Cash Flow",
  "value": 1444000000,
  "unit": "USD",
  "period": "Q1 2026",
  "raw_or_derived": "derived",
  "formula": "Operating Cash Flow - Capital Expenditures",
  "input_data_ids": [
    "TSLA_Q1_2026_OPERATING_CASH_FLOW",
    "TSLA_Q1_2026_CAPEX"
  ],
  "confidence": 0.93
}
```

---

## Report Requirement

Every investment report must include a Source Annotation Table:

| Data ID | Metric | Value | Period | Source | Source Type | Source Date | URL / Path | Confidence |
|---|---:|---:|---|---|---|---|---|---:|

For every valuation model, include a Model Input Source Table:

| Model | Input | Value | Data ID | Source |
|---|---|---:|---|---|

---

## Derived Metric Requirement

Every derived metric must include:

```text
Metric:
Formula:
Inputs:
Input data IDs:
Output:
```

Example:

```text
FCF = Operating Cash Flow - CapEx
FCF = 3.937B - 2.493B = 1.444B
Source IDs:
- TSLA_Q1_2026_OPERATING_CASH_FLOW
- TSLA_Q1_2026_CAPEX
```

---

## AI Fabrication Prevention Rules

1. Do not invent financial numbers.
2. Do not estimate missing source data unless explicitly labeled as an assumption.
3. Do not mix sourced data with assumptions without marking the difference.
4. Do not use AI-generated numbers as source data.
5. Do not allow unsourced data to affect valuation output.
6. If data is not available, block the calculation or request the missing data.
7. If a number comes from a script/API, store the API name, endpoint, retrieval time, and raw response path if possible.
8. If official and third-party data conflict, prefer official data and log the reconciliation.

---

## Human Verification Mode

When user requests verification, output:

1. All source URLs
2. All source periods
3. Data IDs
4. Model inputs
5. Derived formulas
6. Confidence scores
7. Missing data
8. Unverified assumptions

Do not hide source tables in appendices if the user explicitly asks to verify data.
