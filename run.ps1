# Atelier dev server — 使用当前环境里的 python（如 conda base）
# 在仓库根目录:  .\run.ps1
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
    Write-Host "未找到 python（请先激活 conda base 或把 Python 加入 PATH）" -ForegroundColor Red
    exit 1
}

Write-Host "Using: $($python.Source)" -ForegroundColor DarkGray
& python $main
