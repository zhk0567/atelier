# Atelier dev server — run from repo root: .\run.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$main = Join-Path $PSScriptRoot "main.py"
if (-not (Test-Path $main)) {
    Write-Host "Missing $main" -ForegroundColor Red
    exit 1
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "python not found. Activate conda base or add Python to PATH." -ForegroundColor Red
    exit 1
}

Write-Host ("Using: " + $python.Source) -ForegroundColor DarkGray
& python $main
