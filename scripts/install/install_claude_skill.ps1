param(
    [string]$SkillName = "value-investing",
    [string]$ClaudeSkillsDir = "$env:USERPROFILE\.claude\skills",
    [ValidateSet("Copy", "Junction")]
    [string]$Mode = "Copy",
    [switch]$Force,
    [switch]$IncludeTests
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
    $scriptPath = Split-Path -Parent $PSCommandPath
    return (Resolve-Path (Join-Path $scriptPath "..\..")).Path
}

function Test-SkippedPath {
    param([string]$RelativePath, [bool]$IncludeTestsFlag)
    $parts = $RelativePath -split "[\\/]+"
    $skipDirs = @(".git", ".trae", "__pycache__", ".pytest_cache", ".venv", "venv", "env", "dist", "reports", "output", "outputs", "results")
    if (-not $IncludeTestsFlag) {
        $skipDirs += "tests"
    }
    foreach ($part in $parts) {
        if ($skipDirs -contains $part) {
            return $true
        }
    }
    if ($RelativePath -like "*.pyc" -or $RelativePath -like "*.log" -or $RelativePath -like "*.tmp") {
        return $true
    }
    return $false
}

function Copy-SkillTree {
    param(
        [string]$Source,
        [string]$Destination,
        [bool]$IncludeTestsFlag
    )

    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    $sourceFull = (Resolve-Path $Source).Path.TrimEnd("\", "/")
    Get-ChildItem -LiteralPath $sourceFull -Recurse -File | ForEach-Object {
        $relative = $_.FullName.Substring($sourceFull.Length).TrimStart("\", "/")
        if (Test-SkippedPath -RelativePath $relative -IncludeTestsFlag $IncludeTestsFlag) {
            return
        }
        $targetFile = Join-Path $Destination $relative
        $targetDir = Split-Path -Parent $targetFile
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
        Copy-Item -LiteralPath $_.FullName -Destination $targetFile -Force
    }
}

$repoRoot = Get-RepoRoot
$targetRoot = Join-Path $ClaudeSkillsDir $SkillName

if (-not (Test-Path (Join-Path $repoRoot "SKILL.md"))) {
    throw "Repo root does not contain SKILL.md: $repoRoot"
}

if (Test-Path $targetRoot) {
    if (-not $Force) {
        throw "Target already exists: $targetRoot. Re-run with -Force to replace it."
    }
    Remove-Item -LiteralPath $targetRoot -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $ClaudeSkillsDir | Out-Null

if ($Mode -eq "Junction") {
    New-Item -ItemType Junction -Path $targetRoot -Target $repoRoot | Out-Null
} else {
    Copy-SkillTree -Source $repoRoot -Destination $targetRoot -IncludeTestsFlag ([bool]$IncludeTests)
}

Write-Host "Installed Claude skill:"
Write-Host "  Source: $repoRoot"
Write-Host "  Target: $targetRoot"
Write-Host "  Mode:   $Mode"
Write-Host ""
Write-Host "If your Claude client uses a different skills directory, re-run with -ClaudeSkillsDir <path>."
