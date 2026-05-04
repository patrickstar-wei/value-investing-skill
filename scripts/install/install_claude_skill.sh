#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="value-investing"
OS_NAME="$(uname -s 2>/dev/null || echo unknown)"
DEFAULT_CLAUDE_SKILLS_DIR="${HOME}/.claude/skills"
if [[ "$OS_NAME" == "Darwin" && -d "${HOME}/Library/Application Support/Claude" ]]; then
  DEFAULT_CLAUDE_SKILLS_DIR="${HOME}/Library/Application Support/Claude/skills"
fi
CLAUDE_SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$DEFAULT_CLAUDE_SKILLS_DIR}"
MODE="copy"
FORCE=0
INCLUDE_TESTS=0

usage() {
  cat <<'EOF'
Usage: install_claude_skill.sh [options]

Options:
  --name NAME              Installed skill directory name (default: value-investing)
  --dir DIR                Claude skills directory (default: ~/.claude/skills; on macOS uses ~/Library/Application Support/Claude/skills if Claude app dir exists)
  --mode copy|symlink      Install mode (default: copy)
  --force                  Replace existing target
  --include-tests          Include tests when --mode copy is used
  -h, --help               Show help
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      SKILL_NAME="$2"; shift 2 ;;
    --dir)
      CLAUDE_SKILLS_DIR="$2"; shift 2 ;;
    --mode)
      MODE="$2"; shift 2 ;;
    --force)
      FORCE=1; shift ;;
    --include-tests)
      INCLUDE_TESTS=1; shift ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "Unknown option: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ "$MODE" != "copy" && "$MODE" != "symlink" ]]; then
  echo "--mode must be copy or symlink" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
TARGET="${CLAUDE_SKILLS_DIR}/${SKILL_NAME}"

if [[ ! -f "${REPO_ROOT}/SKILL.md" ]]; then
  echo "Repo root does not contain SKILL.md: ${REPO_ROOT}" >&2
  exit 1
fi

if [[ -e "$TARGET" || -L "$TARGET" ]]; then
  if [[ "$FORCE" -ne 1 ]]; then
    echo "Target already exists: ${TARGET}. Re-run with --force to replace it." >&2
    exit 1
  fi
  rm -rf "$TARGET"
fi

mkdir -p "$CLAUDE_SKILLS_DIR"

if [[ "$MODE" == "symlink" ]]; then
  ln -s "$REPO_ROOT" "$TARGET"
else
  mkdir -p "$TARGET"
  EXCLUDES=(
    --exclude='.git'
    --exclude='.trae'
    --exclude='__pycache__'
    --exclude='.pytest_cache'
    --exclude='.venv'
    --exclude='venv'
    --exclude='env'
    --exclude='dist'
    --exclude='reports'
    --exclude='output'
    --exclude='outputs'
    --exclude='results'
    --exclude='*.pyc'
    --exclude='*.log'
    --exclude='*.tmp'
  )
  if [[ "$INCLUDE_TESTS" -ne 1 ]]; then
    EXCLUDES+=(--exclude='tests')
  fi
  if command -v rsync >/dev/null 2>&1; then
    rsync -a "${EXCLUDES[@]}" "${REPO_ROOT}/" "${TARGET}/"
  else
    tar -C "$REPO_ROOT" "${EXCLUDES[@]}" -cf - . | tar -C "$TARGET" -xf -
  fi
fi

cat <<EOF
Installed Claude skill:
  Source: ${REPO_ROOT}
  Target: ${TARGET}
  Mode:   ${MODE}
  OS:     ${OS_NAME}

If your Claude client uses a different skills directory, re-run with --dir <path>.
EOF
