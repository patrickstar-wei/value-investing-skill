# Token Budget Policy

## Goal

Reduce token consumption without weakening investment research quality.

The system should not load every framework, valuation model, example, and report template into context at once. It should load:

1. A compact master routing prompt
2. Only the relevant sub-skill
3. Only the needed reference cards
4. Only the required data fields
5. Only the output depth requested by the user

---

## Default Token Budgets

| Mode | Use Case | Target Input Context | Target Output |
|---|---|---:|---:|
| L0 Quick Check | 是否值得深入 | 2k-4k tokens | 500-900 tokens |
| L1 Standard Report | 标准分析 | 6k-12k tokens | 1.5k-3k tokens |
| L2 Full Memo | 完整备忘录 | 12k-30k tokens | 4k-8k tokens |
| L3 Committee Pack | 投委会材料 | 20k-50k tokens | file deliverables |
| L4 Audit Package | 可审计模型包 | case-dependent | XLSX + audit logs |

---

## Hard Rules

1. Master `SKILL.md` should remain compact.
2. Do not inline all valuation formulas in the master skill.
3. Do not load all value-investing masters unless the task is specifically about philosophy comparison.
4. Do not load every industry framework. Load only the matched industry and one adjacent industry if needed.
5. Do not load full filings by default. Extract data packets.
6. Do not output full report unless user requests full memo or committee pack.
7. Store long formulas and examples as reference cards.
8. Use scripts for calculations instead of asking the model to carry large formula blocks in context.
9. Use caching for stable system instructions, tool definitions, and long reusable documents when API/runtime supports it.
10. Log token usage and cache-hit metrics when available.
