"""Generate a markdown value investing report."""

from pathlib import Path
from typing import Dict, Any


def generate_report(data: Dict[str, Any]) -> str:
    return f"""# Value Investing Report

## 1. Target Overview

- Company / Industry: {data.get("target", "TBD")}
- Ticker: {data.get("ticker", "TBD")}
- Market: {data.get("market", "TBD")}
- Industry: {data.get("industry", "TBD")}
- Business Model: {data.get("business_model", "TBD")}

## 2. Valuation Model Selection

| Role | Model |
|---|---|
| Primary | {data.get("primary_model", "TBD")} |
| Cross-check | {data.get("cross_check_model", "TBD")} |
| Downside | {data.get("downside_model", "TBD")} |
| Implied Expectation | {data.get("implied_model", "TBD")} |

## 3. Business Quality

TBD

## 4. Financial Quality

TBD

## 5. Valuation

TBD

## 6. Margin of Safety

TBD

## 7. Risk Analysis

TBD

## 8. Final View

TBD
"""


if __name__ == "__main__":
    sample = {
        "target": "Sample Company",
        "ticker": "SAMPLE",
        "market": "US",
        "industry": "Quality Compounder",
        "business_model": "Recurring cash flow",
        "primary_model": "Owner Earnings DCF",
        "cross_check_model": "EPV",
        "downside_model": "No-growth EPV",
        "implied_model": "Reverse DCF",
    }
    report = generate_report(sample)
    out = Path("outputs/markdown/sample_report.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(out)
