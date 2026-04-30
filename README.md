# Value Investing Skill Project v17.1

这是一个用于构建价值投资研究系统的 Skill 工程骨架。

v17 的重点升级（仍保留）：

1. 新增 **公司分类路由层**：先识别 Base Business Type，再叠加 Shareholder Return、Technology Optionality、Cyclicality 等 Overlay。
2. 新增 **Dividend Compounder / High Shareholder Return Compounder** 估值分支，支持 DDM、Dividend Yield Band、Shareholder Yield 和 Dividend Safety Check。
3. 新增 **Tech-enabled Mature Quality Compounder** 识别规则：成熟现金流主业 + 高股东回报 + 可验证科技业务可选项。
4. 新增 **Technology Optionality Overlay**：科技业务不自动改判为科技股；只有具备分部披露、收入、利润路径和商业化证据时才进入 SOTP 或情景估值。
5. 保留 v15 原则：估值模型的逐步计算过程默认不进入用户报告，只输出估值区间、关键假设、敏感性和安全边际判断。

## 快速开始

```bash
cd value_investing_skill_project_v171
python -m scripts.routing.select_valuation_models
python -m scripts.report.generate_markdown
```

## 推荐开发顺序

1. 先完善 `SKILL.md`
2. 再补充 `skills/*/SKILL.md`
3. 接入 `scripts/connectors/` 数据源
4. 实现 `scripts/valuation/` 估值模型
5. 加入 `scripts/audit/` 模型审计
6. 最后完善 `scripts/report/` 报告生成


## v17 Update: Token-Efficient Multi-Company Routing

This version expands company-type coverage while preserving a lazy-loading token discipline.

New specialized routes:

- AI / Semiconductor Hypergrowth Platform
- Digital Platform Compounder
- Hyperscale Cloud / Digital Infrastructure Platform
- Managed Care / Healthcare Services Compounder
- Insurance Float-backed Holding Company
- Financial Institution: Bank / Insurance / Asset Manager
- SaaS / Subscription Software Compounder
- Commodity / Deep Cyclical Producer
- REIT / Infrastructure Yield Asset
- Auto / EV / Mobility Platform

Default behavior remains compact: classify first, activate one base route, add at most two material overlays, and do not expose calculation traces unless explicitly requested.


## v17.1 Update: Core Philosophy + Modular Workflow Refactor

v17.1 does not keep expanding the monolithic SKILL.md. It preserves v17 capabilities by moving domain-specific logic into lazy-loaded workflows and adding a Core Investment Philosophy Layer as the investment-quality gatekeeper.

Key changes:

1. Added `references/core/investment_philosophy_layer.md` as the non-overridable master-investor principle layer.
2. Added `references/core/investment_quality_gate.md` to enforce business quality, financial quality, model-fit, expectations, margin-of-safety, bear-case, and data-confidence checks.
3. Added `references/core/modular_workflow_architecture.md` to keep the core skill lightweight.
4. Added `workflows/00_router.md` through `workflows/09_watchlist_compare.md` so specialist analysis is loaded on demand.
5. Updated the routing script to surface active workflow files and the quality gate without showing internal scorecards or calculation traces.

Default runtime pattern:

```text
Core Skill → Lightweight Router → 1 primary workflow → up to 2 auxiliary workflows → Investment Quality Gate → Pyramid output
```
