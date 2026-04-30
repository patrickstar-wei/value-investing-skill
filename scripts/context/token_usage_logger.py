"""Token usage logger.

Use this to store usage metrics from API responses.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
import json
from typing import Optional


@dataclass
class TokenUsageRecord:
    task_id: str
    model: str
    input_tokens: int
    cached_input_tokens: int
    output_tokens: int
    total_tokens: int
    context_files: list[str]
    mode: str


def append_usage(record: TokenUsageRecord, path: str = "outputs/audit_logs/token_usage.jsonl") -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")


def cache_hit_rate(record: TokenUsageRecord) -> Optional[float]:
    if record.input_tokens <= 0:
        return None
    return record.cached_input_tokens / record.input_tokens
