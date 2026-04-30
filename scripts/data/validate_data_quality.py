"""Validate data quality and assign confidence scores."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class DataPoint:
    metric: str
    value: Any
    period: Optional[str]
    source: Optional[str]
    source_tier: Optional[int]
    last_updated: Optional[str]


def confidence_score(data: DataPoint) -> float:
    score = 0.0

    if data.value is not None:
        score += 0.35

    if data.period:
        score += 0.15

    if data.source_tier is not None:
        if data.source_tier == 1:
            score += 0.35
        elif data.source_tier == 2:
            score += 0.30
        elif data.source_tier == 3:
            score += 0.22
        elif data.source_tier == 4:
            score += 0.12
        else:
            score += 0.05

    if data.last_updated:
        score += 0.15

    return min(score, 1.0)


def requires_review(data: DataPoint, threshold: float = 0.7) -> bool:
    return confidence_score(data) < threshold


if __name__ == "__main__":
    dp = DataPoint(
        metric="Revenue",
        value=383_285_000_000,
        period="FY2023",
        source="10-K",
        source_tier=2,
        last_updated="2024-02-01",
    )
    print(confidence_score(dp))
