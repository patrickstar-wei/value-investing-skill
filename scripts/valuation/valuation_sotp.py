"""Sum-of-the-parts valuation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from scripts.valuation.valuation_common import equity_value_from_enterprise_value, per_share, require_non_negative


@dataclass(frozen=True)
class SegmentInput:
    name: str
    metric: Optional[float] = None
    multiple: Optional[float] = None
    explicit_value: Optional[float] = None
    ownership: float = 1.0


def segment_value(segment: SegmentInput) -> float:
    if segment.explicit_value is not None:
        value = segment.explicit_value
    else:
        if segment.metric is None or segment.multiple is None:
            raise ValueError(f"segment {segment.name} requires metric and multiple or explicit_value")
        value = segment.metric * segment.multiple
    require_non_negative(segment.ownership, f"{segment.name}.ownership")
    return value * segment.ownership


def enterprise_value_from_segments(
    segments: Iterable[SegmentInput],
    corporate_cost_value: float = 0.0,
    holding_company_discount: float = 0.0,
) -> float:
    if not 0 <= holding_company_discount < 1:
        raise ValueError("holding_company_discount must be between 0 and 1")

    gross_value = sum(segment_value(segment) for segment in segments) - corporate_cost_value
    return gross_value * (1 - holding_company_discount)


def sotp_equity_value(
    segments: Iterable[SegmentInput],
    net_debt: float = 0.0,
    minority_interest: float = 0.0,
    non_operating_assets: float = 0.0,
    corporate_cost_value: float = 0.0,
    holding_company_discount: float = 0.0,
) -> float:
    enterprise_value = enterprise_value_from_segments(
        segments=segments,
        corporate_cost_value=corporate_cost_value,
        holding_company_discount=holding_company_discount,
    )
    return equity_value_from_enterprise_value(
        enterprise_value=enterprise_value,
        net_debt=net_debt,
        minority_interest=minority_interest,
        non_operating_assets=non_operating_assets,
    )


def sotp_value_per_share(equity_value: float, shares_outstanding: float) -> float:
    return per_share(equity_value, shares_outstanding)

