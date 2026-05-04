"""Fixed bilingual report renderer.

Workflows produce a structured payload. This renderer owns the stable Markdown
shape and can render fixed headings / labels in English or Simplified Chinese
based on payload["output_language"].
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List
import re


FORBIDDEN_PHRASES = [
    "step-by-step valuation calculation",
    "discounting schedule",
    "internal routing score",
    "internal scorecard",
    "debug trace",
    "hidden reasoning",
]


LABELS: Dict[str, Dict[str, str]] = {
    "en": {
        "title": "{target} Investment Analysis",
        "executive": "## Executive Conclusion",
        "rating": "Rating",
        "style": "Style Classification",
        "one_line": "One-line Judgment",
        "why": "### Why this conclusion?",
        "bottom": "### Bottom Line",
        "snapshot": "## Decision Snapshot",
        "dimension": "Dimension",
        "judgment": "Judgment",
        "signal": "Signal",
        "classification": "## Company Classification",
        "base_type": "Base Type",
        "overlays": "Overlays",
        "primary_workflow": "Primary Workflow",
        "aux_workflows": "Auxiliary Workflows",
        "classification_confidence": "Classification Confidence",
        "interpretation": "Interpretation",
        "master_lens": "## Master Lens Used",
        "master": "Master / Framework",
        "lens_rationale": "Why Used",
        "lens_influence": "Impact on Analysis",
        "downgraded_lenses": "Downgraded / deferred lenses",
        "thesis": "## Core Thesis",
        "bull": "### Bull Case",
        "bear": "### Bear Case",
        "evidence": "## Key Evidence",
        "fact": "Fact",
        "implication": "Investment Implication",
        "valuation": "## Valuation Summary",
        "item": "Item",
        "result": "Result",
        "selected_models": "Selected models",
        "bear_value": "Bear value",
        "base_value": "Base value",
        "bull_value": "Bull value",
        "current_price": "Current price",
        "mos": "Margin of safety",
        "valuation_status": "Valuation status",
        "key_assumptions": "Key assumptions",
        "assumption_confidence": "Assumption confidence",
        "structured_assumptions": "Structured assumptions",
        "assumption": "Assumption",
        "value": "Value",
        "scenario": "Scenario",
        "confidence": "Confidence",
        "sensitivity": "Sensitivity",
        "sensitivity_summary": "Sensitivity summary",
        "blocked": "Blocked / low-confidence valuation items",
        "risks": "## Key Risks",
        "gates": "## Execution Gate Checklist",
        "gate": "Gate",
        "status": "Status",
        "comment": "Comment",
        "action": "## Investor Action Framework",
        "price_zones": "### Price Zones",
        "zone": "Zone",
        "price_range": "Price Range",
        "position": "### Position-Aware Suggestions",
        "investor_type": "Investor Type",
        "suggested_action": "Suggested Action",
        "rationale": "Rationale",
        "tranche": "### Tranche Plan",
        "starter": "Starter / first-entry range",
        "add": "Add range",
        "strong_add": "Strong-add range",
        "hold": "Hold range",
        "trim": "Trim range",
        "exit": "Exit-review / sell-avoid range",
        "conditions": "### Key Conditions",
        "add_if": "Add only if",
        "hold_if": "Hold only if",
        "trim_if": "Trim if",
        "exit_if": "Exit or avoid if",
        "provenance": "## Data Provenance",
        "data_confidence": "Data Confidence",
        "analysis_as_of": "Analysis as-of",
        "market_as_of": "Market data as-of",
        "latest_period": "Latest financial period used",
        "missing": "Important missing data",
        "none": "None noted",
    },
    "zh-CN": {
        "title": "{target} 投资分析",
        "executive": "## 执行结论",
        "rating": "评级",
        "style": "风格分类",
        "one_line": "一句话判断",
        "why": "### 为什么是这个结论？",
        "bottom": "### 底线结论",
        "snapshot": "## 决策快照",
        "dimension": "维度",
        "judgment": "判断",
        "signal": "信号",
        "classification": "## 公司分类",
        "base_type": "基础类型",
        "overlays": "叠加标签",
        "primary_workflow": "主工作流",
        "aux_workflows": "辅助工作流",
        "classification_confidence": "分类置信度",
        "interpretation": "解读",
        "master_lens": "## 大师框架",
        "master": "大师 / 框架",
        "lens_rationale": "使用原因",
        "lens_influence": "对分析的影响",
        "downgraded_lenses": "降权 / 暂缓框架",
        "thesis": "## 核心投资论点",
        "bull": "### 乐观情景",
        "bear": "### 悲观情景",
        "evidence": "## 关键证据",
        "fact": "事实",
        "implication": "投资含义",
        "valuation": "## 估值摘要",
        "item": "项目",
        "result": "结果",
        "selected_models": "选用模型",
        "bear_value": "悲观价值",
        "base_value": "基准价值",
        "bull_value": "乐观价值",
        "current_price": "当前价格",
        "mos": "安全边际",
        "valuation_status": "估值状态",
        "key_assumptions": "关键假设",
        "assumption_confidence": "假设置信度",
        "structured_assumptions": "结构化假设",
        "assumption": "假设",
        "value": "数值",
        "scenario": "情景",
        "confidence": "置信度",
        "sensitivity": "敏感性",
        "sensitivity_summary": "敏感性摘要",
        "blocked": "受阻 / 低置信度估值项",
        "risks": "## 关键风险",
        "gates": "## 执行门禁检查",
        "gate": "门禁",
        "status": "状态",
        "comment": "说明",
        "action": "## 投资者行动框架",
        "price_zones": "### 价格区间",
        "zone": "区间",
        "price_range": "价格范围",
        "position": "### 按持仓状态的建议",
        "investor_type": "投资者类型",
        "suggested_action": "建议动作",
        "rationale": "理由",
        "tranche": "### 分批计划",
        "starter": "初始建仓区间",
        "add": "加仓区间",
        "strong_add": "强加仓区间",
        "hold": "持有区间",
        "trim": "减仓区间",
        "exit": "退出复核 / 卖出规避区间",
        "conditions": "### 关键条件",
        "add_if": "仅在以下条件加仓",
        "hold_if": "仅在以下条件持有",
        "trim_if": "出现以下情况减仓",
        "exit_if": "出现以下情况退出或规避",
        "provenance": "## 数据来源",
        "data_confidence": "数据置信度",
        "analysis_as_of": "分析截至日期",
        "market_as_of": "市场数据截至日期",
        "latest_period": "使用的最新财务期",
        "missing": "重要缺失数据",
        "none": "未注明",
    },
}


REQUIRED_SECTIONS_BY_LANGUAGE = {
    lang: [
        labels["executive"],
        labels["snapshot"],
        labels["classification"],
        labels["master_lens"],
        labels["thesis"],
        labels["evidence"],
        labels["valuation"],
        labels["risks"],
        labels["gates"],
        labels["action"],
        labels["provenance"],
    ]
    for lang, labels in LABELS.items()
}


def _language(payload: Dict[str, Any]) -> str:
    language = payload.get("output_language", "en")
    if language in {"zh", "zh-CN", "Chinese", "中文"}:
        return "zh-CN"
    if language == "auto" or "output_language" not in payload:
        user_text = str(payload.get("user_request", payload.get("latest_user_message", "")))
        if re.search(r"[\u4e00-\u9fff]", user_text):
            return "zh-CN"
    return "en"


def _labels(payload: Dict[str, Any]) -> Dict[str, str]:
    return LABELS[_language(payload)]


def _list(items: Iterable[Any]) -> str:
    values = list(items or [])
    if not values:
        return "- N/A"
    return "\n".join(f"- {item}" for item in values)


def _table_rows(rows: Iterable[Dict[str, Any]], columns: List[str]) -> str:
    out = []
    for row in rows or []:
        out.append("| " + " | ".join(str(row.get(col, "N/A")) for col in columns) + " |")
    return "\n".join(out) if out else "| N/A | N/A | N/A |"


def render_report(payload: Dict[str, Any]) -> str:
    """Render a structured investment payload into the fixed L1 report."""

    labels = _labels(payload)
    ec = payload.get("executive_conclusion", {})
    classification = payload.get("company_classification", {})
    master_lenses = payload.get("master_lens_used", payload.get("master_lenses_used", []))
    downgraded_lenses = payload.get("downgraded_master_lenses", [])
    thesis = payload.get("core_thesis", {})
    valuation = payload.get("valuation_summary", payload.get("valuation_results", {}))
    action = payload.get("investor_action_framework", {})
    provenance = payload.get("data_provenance", {})

    decision_rows = payload.get("decision_snapshot", [])
    evidence = payload.get("key_evidence", [])
    gates = payload.get("execution_gate_checklist", [])

    lines: List[str] = []
    lines.append("# " + labels["title"].format(target=payload.get("target_name", "[Company]")))
    lines.append("")
    lines.append(labels["executive"])
    lines.append("")
    lines.append(f"**{labels['rating']}:** {ec.get('rating', 'N/A')}  ")
    lines.append(f"**{labels['style']}:** {ec.get('style_classification', 'N/A')}  ")
    lines.append(f"**{labels['one_line']}:** {ec.get('one_line_judgment', 'N/A')}")
    lines.append("")
    lines.append(labels["why"])
    lines.append("")
    for i, reason in enumerate(ec.get("key_reasons", []), 1):
        lines.append(f"{i}. {reason}")
    if not ec.get("key_reasons"):
        lines.append("1. N/A")
    lines.append("")
    lines.append(labels["bottom"])
    lines.append("")
    lines.append(f"> {ec.get('bottom_line', 'N/A')}")
    lines.append("")

    lines.append(labels["snapshot"])
    lines.append("")
    lines.append(f"| {labels['dimension']} | {labels['judgment']} | {labels['signal']} |")
    lines.append("|---|---|---|")
    lines.append(_table_rows(decision_rows, ["dimension", "judgment", "signal"]) if decision_rows else "| N/A | N/A | N/A |")
    lines.append("")

    lines.append(labels["classification"])
    lines.append("")
    lines.append(f"**{labels['base_type']}:** {classification.get('base_type', 'N/A')}  ")
    overlays = classification.get("overlays", [])
    lines.append(f"**{labels['overlays']}:** {', '.join(overlays) if overlays else 'N/A'}  ")
    lines.append(f"**{labels['primary_workflow']}:** {classification.get('primary_workflow', 'N/A')}  ")
    aux = classification.get("auxiliary_workflows", [])
    lines.append(f"**{labels['aux_workflows']}:** {', '.join(aux) if aux else 'N/A'}  ")
    lines.append(f"**{labels['classification_confidence']}:** {classification.get('classification_confidence', 'N/A')}")
    lines.append("")
    lines.append(f"**{labels['interpretation']}:** {classification.get('classification_interpretation', 'N/A')}")
    lines.append("")

    lines.append(labels["master_lens"])
    lines.append("")
    lines.append(f"| {labels['master']} | {labels['lens_rationale']} | {labels['lens_influence']} |")
    lines.append("|---|---|---|")
    if master_lenses:
        for item in master_lenses:
            if isinstance(item, str):
                lines.append(f"| {item} | N/A | N/A |")
            else:
                master = item.get("master", item.get("name", "N/A"))
                rationale = item.get("rationale", item.get("why_used", "N/A"))
                influence = item.get("influence", item.get("impact", "N/A"))
                lines.append(f"| {master} | {rationale} | {influence} |")
    else:
        lines.append("| N/A | No master lens was explicitly selected. | Treat as low-confidence output discipline issue. |")
    if downgraded_lenses:
        lines.append("")
        lines.append(f"**{labels['downgraded_lenses']}:**")
        for item in downgraded_lenses:
            if isinstance(item, str):
                lines.append(f"- {item}")
            else:
                name = item.get("master", item.get("name", "N/A"))
                reason = item.get("reason", item.get("rationale", "N/A"))
                lines.append(f"- {name}: {reason}")
    lines.append("")

    lines.append(labels["thesis"])
    lines.append("")
    lines.append(labels["bull"])
    lines.append(_list(thesis.get("bull_case", [])))
    lines.append("")
    lines.append(labels["bear"])
    lines.append(_list(thesis.get("bear_case", [])))
    lines.append("")

    lines.append(labels["evidence"])
    lines.append("")
    if evidence:
        for item in evidence:
            lines.append(f"- {labels['fact']}: {item.get('fact', 'N/A')}")
            lines.append(f"  - {labels['interpretation']}: {item.get('interpretation', 'N/A')}")
            lines.append(f"  - {labels['implication']}: {item.get('investment_implication', 'N/A')}")
    else:
        lines.append(f"- {labels['fact']}: N/A")
    lines.append("")

    lines.append(labels["valuation"])
    lines.append("")
    selected = valuation.get("selected_models", valuation.get("primary_model", "N/A"))
    if isinstance(selected, list):
        selected = ", ".join(selected)
    lines.append(f"| {labels['item']} | {labels['result']} | {labels['interpretation']} |")
    lines.append("|---|---:|---|")
    rows = [
        (labels["selected_models"], selected, "Model stack selected by company type"),
        (labels["bear_value"], valuation.get("bear_value", "Blocked"), "Conservative intrinsic value estimate"),
        (labels["base_value"], valuation.get("base_value", "Blocked"), "Base-case intrinsic value estimate"),
        (labels["bull_value"], valuation.get("bull_value", "Blocked"), "Upside-case intrinsic value estimate"),
        (labels["current_price"], valuation.get("current_price", "Blocked"), "Latest available market reference"),
        (labels["mos"], valuation.get("margin_of_safety", "Blocked"), "Price vs base intrinsic value"),
        (labels["valuation_status"], valuation.get("valuation_status", valuation.get("status", "Blocked")), "Overall valuation judgment"),
    ]
    for name, result, interpretation in rows:
        lines.append(f"| {name} | {result} | {interpretation} |")
    lines.append("")
    lines.append(f"**{labels['key_assumptions']}:**")
    lines.append(_list(valuation.get("key_assumptions", [])))

    assumption_confidence = valuation.get("assumption_confidence")
    if assumption_confidence:
        lines.append("")
        lines.append(f"**{labels['assumption_confidence']}:** {assumption_confidence}")

    structured_assumptions = valuation.get("structured_assumptions", [])
    if structured_assumptions:
        lines.append("")
        lines.append(f"**{labels['structured_assumptions']}:**")
        lines.append(
            f"| {labels['assumption']} | {labels['value']} | {labels['scenario']} | "
            f"{labels['confidence']} | {labels['sensitivity']} | Evidence |"
        )
        lines.append("|---|---:|---|---|---|---|")
        for item in structured_assumptions:
            evidence = item.get("evidence", [])
            if isinstance(evidence, list):
                evidence = "; ".join(map(str, evidence))
            value = item.get("value", "N/A")
            unit = item.get("unit", "")
            if unit:
                value = f"{value} {unit}"
            lines.append(
                "| {assumption} | {value} | {scenario} | {confidence} | {sensitivity} | {evidence} |".format(
                    assumption=item.get("assumption", "N/A"),
                    value=value,
                    scenario=item.get("scenario", "N/A"),
                    confidence=item.get("confidence", "N/A"),
                    sensitivity=item.get("sensitivity", "N/A"),
                    evidence=evidence or item.get("source_or_reason", "N/A"),
                )
            )

    lines.append("")
    lines.append(f"**{labels['sensitivity_summary']}:** {valuation.get('sensitivity_summary', 'N/A')}")
    blocked = valuation.get("blocked_or_low_confidence_items", [])
    if blocked:
        lines.append("")
        lines.append(f"**{labels['blocked']}:**")
        lines.append(_list(blocked))
    lines.append("")

    lines.append(labels["risks"])
    lines.append("")
    risks = payload.get("risks", payload.get("risk_analysis", {}).get("top_risks", []))
    lines.append(_list(risks))
    lines.append("")

    lines.append(labels["gates"])
    lines.append("")
    lines.append(f"| {labels['gate']} | {labels['status']} | {labels['comment']} |")
    lines.append("|---|---|---|")
    lines.append(_table_rows(gates, ["gate", "status", "comment"]))
    lines.append("")

    lines.append(labels["action"])
    lines.append("")
    lines.append(labels["price_zones"])
    lines.append("")
    lines.append(f"| {labels['zone']} | {labels['price_range']} | {labels['interpretation']} |")
    lines.append("|---|---:|---|")
    lines.append(_table_rows(action.get("price_zones", []), ["zone", "price_range", "interpretation"]))
    lines.append("")
    lines.append(labels["position"])
    lines.append("")
    lines.append(f"| {labels['investor_type']} | {labels['suggested_action']} | {labels['rationale']} |")
    lines.append("|---|---|---|")
    lines.append(_table_rows(action.get("position_aware_suggestions", []), ["investor_type", "suggested_action", "rationale"]))
    lines.append("")

    tp = action.get("tranche_plan", {})
    lines.append(labels["tranche"])
    lines.append("")
    lines.append(f"- {labels['starter']}: {tp.get('starter_range', 'Blocked')}")
    lines.append(f"- {labels['add']}: {tp.get('add_range', 'Blocked')}")
    lines.append(f"- {labels['strong_add']}: {tp.get('strong_add_range', 'Blocked')}")
    lines.append(f"- {labels['hold']}: {tp.get('hold_range', 'Blocked')}")
    lines.append(f"- {labels['trim']}: {tp.get('trim_range', 'Blocked')}")
    lines.append(f"- {labels['exit']}: {tp.get('exit_review_range', 'Blocked')}")
    lines.append("")

    kc = action.get("key_conditions", {})
    lines.append(labels["conditions"])
    lines.append("")
    lines.append(f"- {labels['add_if']}: {kc.get('add_only_if', 'N/A')}")
    lines.append(f"- {labels['hold_if']}: {kc.get('hold_only_if', 'N/A')}")
    lines.append(f"- {labels['trim_if']}: {kc.get('trim_if', 'N/A')}")
    lines.append(f"- {labels['exit_if']}: {kc.get('exit_or_avoid_if', 'N/A')}")
    lines.append("")

    lines.append(labels["provenance"])
    lines.append("")
    lines.append(f"**{labels['data_confidence']}:** {provenance.get('data_confidence', 'N/A')}  ")
    lines.append(f"**{labels['analysis_as_of']}:** {provenance.get('analysis_as_of', 'N/A')}  ")
    lines.append(f"**{labels['market_as_of']}:** {provenance.get('market_data_as_of', 'N/A')}  ")
    lines.append(f"**{labels['latest_period']}:** {provenance.get('latest_financial_period', 'N/A')}  ")
    missing = provenance.get("missing_data", [])
    lines.append(f"**{labels['missing']}:** {', '.join(missing) if missing else labels['none']}")

    return "\n".join(lines)


def validate_report(markdown: str) -> List[str]:
    """Return validation problems. Empty list means pass."""

    errors: List[str] = []
    matching_sections = None
    for sections in REQUIRED_SECTIONS_BY_LANGUAGE.values():
        if any(section in markdown for section in sections):
            matching_sections = sections
            break
    if matching_sections is None:
        matching_sections = REQUIRED_SECTIONS_BY_LANGUAGE["en"]

    position = -1
    for section in matching_sections:
        new_position = markdown.find(section)
        if new_position < 0:
            errors.append(f"Missing required section: {section}")
        elif new_position < position:
            errors.append(f"Section out of order: {section}")
        else:
            position = new_position

    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in markdown.lower():
            errors.append(f"Forbidden content detected: {phrase}")

    required_terms = [
        "Bear value",
        "Base value",
        "Bull value",
        "Margin of safety",
        "Price Zones",
        "Position-Aware Suggestions",
        "Tranche Plan",
        "Master Lens Used",
    ]
    chinese_terms = ["悲观价值", "基准价值", "乐观价值", "安全边际", "价格区间", "按持仓状态的建议", "分批计划", "大师框架"]
    if any(term in markdown for term in chinese_terms):
        required_terms = chinese_terms
    for term in required_terms:
        if term not in markdown:
            errors.append(f"Missing required field/group: {term}")
    return errors


# Backward-compatible alias.
def generate_report(data: Dict[str, Any]) -> str:
    return render_report(data)


if __name__ == "__main__":
    sample = {
        "target_name": "Sample Company",
        "output_language": "en",
        "executive_conclusion": {
            "rating": "Watchlist",
            "style_classification": "Mature Quality Compounder",
            "one_line_judgment": "Good company, but price discipline is required.",
            "key_reasons": ["Business quality is solid", "Valuation requires margin of safety", "Wait for entry zone"],
            "bottom_line": "Watchlist until price reaches a more attractive zone.",
        },
        "valuation_summary": {
            "selected_models": ["Owner Earnings DCF", "EPV", "Reverse DCF"],
            "bear_value": "80",
            "base_value": "100",
            "bull_value": "120",
            "current_price": "95",
            "margin_of_safety": "5%",
            "valuation_status": "fair",
            "key_assumptions": ["Stable FCF conversion", "Moderate growth"],
            "sensitivity_summary": "Most sensitive to margin and terminal growth.",
        },
        "master_lens_used": [
            {
                "master": "Buffett / Munger",
                "rationale": "Mature cash-flow compounder with moat and capital allocation questions.",
                "influence": "Prioritize owner earnings, moat durability, management integrity, and margin of safety.",
            }
        ],
        "investor_action_framework": {
            "price_zones": [
                {"zone": "Deep Value", "price_range": "<=56", "interpretation": "High MOS"},
                {"zone": "Accumulation", "price_range": "56-85", "interpretation": "Attractive"},
                {"zone": "Watchlist", "price_range": "85-100", "interpretation": "Monitor"},
                {"zone": "Fair Value", "price_range": "100-132", "interpretation": "Limited upside"},
                {"zone": "Trim", "price_range": "132-156", "interpretation": "Valuation risk"},
                {"zone": "Sell / Avoid", "price_range": ">156", "interpretation": "Expectations high"},
            ],
            "position_aware_suggestions": [
                {"investor_type": "Empty Position", "suggested_action": "Wait or starter only if thesis is strong.", "rationale": "Limited MOS"},
                {"investor_type": "Half Position", "suggested_action": "Hold.", "rationale": "Fair valuation"},
                {"investor_type": "Full Position", "suggested_action": "Hold / reassess.", "rationale": "Opportunity cost"},
                {"investor_type": "Overweight Position", "suggested_action": "Trim if risk rises.", "rationale": "Concentration"},
            ],
            "tranche_plan": {
                "starter_range": "85-100",
                "add_range": "56-85",
                "strong_add_range": "<=56",
                "hold_range": "85-132",
                "trim_range": "132-156",
                "exit_review_range": ">156",
            },
            "key_conditions": {
                "add_only_if": "Thesis remains intact.",
                "hold_only_if": "FCF quality remains stable.",
                "trim_if": "Valuation exceeds bull case.",
                "exit_or_avoid_if": "Thesis breaks.",
            },
        },
    }
    report = render_report(sample)
    errors = validate_report(report)
    if errors:
        raise SystemExit(errors)
    out = Path("outputs/markdown/sample_report.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
