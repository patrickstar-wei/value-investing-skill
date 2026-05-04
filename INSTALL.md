# Install Guide

This project can be installed as a local skill for Codex and Claude on Windows, Linux, and macOS.

## Codex

### Windows

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install\install_codex_skill.ps1
```

Default target:

```text
%USERPROFILE%\.codex\skills\value-investing
```

### Linux / macOS

```bash
bash scripts/install/install_codex_skill.sh
```

Default target:

```text
~/.codex/skills/value-investing
```

Use copy mode instead of symlink mode:

```bash
bash scripts/install/install_codex_skill.sh --mode copy --force
```

## Claude

### Windows

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install\install_claude_skill.ps1
```

Default target:

```text
%USERPROFILE%\.claude\skills\value-investing
```

### Linux

```bash
bash scripts/install/install_claude_skill.sh
```

Default target:

```text
~/.claude/skills/value-investing
```

### macOS

Default:

```bash
bash scripts/install/install_claude_skill.sh
```

If your Claude client uses the Application Support directory:

```bash
bash scripts/install/install_claude_skill.sh --dir "$HOME/Library/Application Support/Claude/skills"
```

The script automatically chooses `~/Library/Application Support/Claude/skills` on macOS when `~/Library/Application Support/Claude` already exists. Otherwise it falls back to `~/.claude/skills`.

## Claude Package

### Windows

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install\package_claude_skill.ps1 -Force
```

### Linux / macOS

```bash
bash scripts/install/package_claude_skill.sh --force
```

Output:

```text
dist/value-investing-claude-skill/
dist/value-investing-claude-skill.zip
```

If `zip` is unavailable on Linux/macOS, the script still creates the package folder.

## Common Options

Linux/macOS installers:

```bash
--name value-investing
--dir /custom/skills/path
--mode symlink|copy
--force
--include-tests
```

Windows installers:

```powershell
-SkillName value-investing
-CodexSkillsDir <path>
-ClaudeSkillsDir <path>
-Mode Junction|Copy
-Force
-IncludeTests
```

