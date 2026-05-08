"""Repository health checks for the value-investing skill package.

The checks are intentionally lightweight so they can run without network
access, API keys, or model calls.
"""

from __future__ import annotations

import json
import re
import sys
import ast
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


def _validate_formula_source_registry() -> list[str]:
    path = ROOT / "references" / "valuation_rules" / "formula_source_registry.json"
    if not path.exists():
        return ["references/valuation_rules/formula_source_registry.json is missing"]

    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"formula_source_registry.json invalid JSON: {exc}"]

    allowed_statuses = {
        "standard_formula",
        "standard_with_modeling_judgment",
        "heuristic_helper",
        "infrastructure",
    }
    sources = payload.get("sources")
    if not isinstance(sources, dict) or not sources:
        errors.append("formula_source_registry.json must define non-empty sources")
        sources = {}

    for source_id, source in sources.items():
        if not isinstance(source, dict):
            errors.append(f"formula_source_registry sources[{source_id}] must be an object")
            continue
        if not source.get("title") or not source.get("url") or not source.get("type"):
            errors.append(f"formula_source_registry sources[{source_id}] must include title, url, and type")

    implementations = payload.get("implementations")
    if not isinstance(implementations, list) or not implementations:
        errors.append("formula_source_registry.json must define non-empty implementations")
        return errors

    by_script: dict[str, dict] = {}
    for index, implementation in enumerate(implementations):
        if not isinstance(implementation, dict):
            errors.append(f"formula_source_registry implementations[{index}] must be an object")
            continue

        script = implementation.get("script")
        if not isinstance(script, str) or not script.strip():
            errors.append(f"formula_source_registry implementations[{index}] missing script")
            continue
        if script in by_script:
            errors.append(f"formula_source_registry duplicate implementation for {script}")
        by_script[script] = implementation

        script_path = ROOT / script
        script_functions: set[str] = set()
        if not script_path.exists():
            errors.append(f"formula_source_registry references missing script: {script}")
        else:
            try:
                parsed_script = ast.parse(script_path.read_text(encoding="utf-8"))
            except SyntaxError as exc:
                errors.append(f"formula_source_registry could not parse {script}: {exc}")
            else:
                script_functions = {
                    node.name
                    for node in ast.walk(parsed_script)
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                }

        status = implementation.get("status")
        if status not in allowed_statuses:
            errors.append(f"formula_source_registry {script} has invalid status: {status}")

        formulas = implementation.get("formulas")
        if not isinstance(formulas, list):
            errors.append(f"formula_source_registry {script} formulas must be a list")
            continue
        if status != "infrastructure" and not formulas:
            errors.append(f"formula_source_registry {script} must include formulas")

        for formula_index, formula in enumerate(formulas):
            if not isinstance(formula, dict):
                errors.append(f"formula_source_registry {script} formulas[{formula_index}] must be an object")
                continue
            functions = formula.get("functions")
            if not isinstance(functions, list) or not all(isinstance(item, str) and item for item in functions):
                errors.append(f"formula_source_registry {script} formulas[{formula_index}] functions must be non-empty strings")
            else:
                missing_functions = [function for function in functions if function not in script_functions]
                if missing_functions:
                    errors.append(
                        f"formula_source_registry {script} formulas[{formula_index}] references missing functions: "
                        + ", ".join(missing_functions)
                    )
            if not isinstance(formula.get("formula"), str) or not formula["formula"].strip():
                errors.append(f"formula_source_registry {script} formulas[{formula_index}] missing formula")
            source_ids = formula.get("source_ids")
            if not isinstance(source_ids, list) or not source_ids:
                errors.append(f"formula_source_registry {script} formulas[{formula_index}] missing source_ids")
            else:
                for source_id in source_ids:
                    if source_id not in sources:
                        errors.append(f"formula_source_registry {script} formulas[{formula_index}] unknown source_id: {source_id}")

        tests = implementation.get("tests")
        if not isinstance(tests, list) or not tests:
            errors.append(f"formula_source_registry {script} must include tests")
        limitations = implementation.get("limitations")
        if not isinstance(limitations, list) or not limitations:
            errors.append(f"formula_source_registry {script} must include limitations")

    valuation_scripts = sorted(
        str(path.relative_to(ROOT))
        for path in (ROOT / "scripts" / "valuation").glob("valuation_*.py")
    )
    missing = [script for script in valuation_scripts if script not in by_script]
    if missing:
        errors.append("formula_source_registry missing valuation scripts: " + ", ".join(missing))

    return errors


def main() -> int:
    skill_files = [ROOT / "SKILL.md", *sorted((ROOT / "skills").glob("*/SKILL.md"))]
    errors: list[str] = []

    for path in skill_files:
        errors.extend(_validate_skill_file(path))
    errors.extend(_validate_evals())
    errors.extend(_validate_formula_source_registry())

    if errors:
        print("Skill health check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Skill health check passed: {len(skill_files)} skill files, evals/evals.json, and formula registry")
    return 0


if __name__ == "__main__":
    sys.exit(main())
