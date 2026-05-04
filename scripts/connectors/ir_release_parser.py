"""Public IR / earnings-release parser.

This parser extracts a compact, auditable summary from public HTML/text
earnings releases or local text/HTML files. It is intentionally conservative:
numbers are candidate evidence, not authoritative financial statements.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List
from urllib.request import Request, urlopen


CURRENCY_PREFIX = r"(?:USD|RMB|CNY|HKD|EUR|GBP|\$)?"
METRIC_PATTERNS = {
    "revenue": re.compile(
        rf"\b(?:revenue|revenues|net sales)\b[^.\n]{{0,120}}?({CURRENCY_PREFIX}\s?[\d,.]+)\s?(billion|million|bn|m)?",
        re.I,
    ),
    "free_cash_flow": re.compile(
        rf"\bfree cash flow\b[^.\n]{{0,120}}?({CURRENCY_PREFIX}\s?[\d,.]+)\s?(billion|million|bn|m)?",
        re.I,
    ),
    "gross_margin": re.compile(r"\bgross margin\b[^.\n]{0,120}?(\d+(?:\.\d+)?)\s?%", re.I),
    "operating_margin": re.compile(r"\boperating margin\b[^.\n]{0,120}?(\d+(?:\.\d+)?)\s?%", re.I),
    "eps": re.compile(
        rf"\b(?:diluted )?(?:eps|earnings per share)\b[^.\n]{{0,120}}?({CURRENCY_PREFIX}\s?[\d,.]+)",
        re.I,
    ),
    "capex": re.compile(
        rf"\b(?:capital expenditures|capex)\b[^.\n]{{0,120}}?({CURRENCY_PREFIX}\s?[\d,.]+)\s?(billion|million|bn|m)?",
        re.I,
    ),
}

GUIDANCE_PATTERN = re.compile(r"\b(?:outlook|guidance|expects?|forecast|projects?)\b[^.\n]{0,220}", re.I)


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip = False
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[no-untyped-def]
        if tag.lower() in {"script", "style", "noscript"}:
            self._skip = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript"}:
            self._skip = False

    def handle_data(self, data: str) -> None:
        if not self._skip and data.strip():
            self.parts.append(data.strip())


@dataclass
class ParsedRelease:
    source: str
    title: str = ""
    release_date: str = ""
    metrics: Dict[str, List[str]] = field(default_factory=dict)
    guidance_sentences: List[str] = field(default_factory=list)
    risk_sentences: List[str] = field(default_factory=list)
    source_type: str = "public_ir_release"
    source_tier: int = 2
    confidence: str = "medium"
    extraction_timestamp: str = ""
    notes: str = "Use as public IR evidence; reconcile key numbers to filings when available."


def _fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "value-investing-skill/0.1"})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def html_to_text(raw: str) -> str:
    parser = _TextExtractor()
    parser.feed(raw)
    text = " ".join(parser.parts) if parser.parts else raw
    return re.sub(r"\s+", " ", text).strip()


def _load_source(source: str) -> str:
    if re.match(r"^https?://", source, re.I):
        return _fetch_text(source)
    return Path(source).read_text(encoding="utf-8", errors="replace")


def _sentences(text: str) -> List[str]:
    return [item.strip() for item in re.split(r"(?<=[.!?])\s+", text) if item.strip()]


def _title(text: str) -> str:
    first = text.split(". ", 1)[0].strip()
    return first[:180]


def _release_date(text: str) -> str:
    patterns = [
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},\s+\d{4}\b",
        r"\b\d{4}-\d{2}-\d{2}\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group(0)
    return ""


def parse_release_text(text: str, source: str = "inline") -> Dict[str, object]:
    clean = html_to_text(text)
    metrics: Dict[str, List[str]] = {}
    for name, pattern in METRIC_PATTERNS.items():
        matches = []
        for match in pattern.finditer(clean):
            matches.append(match.group(0)[:220])
        if matches:
            metrics[name] = matches[:5]

    sentences = _sentences(clean)
    guidance = [sentence[:260] for sentence in sentences if GUIDANCE_PATTERN.search(sentence)][:8]
    risk = [
        sentence[:260]
        for sentence in sentences
        if re.search(r"\b(risk|uncertain|headwind|restriction|regulation|supply|demand)\b", sentence, re.I)
    ][:8]

    result = ParsedRelease(
        source=source,
        title=_title(clean),
        release_date=_release_date(clean),
        metrics=metrics,
        guidance_sentences=guidance,
        risk_sentences=risk,
        extraction_timestamp=datetime.now(timezone.utc).isoformat(),
    )
    return asdict(result)


def parse_release(source: str) -> Dict[str, object]:
    return parse_release_text(_load_source(source), source=source)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python -m scripts.connectors.ir_release_parser <url-or-local-file>")
    print(json.dumps(parse_release(sys.argv[1]), indent=2, ensure_ascii=False))
