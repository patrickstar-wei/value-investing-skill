"""Output validator .

Checks that user-facing reports preserve the fixed investment framework,
including valuation range and position-aware action guidance.
"""

from __future__ import annotations

from typing import List


REQUIRED_SECTIONS = [
    "## 📌 Executive Conclusion",
    "## 🧭 Decision Snapshot",
    "## 🧭 Company Classification",
    "## Master Lens Used",
    "## 🔹 Core Thesis",
    "## 📊 Key Evidence",
    "## 🧮 Valuation Summary",
    "## ⚠️ Key Risks",
    "## ✅ / ❌ Execution Gate Checklist",
    "## 🧭 Investor Action Framework",
    "## 🔍 Data Provenance",
]

REQUIRED_TERMS = [
    "Bear value",
    "Base value",
    "Bull value",
    "Current price",
    "Margin of safety",
    "Conclusion change triggers",
    "Master Lens Used",
    "Price Zones",
    "Price Zone Assumption Basis",
    "Position-Aware Suggestions",
    "Tranche Plan",
    "Empty Position",
    "Half Position",
    "Full Position",
    "Overweight Position",
    "Starter",
    "Trim",
    "Exit",
    "Public data sources used / checked",
    "Optional user-provided data",
]

FORBIDDEN_DEFAULT_TERMS = [
    "year-by-year DCF",
    "discounting schedule",
    "formula derivation",
    "internal routing score",
    "internal quality-gate score",
    "debug trace",
]


def validate_fixed_output(markdown: str) -> List[str]:
    errors: List[str] = []
    previous = -1
    for section in REQUIRED_SECTIONS:
        pos = markdown.find(section)
        if pos < 0:
            errors.append(f"Missing section: {section}")
        elif pos < previous:
            errors.append(f"Section out of order: {section}")
        previous = max(previous, pos)

    lower = markdown.lower()
    for term in REQUIRED_TERMS:
        if term.lower() not in lower:
            errors.append(f"Missing required valuation/action field: {term}")

    for term in FORBIDDEN_DEFAULT_TERMS:
        if term.lower() in lower:
            errors.append(f"Forbidden default content: {term}")

    return errors
