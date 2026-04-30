"""Data provenance utilities for investment analysis."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, List, Optional, Dict
import json
from pathlib import Path


@dataclass
class DataPoint:
    data_id: str
    metric: str
    value: Any
    unit: str
    period: str
    company: Optional[str]
    ticker: Optional[str]
    source_name: str
    source_type: str
    source_url: Optional[str]
    source_path: Optional[str]
    source_date: str
    extraction_timestamp: str
    page_or_table: Optional[str]
    source_tier: int
    freshness_status: str
    confidence: float
    raw_or_derived: str
    formula: Optional[str] = None
    input_data_ids: Optional[List[str]] = None
    notes: Optional[str] = None


def make_raw_data_point(
    data_id: str,
    metric: str,
    value: Any,
    unit: str,
    period: str,
    source_name: str,
    source_type: str,
    source_date: str,
    source_tier: int,
    confidence: float,
    company: Optional[str] = None,
    ticker: Optional[str] = None,
    source_url: Optional[str] = None,
    source_path: Optional[str] = None,
    page_or_table: Optional[str] = None,
    freshness_status: str = "Unknown",
    notes: Optional[str] = None,
) -> DataPoint:
    return DataPoint(
        data_id=data_id,
        metric=metric,
        value=value,
        unit=unit,
        period=period,
        company=company,
        ticker=ticker,
        source_name=source_name,
        source_type=source_type,
        source_url=source_url,
        source_path=source_path,
        source_date=source_date,
        extraction_timestamp=datetime.now().isoformat(timespec="seconds"),
        page_or_table=page_or_table,
        source_tier=source_tier,
        freshness_status=freshness_status,
        confidence=confidence,
        raw_or_derived="raw",
        notes=notes,
    )


def make_derived_data_point(
    data_id: str,
    metric: str,
    value: Any,
    unit: str,
    period: str,
    formula: str,
    input_data_ids: List[str],
    confidence: float,
    company: Optional[str] = None,
    ticker: Optional[str] = None,
    notes: Optional[str] = None,
) -> DataPoint:
    return DataPoint(
        data_id=data_id,
        metric=metric,
        value=value,
        unit=unit,
        period=period,
        company=company,
        ticker=ticker,
        source_name="Derived from sourced inputs",
        source_type="Derived metric",
        source_url=None,
        source_path=None,
        source_date="Derived",
        extraction_timestamp=datetime.now().isoformat(timespec="seconds"),
        page_or_table=None,
        source_tier=0,
        freshness_status="Derived",
        confidence=confidence,
        raw_or_derived="derived",
        formula=formula,
        input_data_ids=input_data_ids,
        notes=notes,
    )


def save_data_lineage(data_points: List[DataPoint], path: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump([asdict(dp) for dp in data_points], f, indent=2, ensure_ascii=False)


def load_data_lineage(path: str) -> List[Dict[str, Any]]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def find_orphan_numbers(data_points: List[DataPoint]) -> List[str]:
    """Return data IDs that do not have enough provenance."""
    orphan_ids: List[str] = []
    for dp in data_points:
        if dp.raw_or_derived == "raw":
            if not (dp.source_name and (dp.source_url or dp.source_path) and dp.source_date):
                orphan_ids.append(dp.data_id)
        elif dp.raw_or_derived == "derived":
            if not (dp.formula and dp.input_data_ids):
                orphan_ids.append(dp.data_id)
        elif dp.raw_or_derived in {"assumption", "user_input"}:
            # Allowed, but should be clearly labeled.
            continue
        else:
            orphan_ids.append(dp.data_id)
    return orphan_ids


def confidence_floor_check(data_points: List[DataPoint], floor: float = 0.7) -> List[str]:
    return [dp.data_id for dp in data_points if dp.confidence < floor]
