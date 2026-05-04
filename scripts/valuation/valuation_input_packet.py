"""Structured valuation input packet.

The packet binds model inputs to source data IDs, freshness status, and
structured assumptions so valuation execution can block weak inputs instead of
silently inventing values.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class ValuationInput:
    name: str
    value: Any
    unit: str = ""
    data_ids: List[str] = field(default_factory=list)
    assumption_ids: List[str] = field(default_factory=list)
    required: bool = True


@dataclass
class ValuationInputPacket:
    company: str
    ticker: str
    currency: str = "USD"
    analysis_as_of: Optional[str] = None
    market_data_as_of: Optional[str] = None
    latest_financial_period: Optional[str] = None
    model_inputs: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    inputs: List[ValuationInput] = field(default_factory=list)
    structured_assumptions: List[Dict[str, Any]] = field(default_factory=list)
    data_points: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ValuationInputPacket":
        inputs = [
            item if isinstance(item, ValuationInput) else ValuationInput(**item)
            for item in data.get("inputs", [])
        ]
        return cls(
            company=data.get("company", ""),
            ticker=data.get("ticker", ""),
            currency=data.get("currency", "USD"),
            analysis_as_of=data.get("analysis_as_of"),
            market_data_as_of=data.get("market_data_as_of"),
            latest_financial_period=data.get("latest_financial_period"),
            model_inputs=data.get("model_inputs", {}),
            inputs=inputs,
            structured_assumptions=data.get("structured_assumptions", []),
            data_points=data.get("data_points", []),
        )

    def get_model_inputs(self, model_key: str) -> Dict[str, Any]:
        return dict(self.model_inputs.get(model_key, {}))

    def bound_data_ids(self) -> set[str]:
        ids: set[str] = set()
        for item in self.inputs:
            ids.update(item.data_ids)
        for model_input in self.model_inputs.values():
            for value in model_input.values():
                if isinstance(value, dict):
                    ids.update(value.get("data_ids", []))
        return ids

    def missing_required_bindings(self) -> List[str]:
        missing = []
        for item in self.inputs:
            if item.required and not item.data_ids and not item.assumption_ids:
                missing.append(item.name)
        return missing


def unwrap_input(value: Any) -> Any:
    """Allow model inputs to be passed as raw values or bound input objects."""

    if isinstance(value, dict) and "value" in value:
        return value["value"]
    return value

