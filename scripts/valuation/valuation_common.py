"""Common valuation result structures and validation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class StructuredAssumption:
    """Auditable assumption used by valuation models."""

    assumption: str
    value: Any
    unit: str = ""
    scenario: str = "single"
    evidence: List[str] = field(default_factory=list)
    confidence: str = "medium"
    sensitivity: str = "medium"
    source_or_reason: str = ""


@dataclass
class ValuationResult:
    """Standard output envelope for valuation models."""

    model_name: str
    bear_value: Optional[float] = None
    base_value: Optional[float] = None
    bull_value: Optional[float] = None
    per_share_bear: Optional[float] = None
    per_share_base: Optional[float] = None
    per_share_bull: Optional[float] = None
    key_assumptions: List[str] = field(default_factory=list)
    structured_assumptions: List[StructuredAssumption] = field(default_factory=list)
    assumption_confidence: str = "medium"
    sensitivity: Dict[str, Any] = field(default_factory=dict)
    blocked: bool = False
    blocked_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        """Convert result to the report payload valuation_summary shape."""

        return {
            "selected_models": [self.model_name],
            "bear_value": "Blocked" if self.blocked else self.bear_value,
            "base_value": "Blocked" if self.blocked else self.base_value,
            "bull_value": "Blocked" if self.blocked else self.bull_value,
            "margin_of_safety": self.metadata.get("margin_of_safety", "Blocked"),
            "valuation_status": "blocked" if self.blocked else self.metadata.get("valuation_status", "low-confidence"),
            "key_assumptions": self.key_assumptions,
            "structured_assumptions": [
                assumption if isinstance(assumption, dict) else assumption.__dict__
                for assumption in self.structured_assumptions
            ],
            "assumption_confidence": "blocked" if self.blocked else self.assumption_confidence,
            "sensitivity_summary": self.metadata.get("sensitivity_summary", "N/A"),
            "blocked_or_low_confidence_items": [self.blocked_reason] if self.blocked_reason else [],
        }


def require_positive(value: float, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


def require_non_negative(value: float, name: str) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def require_rate_order(discount_rate: float, terminal_growth: float) -> None:
    if discount_rate <= terminal_growth:
        raise ValueError("discount_rate must be greater than terminal_growth")


def per_share(value: float, shares_outstanding: float) -> float:
    require_positive(shares_outstanding, "shares_outstanding")
    return value / shares_outstanding


def equity_value_from_enterprise_value(
    enterprise_value: float,
    net_debt: float = 0.0,
    minority_interest: float = 0.0,
    non_operating_assets: float = 0.0,
) -> float:
    return enterprise_value - net_debt - minority_interest + non_operating_assets
