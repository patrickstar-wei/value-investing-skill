"""Parse safe institutional-view exports into structured records.

This parser intentionally handles structured JSON/CSV files and short user
notes. It does not scrape paywalled pages and does not extract long report
text from paid PDFs.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List


ALLOWED_SOURCE_TYPES = {"public_summary", "user_provided_export", "licensed_api", "user_notes", "unknown"}
ALLOWED_LICENSE_SCOPES = {"public", "user_subscription", "internal", "restricted", "unknown"}
BLOCKED_LICENSE_SCOPES = {"restricted", "unknown"}
STRUCTURED_SUFFIXES = {".json", ".csv"}
REFERENCE_ONLY_SUFFIXES = {".pdf", ".xlsx", ".xls", ".docx", ".txt", ".md"}


@dataclass
class InstitutionalView:
    provider: str
    ticker: str
    as_of_date: str
    source_type: str
    license_scope: str
    source_confidence: str
    institution: str = ""
    company: str = ""
    source_path_or_url: str = ""
    copyright_handling: str = "summarize_only"
    rating: str = ""
    target_price: float | None = None
    currency: str = ""
    model_used: str = ""
    forecast_fields: Dict[str, Any] = field(default_factory=dict)
    key_assumptions: List[str] = field(default_factory=list)
    bull_case: List[str] = field(default_factory=list)
    bear_case: List[str] = field(default_factory=list)
    difference_vs_our_view: List[str] = field(default_factory=list)
    missing_data: List[str] = field(default_factory=list)
    notes: str = ""


def _split_list(value: Any) -> List[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(";") if item.strip()]


def normalize_view(raw: Dict[str, Any]) -> InstitutionalView:
    source_type = raw.get("source_type", "unknown")
    license_scope = raw.get("license_scope", "unknown")
    if source_type not in ALLOWED_SOURCE_TYPES:
        source_type = "unknown"
    if license_scope not in ALLOWED_LICENSE_SCOPES:
        license_scope = "unknown"

    missing = []
    for field_name in ["provider", "ticker", "as_of_date"]:
        if not raw.get(field_name):
            missing.append(field_name)

    confidence = raw.get("source_confidence", "medium")
    copyright_handling = raw.get("copyright_handling", "summarize_only")
    if license_scope in BLOCKED_LICENSE_SCOPES:
        confidence = "blocked"
        copyright_handling = "blocked"
        missing.append("clear license_scope")

    target_price = raw.get("target_price")
    if target_price in {"", None}:
        target_price = None
    elif not isinstance(target_price, (int, float)):
        target_price = float(target_price)

    forecast_fields = raw.get("forecast_fields", {})
    if isinstance(forecast_fields, str):
        try:
            forecast_fields = json.loads(forecast_fields) if forecast_fields.strip() else {}
        except json.JSONDecodeError:
            forecast_fields = {"raw": forecast_fields}

    return InstitutionalView(
        provider=str(raw.get("provider", "")),
        institution=str(raw.get("institution", "")),
        ticker=str(raw.get("ticker", "")),
        company=str(raw.get("company", "")),
        as_of_date=str(raw.get("as_of_date", "")),
        source_type=source_type,
        source_path_or_url=str(raw.get("source_path_or_url", "")),
        license_scope=license_scope,
        copyright_handling=copyright_handling,
        rating=str(raw.get("rating", "")),
        target_price=target_price,
        currency=str(raw.get("currency", "")),
        model_used=str(raw.get("model_used", "")),
        forecast_fields=forecast_fields,
        key_assumptions=_split_list(raw.get("key_assumptions")),
        bull_case=_split_list(raw.get("bull_case")),
        bear_case=_split_list(raw.get("bear_case")),
        difference_vs_our_view=_split_list(raw.get("difference_vs_our_view")),
        source_confidence=confidence,
        missing_data=sorted(set(_split_list(raw.get("missing_data")) + missing)),
        notes=str(raw.get("notes", "")),
    )


def load_institutional_views(path: str | Path) -> List[Dict[str, Any]]:
    source = Path(path)
    suffix = source.suffix.lower()
    records: List[Dict[str, Any]]
    if suffix == ".json":
        raw = json.loads(source.read_text(encoding="utf-8"))
        records = raw if isinstance(raw, list) else [raw]
    elif suffix == ".csv":
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            records = list(csv.DictReader(handle))
    else:
        raise ValueError("Only structured .json and .csv institutional-view exports are supported by this parser.")
    return [asdict(normalize_view(record)) for record in records]


def _matches_target(record: Dict[str, Any], target: str) -> bool:
    if not target:
        return True
    needle = target.casefold()
    fields = [
        record.get("ticker", ""),
        record.get("company", ""),
        record.get("institution", ""),
        record.get("provider", ""),
        record.get("source_path_or_url", ""),
    ]
    return any(needle in str(value).casefold() for value in fields)


def discover_institutional_view_files(path: str | Path) -> Dict[str, Any]:
    """Discover locally provided institutional-view files without reading raw reports."""
    source = Path(path)
    if source.is_file():
        candidates = [source]
    elif source.is_dir():
        candidates = [candidate for candidate in source.rglob("*") if candidate.is_file()]
    else:
        raise FileNotFoundError(f"Institutional view path not found: {source}")

    structured = sorted(
        str(candidate)
        for candidate in candidates
        if candidate.suffix.lower() in STRUCTURED_SUFFIXES
    )
    reference_only = sorted(
        str(candidate)
        for candidate in candidates
        if candidate.suffix.lower() in REFERENCE_ONLY_SUFFIXES
        and candidate.suffix.lower() not in STRUCTURED_SUFFIXES
    )
    unsupported = sorted(
        str(candidate)
        for candidate in candidates
        if candidate.suffix.lower() not in STRUCTURED_SUFFIXES
        and candidate.suffix.lower() not in REFERENCE_ONLY_SUFFIXES
    )
    return {
        "path": str(source),
        "structured_files": structured,
        "reference_only_files": reference_only,
        "unsupported_files": unsupported,
    }


def load_institutional_views_from_path(path: str | Path, target: str = "") -> Dict[str, Any]:
    """Load structured views from a file or directory and filter by target when provided."""
    discovered = discover_institutional_view_files(path)
    records: List[Dict[str, Any]] = []
    parse_errors = []
    for file_path in discovered["structured_files"]:
        try:
            records.extend(load_institutional_views(file_path))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            parse_errors.append({"file": file_path, "error": str(exc)})

    matched = [record for record in records if _matches_target(record, target)]
    return {
        "target": target,
        "discovery": discovered,
        "records": matched,
        "summary": summarize_institutional_views(matched),
        "parse_errors": parse_errors,
    }


def summarize_institutional_views(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    usable = [record for record in records if record.get("source_confidence") != "blocked"]
    targets = [record["target_price"] for record in usable if record.get("target_price") is not None]
    ratings = [record.get("rating") for record in usable if record.get("rating")]
    return {
        "count": len(records),
        "usable_count": len(usable),
        "blocked_count": len(records) - len(usable),
        "target_price_min": min(targets) if targets else None,
        "target_price_median": sorted(targets)[len(targets) // 2] if targets else None,
        "target_price_max": max(targets) if targets else None,
        "ratings": ratings,
        "blocked_sources": [
            record.get("provider", "unknown")
            for record in records
            if record.get("source_confidence") == "blocked"
        ],
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) not in {2, 3}:
        raise SystemExit(
            "Usage: python -m scripts.connectors.institutional_view_parser <file-or-folder> [ticker-or-company]"
        )
    result = load_institutional_views_from_path(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else "")
    print(json.dumps(result, indent=2, ensure_ascii=False))
