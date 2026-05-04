"""Investor action framework helpers.

This module converts intrinsic value ranges into price zones and
position-aware action suggestions.
"""

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class IntrinsicValueRange:
    low: float
    mid: float
    high: float


@dataclass
class PriceZones:
    deep_value: Tuple[float, float]
    accumulation: Tuple[float, float]
    watchlist: Tuple[float, float]
    fair_value: Tuple[float, float]
    trim: Tuple[float, float]
    sell_avoid: Tuple[float, float]


def build_price_zones(iv: IntrinsicValueRange) -> Dict[str, Tuple[float, float | None]]:
    """Build default price zones from intrinsic value range."""
    return {
        "Deep Value": (0.0, 0.70 * iv.low),
        "Accumulation": (0.70 * iv.low, 0.85 * iv.mid),
        "Watchlist": (0.85 * iv.mid, 1.00 * iv.mid),
        "Fair Value": (1.00 * iv.mid, 1.10 * iv.high),
        "Trim": (1.10 * iv.high, 1.30 * iv.high),
        "Sell / Avoid": (1.30 * iv.high, None),
    }


def price_zone_assumption_basis(iv: IntrinsicValueRange) -> list[str]:
    """Explain the default assumptions behind generated price zones."""
    return [
        f"Price zones are anchored to IV_low={iv.low}, IV_mid={iv.mid}, and IV_high={iv.high}.",
        "Default thresholds use 70% of IV_low, 85%-100% of IV_mid, and 110%-130% of IV_high.",
        "Zones depend most on the assumptions that set the bear/base/bull intrinsic value range.",
        "If high-sensitivity assumptions change materially, update intrinsic values before using the action zones.",
    ]


def classify_price(current_price: float, iv: IntrinsicValueRange) -> str:
    zones = build_price_zones(iv)
    for zone, (low, high) in zones.items():
        if high is None:
            if current_price > low:
                return zone
        elif low < current_price <= high:
            return zone
        elif zone == "Deep Value" and current_price <= high:
            return zone
    return "Unclassified"


def position_action(position_type: str, price_zone: str) -> str:
    matrix = {
        "empty": {
            "Deep Value": "Consider building a position in tranches if thesis is intact.",
            "Accumulation": "Consider starter position or gradual accumulation.",
            "Watchlist": "Watchlist; wait for better entry or stronger evidence.",
            "Fair Value": "Usually wait unless quality is exceptional.",
            "Trim": "Avoid new position; valuation risk rising.",
            "Sell / Avoid": "Avoid; expectations likely too high.",
        },
        "half": {
            "Deep Value": "Consider adding if thesis remains intact.",
            "Accumulation": "Consider adding gradually.",
            "Watchlist": "Hold and monitor.",
            "Fair Value": "Hold; avoid aggressive adding.",
            "Trim": "Consider trimming if position risk is high.",
            "Sell / Avoid": "Consider reducing if valuation risk dominates.",
        },
        "full": {
            "Deep Value": "Hold; add only if risk budget allows.",
            "Accumulation": "Hold; avoid concentration risk.",
            "Watchlist": "Hold.",
            "Fair Value": "Hold; reassess opportunity cost.",
            "Trim": "Consider trimming to target allocation.",
            "Sell / Avoid": "Consider partial exit or rebalance.",
        },
        "overweight": {
            "Deep Value": "Hold only if risk budget allows.",
            "Accumulation": "Hold or rebalance risk.",
            "Watchlist": "Reduce concentration if needed.",
            "Fair Value": "Trim toward target allocation.",
            "Trim": "Trim or rebalance.",
            "Sell / Avoid": "Strongly consider reducing exposure.",
        },
    }
    return matrix[position_type][price_zone]


def margin_of_safety(current_price: float, intrinsic_mid: float) -> float:
    return (intrinsic_mid - current_price) / intrinsic_mid
