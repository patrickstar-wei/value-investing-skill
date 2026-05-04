"""Liquidation value analysis."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from scripts.valuation.valuation_common import per_share, require_non_negative


@dataclass(frozen=True)
class AssetRecovery:
    name: str
    carrying_value: float
    recovery_rate: float


@dataclass(frozen=True)
class LiabilityClaim:
    name: str
    claim_value: float
    settlement_rate: float = 1.0


def recoverable_asset_value(asset: AssetRecovery) -> float:
    require_non_negative(asset.carrying_value, f"{asset.name}.carrying_value")
    if not 0 <= asset.recovery_rate <= 1.5:
        raise ValueError(f"{asset.name}.recovery_rate must be between 0 and 1.5")
    return asset.carrying_value * asset.recovery_rate


def settled_liability_value(liability: LiabilityClaim) -> float:
    require_non_negative(liability.claim_value, f"{liability.name}.claim_value")
    if not 0 <= liability.settlement_rate <= 1.5:
        raise ValueError(f"{liability.name}.settlement_rate must be between 0 and 1.5")
    return liability.claim_value * liability.settlement_rate


def liquidation_equity_value(
    assets: Iterable[AssetRecovery],
    liabilities: Iterable[LiabilityClaim],
    liquidation_costs: float = 0.0,
) -> float:
    require_non_negative(liquidation_costs, "liquidation_costs")
    recoveries = sum(recoverable_asset_value(asset) for asset in assets)
    claims = sum(settled_liability_value(liability) for liability in liabilities)
    return recoveries - claims - liquidation_costs


def liquidation_value_per_share(equity_value: float, shares_outstanding: float) -> float:
    return per_share(equity_value, shares_outstanding)

