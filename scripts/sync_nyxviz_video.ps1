# Sync NyxViz video.html static bundle into atelier/static/nyxviz/
# Run from atelier root:
#   $env:VITE_NYX_DATA_BASE = "https://data.zhkun.xyz/nyx/"
#   .\scripts\sync_nyxviz_video.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$NyxVizRoot = if ($env:NYXVIZ_ROOT) { $env:NYXVIZ_ROOT } else { "F:\commercial\NyxViz" }
$DestRoot = Join-Path $PSScriptRoot "..\static\nyxviz" | Resolve-Path -ErrorAction SilentlyContinue
if (-not $DestRoot) {
    $DestRoot = Join-Path (Get-Location) "static\nyxviz"
}

if (-not (Test-Path $NyxVizRoot)) {
    Write-Host "NyxViz not found: $NyxVizRoot" -ForegroundColor Red
    exit 1
}

Write-Host "Building NyxViz (atelier)..." -ForegroundColor Cyan
Push-Location $NyxVizRoot
try {
    if (-not $env:VITE_NYX_DATA_BASE) {
        Write-Host "Hint: set VITE_NYX_DATA_BASE to OSS URL, e.g. https://data.zhkun.xyz/nyx/" -ForegroundColor DarkYellow
    }
    npm run build:atelier
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}

$DistDir = Join-Path $NyxVizRoot "dist-atelier"
$FiguresSrc = Join-Path $NyxVizRoot "docs\figures"

if (-not (Test-Path $DistDir)) {
    Write-Host "Missing dist-atelier after build" -ForegroundColor Red
    exit 1
}

Write-Host "Syncing -> $DestRoot" -ForegroundColor Cyan
if (Test-Path $DestRoot) {
    Remove-Item -LiteralPath $DestRoot -Recurse -Force
}
New-Item -ItemType Directory -Path $DestRoot -Force | Out-Null

Copy-Item -Path (Join-Path $DistDir "video.html") -Destination $DestRoot
Copy-Item -Path (Join-Path $DistDir "assets") -Destination $DestRoot -Recurse
if (Test-Path (Join-Path $DistDir "stats")) {
    Copy-Item -Path (Join-Path $DistDir "stats") -Destination $DestRoot -Recurse
}
if (Test-Path $FiguresSrc) {
    Copy-Item -Path $FiguresSrc -Destination (Join-Path $DestRoot "figures") -Recurse
} else {
    Write-Host "Warning: figures dir missing: $FiguresSrc" -ForegroundColor Yellow
}

$bytes = (Get-ChildItem $DestRoot -Recurse -File | Measure-Object -Property Length -Sum).Sum
$mb = [math]::Round($bytes / 1MB, 1)
Write-Host "Done. static/nyxviz size: $mb MB" -ForegroundColor Green
Write-Host "Open: /static/nyxviz/video.html?record=1&scene=intro" -ForegroundColor DarkGray
