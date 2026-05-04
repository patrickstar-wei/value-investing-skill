"""Scenario-weighted valuation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from scripts.valuation.valuation_common import require_rate_order


@dataclass(frozen=True)
class Scenario:
    name: str
    value: float
    probability: float


def probability_weighted_value(scenarios: Iterable[Scenario]) -> float:
    scenarios_list = list(scenarios)
    if not scenarios_list:
        raise ValueError("scenarios must not be empty")

    total_probability = sum(scenario.probability for scenario in scenarios_list)
    if abs(total_probability - 1.0) > 1e-6:
        raise ValueError("scenario probabilities must sum to 1")
    if any(scenario.probability < 0 for scenario in scenarios_list):
        raise ValueError("scenario probabilities must be non-negative")
    return sum(scenario.value * scenario.probability for scenario in scenarios_list)


def dcf_from_cash_flows(
    cash_flows: List[float],
    discount_rate: float,
    terminal_growth: float | None = None,
) -> float:
    if discount_rate <= -1:
        raise ValueError("discount_rate must be greater than -100%")
    present_value = sum(cf / ((1 + discount_rate) ** (i + 1)) for i, cf in enumerate(cash_flows))
    if terminal_growth is None:
        return present_value

    require_rate_order(discount_rate, terminal_growth)
    terminal_value = cash_flows[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    return present_value + terminal_value / ((1 + discount_rate) ** len(cash_flows))


def scenario_weighted_dcf(scenarios: Iterable[Scenario]) -> float:
    return probability_weighted_value(scenarios)

