# Mandatory Output Contract 

## Purpose

Guarantee that every user-facing investment analysis follows a stable, decision-oriented framework regardless of which workflow is activated.

Workflows may reason differently, but the final answer must be rendered through the same output contract.

```text
Workflow = analysis payload
Core Quality Gate = investment standard
Renderer = fixed user-facing report
Validator = format and forbidden-content check
```

## Non-overridable Rules

1. Do not let individual workflows write the final report directly.
2. Every workflow must return structured analysis fields to the fixed report renderer.
3. The final report must preserve valuation range and action guidance.
4. Do not expose detailed valuation calculation traces unless the user explicitly requests model audit, formulas, workbook detail, or debug output.
5. If valuation range or market price is unavailable, do not omit action guidance; mark the affected section as blocked and list missing data.
6. The final report language must follow the user's input language by default. If the user writes in Chinese, render headings, labels, explanations, and action guidance in Chinese. If the user writes in English, render in English. If the user explicitly requests another output language, obey that explicit request.

## Output Language Rule

Workflows and renderers should set or infer:

```json
{
  "output_language": "zh-CN / en / auto"
}
```

Default behavior:

- `auto`: infer from the user's latest investment-analysis request.
- Chinese input -> Chinese output.
- English input -> English output.
- Mixed input -> use the dominant language, unless the user explicitly requests otherwise.
- Company names, tickers, accounting terms, and model names may remain in English where that is clearer.
- Source names and direct source titles should not be force-translated.

## Default L1 Output Order

Every standard stock or company analysis must use this order:

1. `## 📌 Executive Conclusion`
2. `## 🧭 Decision Snapshot`
3. `## 🧭 Company Classification`
4. `## Master Lens Used`
5. `## 🔹 Core Thesis`
6. `## 📊 Key Evidence`
7. `## 🧮 Valuation Summary`
8. `## ⚠️ Key Risks`
9. `## ✅ / ❌ Execution Gate Checklist`
10. `## 🧭 Investor Action Framework`
11. `## 🔍 Data Provenance`

Do not invent new top-level sections in the main report. Put optional details under `## Appendix` only.

## Required Master Lens Fields

The `## Master Lens Used` section must include:

- selected master / framework names
- why each lens was used for this company
- how the lens affected the analysis
- downgraded or deferred master lenses when material

Do not dump every master framework into the report. Include only lenses that materially shape the analysis or explain why a normally relevant lens was downgraded.

## Required Valuation Fields

The `## 🧮 Valuation Summary` section must include the following fields when data is available:

- Selected model stack
- Reasonable intrinsic value range: Bear / Base / Bull
- Current price
- Margin of safety
- Valuation status: undervalued / fair / expensive / blocked / low-confidence
- Key assumptions
- Sensitivity summary
- Price zone assumption basis: explain which valuation anchors and safety-margin rules produced the price/action zones.
- Conclusion change triggers: explicitly state which assumptions, if changed, would change the investment conclusion or action zone.
- Blocked or low-confidence models

The valuation range is mandatory for normal L1/L2 stock analysis. If not enough data is available, the report must say:

```text
Valuation Range: Blocked
Reason: [missing price / missing financials / missing segment data / stale data]
Impact: Cannot provide reliable price-based entry, trim, or sell zones.
```

## Required Investor Action Fields

The `## 🧭 Investor Action Framework` section must include:

1. Price zone table:
   - Deep Value
   - Accumulation
   - Watchlist
   - Fair Value
   - Trim
   - Sell / Avoid

   The price zone table must be followed by a concise `Price Zone Assumption Basis` note explaining:
   - which Bear / Base / Bull intrinsic value anchors were used
   - what margin-of-safety thresholds were applied
   - which assumptions the zones depend on most

2. Position-aware suggestions:
   - Empty Position
   - Half Position
   - Full Position
   - Overweight Position

3. Tranche plan:
   - Starter / first-entry range
   - Add range
   - Strong-add range
   - Hold range
   - Trim range
   - Exit-review / sell-avoid range

4. Thesis conditions:
   - Add only if
   - Hold only if
   - Trim if
   - Exit or avoid if

5. Conclusion change triggers:
   - list the high-sensitivity assumptions that can change the final rating, margin-of-safety judgment, or price zones
   - describe the direction of impact in plain language
   - do not expose full valuation calculation traces unless explicitly requested

If price zones cannot be computed, keep the section and mark it as blocked. Do not replace it with a generic paragraph.

## Position-Aware Guidance Rules

Guidance must be conditional and non-personalized.

Use:

- consider
- may be suitable
- wait for
- monitor
- trim if
- add only if
- reassess if

Avoid:

- must buy
- must sell all
- guaranteed
- risk-free
- certain upside

## Forbidden Default Output

Do not include by default:

- step-by-step valuation calculations
- year-by-year DCF tables
- discounting schedules
- formula derivations
- internal routing scorecards
- internal quality-gate scores
- hidden reasoning traces
- debug logs
- long raw financial tables unless requested

Allowed by default:

- model names
- key assumptions
- intrinsic value range
- margin-of-safety judgment
- price zones
- position-aware action framework
- sensitivity summary
- blocked/missing-data notes

## Deterministic Calculation Rule

Final numerical valuation outputs should come from executable Python valuation scripts, not prompt-only arithmetic. The report may summarize values, assumptions, and sensitivity, but the underlying calculation should be reproducible from the same inputs.

If a valuation number was not produced by a script, label it as a rough manual estimate and do not let it drive the final rating, margin-of-safety judgment, or price/action zones.

## Public Data and Optional User Inputs

For standard company analysis, the skill must proactively use public data that does not require user-provided credentials or files when material and available:

- official filings, company IR, earnings releases, investor presentations, and management guidance
- current price, market capitalization, share count, rates, and FX where material
- public peer, customer, supplier, capex, and industry disclosures
- public news, regulatory events, and company announcements
- yfinance / OpenBB only if available in the runtime; otherwise use verifiable web or official sources

When `scripts/connectors/public_data_packet_builder.py` is usable for the ticker, treat its packet as the first-pass public evidence bundle. Reflect its `sources_used`, `missing_data`, and `errors` in the report's data provenance and optional-data suggestions.

At the end of the report, list optional user-provided data that would improve assumption quality, such as:

- Bloomberg / FactSet / Refinitiv consensus exports
- broker paid research summaries or structured exports
- the user's cost basis, position size, risk budget, or time horizon
- private notes or internal materials
- Wind / Choice / Morningstar exports
- licensed datasets or local files

Do not ask the user for these optional inputs before completing a normal L1/L2 analysis unless the requested analysis is blocked without them.

## L0 Compact Output

For short replies, use this exact compact order:

```markdown
📌 Conclusion:
🧭 Classification:
🧮 Valuation range:
⚖️ Margin of safety:
➡️ Price/action zones:
⚠️ Key risks:
🔍 Data confidence:
```

Even in L0, do not drop valuation range or action zones if the user is asking for an investment view.
