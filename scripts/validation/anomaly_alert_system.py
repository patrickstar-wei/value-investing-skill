"""Small anomaly checks for valuation metrics."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Iterable, List


@dataclass
class AnomalyAlert:
    metric: str
    severity: str
    message: str
    value: float


def zscore_alert(metric: str, value: float, history: Iterable[float], threshold: float = 2.0) -> List[AnomalyAlert]:
    values = [float(item) for item in history]
    if len(values) < 3:
        return []
    mu = mean(values)
    sigma = pstdev(values)
    if sigma == 0:
        return []
    zscore = abs(value - mu) / sigma
    if zscore <= threshold:
        return []
    severity = "HIGH" if zscore > threshold * 1.5 else "MEDIUM"
    return [
        AnomalyAlert(
            metric=metric,
            severity=severity,
            message=f"{metric} value {value} is {zscore:.2f} standard deviations from history.",
            value=value,
        )
    ]


def range_alert(metric: str, value: float, lower: float | None = None, upper: float | None = None) -> List[AnomalyAlert]:
    if lower is not None and value < lower:
        return [AnomalyAlert(metric=metric, severity="HIGH", message=f"{metric} is below lower bound {lower}.", value=value)]
    if upper is not None and value > upper:
        return [AnomalyAlert(metric=metric, severity="HIGH", message=f"{metric} is above upper bound {upper}.", value=value)]
    return []
