# Value Investing Skill Project v19.1

This project is a modular value-investing research skill. It combines company-type routing, structured assumptions, executable valuation models, data freshness / provenance gates, and a fixed report contract.

## What It Does

The skill analyzes a company through this default flow:

```text
CompanyProfile
-> valuation router
-> structured assumption gate
-> data freshness / provenance gates
-> selected Python valuation models
-> ValuationResult
-> fixed report renderer
```

The system is designed to avoid two common mistakes:

- Using a generic DCF for every business.
- Producing precise-looking valuation numbers from unsupported assumptions.

## Core Principles

- Business quality before valuation.
- Cash-flow reality over accounting appearance.
- Valuation model must match company type.
- Margin of safety is required.
- Every material assumption should be structured and evidence-constrained.
- Missing or stale inputs should block or downgrade valuation confidence.
- Calculation traces stay internal by default.

## Supported Company Routes

- Mature Quality Compounder
- Tech-enabled Mature Quality Compounder
- AI / Semiconductor Hypergrowth Platform
- Digital Platform Compounder
- Hyperscale Cloud / Digital Infrastructure Platform
- Managed Care / Healthcare Services Compounder
- Insurance Float-backed Holding Company
- Financial Institution: Bank / Insurance / Asset Manager
- SaaS / Subscription Software Compounder
- Mature Pharma / Pipeline Pharma
- Commodity / Deep Cyclical Producer
- REIT / Infrastructure Yield Asset
- Auto / EV / Mobility Platform
- Fintech / Brokerage Platform

Example mapping:

| Company | Route |
|---|---|
| NVIDIA | AI / Semiconductor Hypergrowth Platform |
| Alphabet / Google | Digital Platform Compounder + Cloud / AI overlay |
| Amazon | Digital Platform Compounder + Cloud + retail margin recovery |
| UnitedHealth | Managed Care / Healthcare Services Compounder |
| Robinhood | Fintech / Brokerage Platform |

## Executable Valuation Models

Python implementations live in `scripts/valuation/`.

| Method | File |
|---|---|
| Shared result envelope / structured assumptions | `valuation_common.py` |
| Owner Earnings DCF | `valuation_owner_earnings_dcf.py` |
| Reverse DCF | `valuation_reverse_dcf.py` |
| EPV / No-growth EPV | `valuation_epv.py` |
| Residual Income | `valuation_residual_income.py` |
| NAV | `valuation_nav.py` |
| DDM / Gordon Growth | `valuation_ddm.py` |
| SOTP | `valuation_sotp.py` |
| Comparable multiples | `valuation_comps.py` |
| Liquidation value | `valuation_liquidation.py` |
| rNPV | `valuation_rnpv.py` |
| REIT / NOI capitalization / AFFO checks | `valuation_reit.py` |
| Cyclical / mid-cycle valuation | `valuation_cyclical.py` |
| Insurance / embedded-value support | `valuation_insurance.py` |
| Scenario-weighted valuation | `valuation_scenario.py` |
| Fintech / brokerage economics | `valuation_fintech.py` |
| Unified execution pipeline | `valuation_executor.py` |

## Structured Assumptions

Material assumptions should use this shape:

```json
{
  "assumption": "discount_rate",
  "value": 0.08,
  "unit": "percent",
  "scenario": "base",
  "evidence": ["risk-free-rate anchor", "industry risk premium"],
  "confidence": "medium",
  "sensitivity": "high",
  "source_or_reason": "Cost of equity estimate"
}
```

If a model needs assumptions that are missing, unsupported, stale, or internally inconsistent, the valuation should be marked `Blocked` or `Low-confidence`.

## Quick Commands

Install into Codex as a local skill on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install\install_codex_skill.ps1
```

Install into Codex as a local skill on Ubuntu / Linux / macOS:

```bash
bash scripts/install/install_codex_skill.sh
```

Install into Claude as a local skill on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install\install_claude_skill.ps1
```

Install into Claude as a local skill on Ubuntu / Linux / macOS:

```bash
bash scripts/install/install_claude_skill.sh
```

On macOS, if your Claude client uses the Application Support directory, use:

```bash
bash scripts/install/install_claude_skill.sh --dir "$HOME/Library/Application Support/Claude/skills"
```

Build a Claude skill package on Windows:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install\package_claude_skill.ps1 -Force
```

Build a Claude skill package on Ubuntu / Linux / macOS:

```bash
bash scripts/install/package_claude_skill.sh --force
```

Optional on Ubuntu / Linux / macOS:

```bash
chmod +x scripts/install/*.sh
./scripts/install/install_codex_skill.sh
```

Run router:

```bash
python -m scripts.routing.select_valuation_models
# Ubuntu systems may prefer:
python3 -m scripts.routing.select_valuation_models
```

Run report renderer smoke test:

```bash
python -m scripts.report.generate_markdown
```

Run valuation model tests:

```bash
python -m unittest tests.test_valuation_models
```

Analyze with local institutional-view files:

```bash
python -m scripts.connectors.institutional_view_parser data/institutional_views NVDA
```

The parser accepts a single `.json` / `.csv` file or a folder. It recursively selects structured exports, filters by ticker or company, and reports PDF / Office / note files as reference-only so paid research is not reproduced.

Run router tests without pytest:

```bash
python -c "import tests.test_valuation_router as t; [getattr(t, name)() for name in dir(t) if name.startswith('test_')]; print('router tests ok')"
```

## Main Files

- `SKILL.md`: top-level skill instructions.
- `.codex-plugin/plugin.json`: Codex plugin metadata.
- `scripts/routing/select_valuation_models.py`: company classification and model routing.
- `scripts/valuation/valuation_executor.py`: unified valuation execution.
- `scripts/install/install_codex_skill.ps1`: local Codex skill installer.
- `scripts/install/install_claude_skill.ps1`: local Claude skill installer.
- `scripts/install/package_claude_skill.ps1`: Claude package / zip builder.
- `scripts/install/install_codex_skill.sh`: Ubuntu / Linux Codex skill installer.
- `scripts/install/install_claude_skill.sh`: Ubuntu / Linux Claude skill installer.
- `scripts/install/package_claude_skill.sh`: Ubuntu / Linux Claude package / zip builder.
- The `.sh` installers also support macOS. Claude's macOS path can be set with `--dir`.
- `scripts/audit/structured_assumption_audit.py`: structured assumption gate.
- `scripts/data/check_data_freshness.py`: data freshness checks.
- `scripts/audit/data_provenance_audit.py`: source / lineage checks.
- `scripts/connectors/institutional_view_parser.py`: safe parser for user-provided institutional view exports.
- `skills/institutional-view-ingestion/SKILL.md`: institutional view ingestion workflow.
- `references/data_source_policy/institutional_view_policy.md`: safety and copyright policy for institutional research.
- `references/core/investment_philosophy_layer.md`: mandatory investment philosophy and quality-control layer.
- `references/masters/`: visual master-lens library with one file per investor framework.
- `references/masters/source_materials/`: Git submodule source library for expanded master-lens materials.
- `references/valuation_rules/structured_assumption_policy.md`: assumption policy.
- `references/output_policy/`: fixed output contract and renderer policy.
- `schemas/valuation_input_packet.schema.json`: valuation input packet schema.

## Development Notes

The project intentionally separates:

```text
Investment judgment -> structured assumptions
Python -> calculation, validation, sensitivity, and blocked/usable status
Renderer -> stable user-facing report
```

Do not add a valuation method that silently fills in critical assumptions. Add the required assumptions to the structured assumption policy and gate first.
