"""A-share accounting correction / restatement detection helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List


RESTATEMENT_KEYWORDS = (
    "会计差错更正",
    "前期差错更正",
    "追溯调整",
    "更正后",
    "调整后",
)


@dataclass
class CNARestatementEvent:
    announcement_date: str
    title: str
    source_url: str = ""
    periods_affected: List[str] = field(default_factory=list)
    financial_impact: Dict[str, Any] = field(default_factory=dict)
    adjusted_figures_available: bool = False


def detect_restatements_from_announcements(announcements: Iterable[Dict[str, Any]]) -> List[CNARestatementEvent]:
    """Detect restatement-like A-share announcements from parsed metadata/text."""

    events: List[CNARestatementEvent] = []
    for item in announcements:
        title = str(item.get("title") or "")
        text = str(item.get("text") or "")
        haystack = title + "\n" + text
        if not any(keyword in haystack for keyword in RESTATEMENT_KEYWORDS):
            continue
        events.append(
            CNARestatementEvent(
                announcement_date=str(item.get("announcement_date") or item.get("date") or ""),
                title=title,
                source_url=str(item.get("source_url") or item.get("url") or ""),
                periods_affected=list(item.get("periods_affected", [])),
                financial_impact=dict(item.get("financial_impact", {})),
                adjusted_figures_available=bool(item.get("adjusted_figures_available")),
            )
        )
    return events


def restatement_status_for_ttm(events: Iterable[CNARestatementEvent], ttm_periods: Iterable[str]) -> str:
    """Classify whether detected restatements affect the TTM window."""

    ttm_period_set = {period for period in ttm_periods if period}
    affected = False
    adjusted = False
    for event in events:
        if not event.periods_affected:
            affected = True
        elif ttm_period_set.intersection(event.periods_affected):
            affected = True
        adjusted = adjusted or event.adjusted_figures_available
    if not affected:
        return "not_affected"
    return "adjusted" if adjusted else "affected_not_adjusted"
