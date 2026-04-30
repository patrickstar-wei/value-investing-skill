"""Sensitivity table generation."""

from typing import Dict, List


def build_sensitivity_grid(
    base_value: float,
    variable_ranges: Dict[str, List[float]],
) -> Dict[str, Dict[float, float]]:
    """Simple placeholder sensitivity grid.

    Real implementation should recalculate valuation under each assumption.
    """
    result: Dict[str, Dict[float, float]] = {}
    for variable, values in variable_ranges.items():
        result[variable] = {}
        for value in values:
            # Placeholder: store base value until model-specific recalculation is implemented.
            result[variable][value] = base_value
    return result
