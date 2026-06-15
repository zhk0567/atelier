# Verify NyxViz static bundle under static/nyxviz/
# Exit 1 if video.html references assets that are missing locally.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$Root = Join-Path (Get-Location) "static\nyxviz"
$Video = Join-Path $Root "video.html"

if (-not (Test-Path $Video)) {
    Write-Host "Missing $Video — run scripts\sync_nyxviz_video.ps1" -ForegroundColor Red
    exit 1
}

$html = Get-Content -LiteralPath $Video -Raw
$refs = [regex]::Matches($html, '/static/nyxviz/([^"''>\s]+)') |
    ForEach-Object { $_.Groups[1].Value } |
    Select-Object -Unique

$missing = @()
foreach ($rel in $refs) {
    if ($rel -eq "runtime-config.js") { continue }
    $path = Join-Path $Root ($rel -replace '^/', '' -replace '/', '\')
    if (-not (Test-Path $path)) {
        $missing += $rel
    }
}

$figCount = 0
$figDir = Join-Path $Root "figures"
if (Test-Path $figDir) {
    $figCount = (Get-ChildItem $figDir -Recurse -File -Filter "*.png").Count
}

Write-Host "video.html: OK" -ForegroundColor Green
Write-Host "assets refs: $($refs.Count), missing: $($missing.Count)" -ForegroundColor $(if ($missing.Count) { "Red" } else { "Green" })
Write-Host "figures png: $figCount" -ForegroundColor $(if ($figCount -lt 1) { "Yellow" } else { "Green" })

if ($missing.Count -gt 0) {
    $missing | ForEach-Object { Write-Host "  MISSING $_" -ForegroundColor Red }
    exit 1
}

if ($figCount -lt 1) {
    Write-Host "Warning: figures/ empty — page may load but images will 404" -ForegroundColor Yellow
}

$reqList = Join-Path $PSScriptRoot "nyxviz_required_figures.txt"
$reqMissing = @()
if (Test-Path $reqList) {
    Get-Content -LiteralPath $reqList | ForEach-Object {
        $line = $_.Trim()
        if (-not $line -or $line.StartsWith("#")) { return }
        $p = Join-Path $figDir $line
        if (-not (Test-Path $p)) {
            $reqMissing += $line
        }
    }
    Write-Host "videoStaticFigures: $($reqMissing.Count) missing of $((Get-Content $reqList | Where-Object { $_ -match '\S' -and -not $_.StartsWith('#') }).Count)" -ForegroundColor $(if ($reqMissing.Count) { "Red" } else { "Green" })
    if ($reqMissing.Count -gt 0) {
        $reqMissing | ForEach-Object { Write-Host "  MISSING $_" -ForegroundColor Red }
        exit 1
    }
}

Write-Host "NyxViz bundle OK" -ForegroundColor Green
