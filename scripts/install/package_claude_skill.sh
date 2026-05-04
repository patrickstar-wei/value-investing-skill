#!/usr/bin/env bash
set -euo pipefail

PACKAGE_NAME="value-investing-claude-skill"
OUTPUT_DIR="dist"
INCLUDE_TESTS=0
INCLUDE_SOURCE_MATERIALS=0
NO_ZIP=0
FORCE=0
OS_NAME="$(uname -s 2>/dev/null || echo unknown)"

usage() {
  cat <<'EOF'
Usage: package_claude_skill.sh [options]

Options:
  --name NAME              Package folder / zip base name
  --output-dir DIR         Output directory (default: dist)
  --include-tests          Include tests in the package
  --include-source-materials
                           Include expanded master source-material submodules
  --no-zip                 Create folder only
  --force                  Replace existing package output
  -h, --help               Show help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      PACKAGE_NAME="$2"; shift 2 ;;
    --output-dir)
      OUTPUT_DIR="$2"; shift 2 ;;
    --include-tests)
      INCLUDE_TESTS=1; shift ;;
    --include-source-materials)
      INCLUDE_SOURCE_MATERIALS=1; shift ;;
    --no-zip)
      NO_ZIP=1; shift ;;
    --force)
      FORCE=1; shift ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
if [[ "$OUTPUT_DIR" = /* ]]; then
  DIST_ROOT="$OUTPUT_DIR"
else
  DIST_ROOT="${REPO_ROOT}/${OUTPUT_DIR}"
fi
PACKAGE_ROOT="${DIST_ROOT}/${PACKAGE_NAME}"
ZIP_PATH="${DIST_ROOT}/${PACKAGE_NAME}.zip"

if [[ ! -f "${REPO_ROOT}/SKILL.md" ]]; then
  echo "Repo root does not contain SKILL.md: ${REPO_ROOT}" >&2
  exit 1
fi

if [[ -e "$PACKAGE_ROOT" || -e "$ZIP_PATH" ]]; then
  if [[ "$FORCE" -ne 1 ]]; then
    echo "Package output already exists. Re-run with --force to replace it: ${PACKAGE_ROOT} / ${ZIP_PATH}" >&2
    exit 1
  fi
  rm -rf "$PACKAGE_ROOT" "$ZIP_PATH"
fi

mkdir -p "$PACKAGE_ROOT"

EXCLUDES=(
  --exclude='.git'
  --exclude='.codex-plugin'
  --exclude='.trae'
  --exclude='__pycache__'
  --exclude='.pytest_cache'
  --exclude='.venv'
  --exclude='venv'
  --exclude='env'
  --exclude='dist'
  --exclude='data'
  --exclude='institutional_reports'
  --exclude='licensed_data'
  --exclude='secrets'
  --exclude='credentials'
  --exclude='reports'
  --exclude='output'
  --exclude='outputs'
  --exclude='results'
  --exclude='*.pyc'
  --exclude='*.log'
  --exclude='*.tmp'
  --exclude='plugin.json'
  --exclude='.gitmodules'
  --exclude='config/*.local.json'
)
if [[ "$INCLUDE_TESTS" -ne 1 ]]; then
  EXCLUDES+=(--exclude='tests')
fi
if [[ "$INCLUDE_SOURCE_MATERIALS" -ne 1 ]]; then
  EXCLUDES+=(--exclude='references/masters/source_materials')
fi

if command -v rsync >/dev/null 2>&1; then
  rsync -a "${EXCLUDES[@]}" "${REPO_ROOT}/" "${PACKAGE_ROOT}/"
else
  tar -C "$REPO_ROOT" "${EXCLUDES[@]}" -cf - . | tar -C "$PACKAGE_ROOT" -xf -
fi

cat > "${PACKAGE_ROOT}/CLAUDE_INSTALL.md" <<'EOF'
# Claude Skill Package

This package contains the Value Investing skill with references, workflows, schemas, and Python valuation scripts.

## Install

Copy this folder to your Claude skills directory, commonly:

```bash
~/.claude/skills/value-investing
```

On macOS Claude desktop setups may use:

```bash
~/Library/Application\ Support/Claude/skills/value-investing
```

If your Claude client uses a different skills directory, place the folder there instead.

## Smoke Test

From the package root:

```bash
python3 -m unittest tests.test_valuation_models
```

Tests are included only when the package script is run with `--include-tests`.
Expanded master source materials are excluded by default; include them only with `--include-source-materials`.
EOF

if [[ "$NO_ZIP" -ne 1 ]]; then
  if command -v zip >/dev/null 2>&1; then
    (cd "$DIST_ROOT" && zip -qr "${PACKAGE_NAME}.zip" "$PACKAGE_NAME")
  else
    echo "zip command not found; created folder only: ${PACKAGE_ROOT}" >&2
  fi
fi

cat <<EOF
Created Claude skill package:
  Folder: ${PACKAGE_ROOT}
  OS:     ${OS_NAME}
EOF
if [[ -f "$ZIP_PATH" ]]; then
  echo "  Zip:    ${ZIP_PATH}"
fi
