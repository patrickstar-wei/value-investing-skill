"""Data freshness checker for investment research.

This script classifies whether a data point is current enough for current valuation.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Dict


DEFAULT_STALENESS_DAYS: Dict[str, int] = {
    "market_price": 7,
    "market_multiple": 14,
    "quarterly_financials": 150,
    "semiannual_financials": 240,
    "annual_financials": 450,
    "earnings_guidance": 180,
    "segment_data": 450,
    "peer_group_data": 30,
    "clinical_regulatory": 90,
    "macro_market_data": 14,
}


@dataclass
class FreshnessResult:
    metric: str
    source_date: Optional[date]
    as_of_date: date
    age_days: Optional[int]
    threshold_days: int
    status: str
    warning: Optional[str]


def parse_date(value: str | date | None) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        return None


def check_freshness(
    metric: str,
    data_category: str,
    source_date: str | date | None,
    as_of_date: str | date | None = None,
) -> FreshnessResult:
    as_of = parse_date(as_of_date) or date.today()
    src_date = parse_date(source_date)
    threshold = DEFAULT_STALENESS_DAYS.get(data_category, 180)

    if src_date is None:
        return FreshnessResult(
            metric=metric,
            source_date=None,
            as_of_date=as_of,
            age_days=None,
            threshold_days=threshold,
            status="Missing",
            warning=f"{metric} source date is missing.",
        )

    age = (as_of - src_date).days

    if age <= threshold * 0.5:
        status = "Current"
        warning = None
    elif age <= threshold:
        status = "Recent but needs review"
        warning = f"{metric} is usable, but should be checked against newer updates."
    else:
        status = "Stale"
        warning = (
            f"{metric} is stale: source date {src_date.isoformat()} is {age} days before "
            f"analysis date {as_of.isoformat()}, exceeding threshold {threshold} days."
        )

    return FreshnessResult(
        metric=metric,
        source_date=src_date,
        as_of_date=as_of,
        age_days=age,
        threshold_days=threshold,
        status=status,
        warning=warning,
    )


def can_run_current_valuation(results: list[FreshnessResult]) -> tuple[bool, list[str]]:
    blocking = []
    for result in results:
        if result.status in {"Missing", "Stale"}:
            if result.metric in {
                "Current Price",
                "Shares Outstanding",
                "Revenue",
                "EBIT",
                "FCF",
                "Cash",
                "Debt",
            }:
                blocking.append(f"{result.metric}: {result.status}")

    return len(blocking) == 0, blocking


if __name__ == "__main__":
    samples = [
        check_freshness("Current Price", "market_price", "2026-04-29", "2026-04-30"),
        check_freshness("Revenue", "annual_financials", "2022-12-31", "2026-04-30"),
    ]
    for item in samples:
        print(item)

    ok, blockers = can_run_current_valuation(samples)
    print("Can run current valuation:", ok)
    print("Blockers:", blockers)
