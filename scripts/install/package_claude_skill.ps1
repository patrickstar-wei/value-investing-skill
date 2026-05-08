param(
    [string]$PackageName = "value-investing-claude-skill",
    [string]$OutputDir = "dist",
    [switch]$IncludeTests,
    [switch]$IncludeSourceMaterials,
    [switch]$NoZip,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
    $scriptPath = Split-Path -Parent $PSCommandPath
    return (Resolve-Path (Join-Path $scriptPath "..\..")).Path
}

function Test-SkippedPath {
    param([string]$RelativePath, [bool]$IncludeTestsFlag, [bool]$IncludeSourceMaterialsFlag)
    $parts = $RelativePath -split "[\\/]+"
    $skipDirs = @(".git", ".codex-plugin", ".trae", "__pycache__", ".pytest_cache", ".venv", "env", "dist", "evals", "reports", "output", "outputs", "results", "data", "institutional_reports", "licensed_data", "secrets", "credentials")
    if (-not $IncludeTestsFlag) {
        $skipDirs += "tests"
    }
    if (-not $IncludeSourceMaterialsFlag -and $RelativePath -match "^references[\\/]masters[\\/]source_materials(?:[\\/]|$)") {
        return $true
    }
    foreach ($part in $parts) {
        if ($skipDirs -contains $part) {
            return $true
        }
    }
    if ($RelativePath -ieq "README.md") {
        return $true
    }
    if ($RelativePath -like "*.pyc" -or $RelativePath -like "*.log" -or $RelativePath -like "*.tmp" -or $RelativePath -like "config\*.local.json" -or $RelativePath -like "config/*.local.json") {
        return $true
    }
    if ($RelativePath -ieq "plugin.json" -or $RelativePath -ieq ".gitmodules") {
        return $true
    }
    return $false
}

function Copy-SkillTree {
    param(
        [string]$Source,
        [string]$Destination,
        [bool]$IncludeTestsFlag,
        [bool]$IncludeSourceMaterialsFlag
    )

    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    $sourceFull = (Resolve-Path $Source).Path.TrimEnd("\", "/")
    Get-ChildItem -LiteralPath $sourceFull -Recurse -File | ForEach-Object {
        $relative = $_.FullName.Substring($sourceFull.Length).TrimStart("\", "/")
        if (Test-SkippedPath -RelativePath $relative -IncludeTestsFlag $IncludeTestsFlag -IncludeSourceMaterialsFlag $IncludeSourceMaterialsFlag) {
            return
        }
        $targetFile = Join-Path $Destination $relative
        $targetDir = Split-Path -Parent $targetFile
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $targetFile -Force
    }
}

$repoRoot = Get-RepoRoot
$distRoot = if ([System.IO.Path]::IsPathRooted($OutputDir)) { $OutputDir } else { Join-Path $repoRoot $OutputDir }
$packageRoot = Join-Path $distRoot $PackageName
$zipPath = Join-Path $distRoot "$PackageName.zip"

if (-not (Test-Path (Join-Path $repoRoot "SKILL.md"))) {
    throw "Repo root does not contain SKILL.md: $repoRoot"
}

if ((Test-Path $packageRoot) -or (Test-Path $zipPath)) {
    if (-not $Force) {
        throw "Package output already exists. Re-run with -Force to replace: $packageRoot / $zipPath"
    }
    if (Test-Path $packageRoot) {
        Remove-Item -LiteralPath $packageRoot -Recurse -Force
    }
    if (Test-Path $zipPath) {
        Remove-Item -LiteralPath $zipPath -Force
    }
}

New-Item -ItemType Directory -Force -Path $distRoot | Out-Null
Copy-SkillTree -Source $repoRoot -Destination $packageRoot -IncludeTestsFlag ([bool]$IncludeTests) -IncludeSourceMaterialsFlag ([bool]$IncludeSourceMaterials)

$installNote = @"
# Claude Skill Package

This package contains the Value Investing skill with its references, workflows, schemas, and Python valuation scripts.

## Install

Copy this folder to your Claude skills directory, commonly:

```powershell
`$env:USERPROFILE\.claude\skills\value-investing
```

If your Claude client uses a different skills directory, place the folder there instead.

## Smoke Test

From the package root:

```powershell
python -m unittest tests.test_valuation_models
```

Tests are included only when the package script is run with `-IncludeTests`.
Expanded master source materials are excluded by default; include them only with `-IncludeSourceMaterials`.
"@

Set-Content -Path (Join-Path $packageRoot "CLAUDE_INSTALL.md") -Value $installNote -Encoding UTF8

if (-not $NoZip) {
    Compress-Archive -Path (Join-Path $packageRoot "*") -DestinationPath $zipPath -Force
}

Write-Host "Created Claude skill package:"
Write-Host "  Folder: $packageRoot"
if (-not $NoZip) {
    Write-Host "  Zip:    $zipPath"
}
