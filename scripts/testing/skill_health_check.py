"""Repository health checks for the value-investing skill package.

The checks are intentionally lightweight so they can run without network
access, API keys, or model calls.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
ALLOWED_FRONTMATTER_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}


def _frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        raise AssertionError(f"{path.relative_to(ROOT)} missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise AssertionError(f"{path.relative_to(ROOT)} frontmatter must be a YAML mapping")
    return data, text


def _validate_skill_file(path: Path) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT)
    try:
        data, _ = _frontmatter(path)
    except Exception as exc:
        return [str(exc)]

    unexpected = set(data) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        errors.append(f"{rel} unexpected frontmatter keys: {', '.join(sorted(unexpected))}")

    name = data.get("name")
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9-]+", name):
        errors.append(f"{rel} name must be kebab-case")

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{rel} description is required")
    elif len(description) > 1024:
        errors.append(f"{rel} description exceeds 1024 characters")

    return errors


def _validate_evals() -> list[str]:
    path = ROOT / "evals" / "evals.json"
    if not path.exists():
        return ["evals/evals.json is missing"]

    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"evals/evals.json invalid JSON: {exc}"]

    if payload.get("skill_name") != "value-investing-research":
        errors.append("evals/evals.json skill_name must be value-investing-research")

    evals = payload.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals/evals.json must contain a non-empty evals list")
        return errors

    ids: set[int] = set()
    for index, item in enumerate(evals):
        if not isinstance(item, dict):
            errors.append(f"evals[{index}] must be an object")
            continue
        eval_id = item.get("id")
        if not isinstance(eval_id, int):
            errors.append(f"evals[{index}].id must be an integer")
        elif eval_id in ids:
            errors.append(f"evals[{index}].id duplicates {eval_id}")
        else:
            ids.add(eval_id)
        for key in ("prompt", "expected_output", "files", "expectations"):
            if key not in item:
                errors.append(f"evals[{index}] missing {key}")
        if "files" in item and not isinstance(item["files"], list):
            errors.append(f"evals[{index}].files must be a list")
        expectations = item.get("expectations")
        if not isinstance(expectations, list):
            errors.append(f"evals[{index}].expectations must be a list")
        elif len(expectations) < 3:
            errors.append(f"evals[{index}].expectations must contain at least 3 items")
        else:
            for exp_index, expectation in enumerate(expectations):
                if not isinstance(expectation, str) or not expectation.strip():
                    errors.append(f"evals[{index}].expectations[{exp_index}] must be a non-empty string")
    return errors


def main() -> int:
    skill_files = [ROOT / "SKILL.md", *sorted((ROOT / "skills").glob("*/SKILL.md"))]
    errors: list[str] = []

    for path in skill_files:
        errors.extend(_validate_skill_file(path))
    errors.extend(_validate_evals())

    if errors:
        print("Skill health check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Skill health check passed: {len(skill_files)} skill files and evals/evals.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
