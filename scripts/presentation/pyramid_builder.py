"""Build pyramid-principle summaries from structured investment reports."""

from typing import Any, Dict, List


def signal(value: str) -> str:
    mapping = {
        "positive": "✅",
        "pass": "✅",
        "passed": "✅",
        "neutral": "⚠️",
        "warning": "⚠️",
        "risk": "⚠️",
        "negative": "❌",
        "fail": "❌",
        "blocked": "❌",
        "action": "➡️",
    }
    return mapping.get(str(value).lower(), "⚠️")


def compact_pyramid(report: Dict[str, Any]) -> str:
    """Return user-facing pyramid summary without exposing calculation traces."""
    final_view = report.get("final_view", {})
    valuation = report.get("valuation_results", {})
    risks = report.get("risk_analysis", {})

    lines: List[str] = []
    lines.append("## 📌 Executive Conclusion")
    lines.append("")
    lines.append(f"**Rating:** {final_view.get('rating', 'N/A')}")
    lines.append(f"**One-line Judgment:** {final_view.get('one_line_judgment', 'N/A')}")
    lines.append("")
    lines.append("### Why this conclusion?")
    for item in final_view.get("key_reasons", []):
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## 🧮 Valuation Summary")
    lines.append(f"- Primary model: {valuation.get('primary_model', 'N/A')}")
    lines.append(f"- Bear / base / bull value: {valuation.get('bear_value', 'N/A')} / {valuation.get('base_value', 'N/A')} / {valuation.get('bull_value', 'N/A')}")
    lines.append(f"- Current price: {valuation.get('current_price', 'N/A')}")
    lines.append(f"- Margin of safety: {valuation.get('margin_of_safety', 'N/A')}")
    if valuation.get('key_assumptions'):
        lines.append(f"- Key assumptions: {'; '.join(map(str, valuation.get('key_assumptions', [])))}")
    if valuation.get('sensitivity_summary'):
        lines.append(f"- Sensitivity: {valuation.get('sensitivity_summary')}")
    if valuation.get('status'):
        lines.append(f"- Valuation status: {valuation.get('status')}")
    lines.append("")
    lines.append("## ⚠️ Key Risks")
    for item in risks.get("top_risks", []):
        lines.append(f"- ⚠️ {item}")
    return "\n".join(lines)


def decision_snapshot(rows: List[Dict[str, str]]) -> str:
    lines = [
        "## 🧭 Decision Snapshot",
        "",
        "| Dimension | Judgment | Signal |",
        "|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('dimension', '')} | {row.get('judgment', '')} | {row.get('signal', '')} |"
        )
    return "\n".join(lines)
