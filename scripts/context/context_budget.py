"""Token/context budget helpers.

This module estimates context size roughly by character count.
For production, replace this with a model-specific tokenizer.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class ContextFile:
    path: str
    chars: int
    estimated_tokens: int


def estimate_tokens(text: str) -> int:
    # Conservative rough estimate for mixed Chinese/English docs.
    return max(1, len(text) // 2)


def inspect_files(paths: Iterable[str]) -> List[ContextFile]:
    result: List[ContextFile] = []
    for path in paths:
        text = Path(path).read_text(encoding="utf-8")
        result.append(ContextFile(
            path=path,
            chars=len(text),
            estimated_tokens=estimate_tokens(text),
        ))
    return result


def over_budget(files: Iterable[ContextFile], budget_tokens: int) -> bool:
    return sum(f.estimated_tokens for f in files) > budget_tokens


if __name__ == "__main__":
    root = Path(".")
    files = list(root.glob("**/SKILL.md"))
    inspected = inspect_files([str(f) for f in files])
    total = sum(f.estimated_tokens for f in inspected)
    print(f"Estimated SKILL.md tokens: {total}")
    for item in sorted(inspected, key=lambda x: x.estimated_tokens, reverse=True)[:10]:
        print(item)
