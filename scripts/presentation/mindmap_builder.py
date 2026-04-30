"""Helpers for building mind-map-like outputs from structured report data."""

from typing import Any, Dict, List


def nested_bullet(report: Dict[str, Any], root_name: str) -> str:
    lines: List[str] = [f"- {root_name}"]

    def add_branch(title: str, items: List[str], indent: int = 1):
        lines.append("  " * indent + f"- {title}")
        for item in items:
            lines.append("  " * (indent + 1) + f"- {item}")

    final_view = report.get("final_view", {})
    add_branch("Final View", [
        f"Rating: {final_view.get('rating', 'N/A')}",
        f"Business quality: {final_view.get('business_quality', 'N/A')}",
        f"Valuation: {final_view.get('valuation_attractiveness', 'N/A')}",
        f"Risk: {final_view.get('risk_level', 'N/A')}",
    ])

    return "\n".join(lines)


def ascii_tree(root: str, branches: Dict[str, List[str]]) -> str:
    lines: List[str] = [root]
    branch_items = list(branches.items())

    for i, (title, leaves) in enumerate(branch_items):
        last_branch = i == len(branch_items) - 1
        prefix = "└─ " if last_branch else "├─ "
        lines.append(prefix + title)

        for j, leaf in enumerate(leaves):
            is_last_leaf = j == len(leaves) - 1
            child_prefix = "   " if last_branch else "│  "
            leaf_prefix = "└─ " if is_last_leaf else "├─ "
            lines.append(child_prefix + leaf_prefix + leaf)

    return "\n".join(lines)


def mermaid_mindmap(root: str, branches: Dict[str, List[str]]) -> str:
    lines = ["```mermaid", "mindmap", f"  root(({root}))"]
    for title, leaves in branches.items():
        lines.append(f"    {title}")
        for leaf in leaves:
            lines.append(f"      {leaf}")
    lines.append("```")
    return "\n".join(lines)
