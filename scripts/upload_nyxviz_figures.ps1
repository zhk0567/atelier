# Upload only static/nyxviz/figures (~178MB) to production ECS.
# Use when JS/CSS already deployed but PNG figures are 404.
#
# Usage (from atelier root):
#   $env:ATELIER_SSH = "root@39.106.117.118"
#   $env:ATELIER_REMOTE = "/opt/atelier"
#   .\scripts\upload_nyxviz_figures.ps1
#
# Optional: sync from NyxViz first if local figures stale:
#   .\scripts\sync_nyxviz_video.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$ssh = if ($env:ATELIER_SSH) { $env:ATELIER_SSH } else { "root@39.106.117.118" }
$remoteRoot = if ($env:ATELIER_REMOTE) { $env:ATELIER_REMOTE.TrimEnd('/') } else { "/opt/atelier" }
$remoteFigures = "$remoteRoot/static/nyxviz/figures"
$localFigures = Join-Path (Get-Location) "static\nyxviz\figures"

if (-not (Test-Path $localFigures)) {
    Write-Host "Missing $localFigures — run .\scripts\sync_nyxviz_video.ps1 first" -ForegroundColor Red
    exit 1
}

$probe = Join-Path $localFigures "task4_brush_top1.png"
if (-not (Test-Path $probe)) {
    Write-Host "Missing $probe — run sync from NyxViz" -ForegroundColor Red
    exit 1
}

$count = (Get-ChildItem $localFigures -Recurse -File).Count
$mb = [math]::Round(((Get-ChildItem $localFigures -Recurse -File | Measure-Object Length -Sum).Sum / 1MB), 1)
Write-Host "Uploading $count files ($mb MB) -> ${ssh}:${remoteFigures}/" -ForegroundColor Cyan

$archive = Join-Path $env:TEMP "nyxviz-figures.tar"
if (Test-Path $archive) { Remove-Item $archive -Force }
& tar.exe -cf $archive -C (Join-Path (Get-Location) "static\nyxviz") figures
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$remoteArchive = "/tmp/nyxviz-figures.tar"
scp.exe $archive "${ssh}:${remoteArchive}"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

ssh.exe $ssh "mkdir -p `"$remoteFigures`" && tar -xf `"$remoteArchive`" -C `"$remoteRoot/static/nyxviz`" && rm -f `"$remoteArchive`""
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Remove-Item $archive -Force -ErrorAction SilentlyContinue

Write-Host "Verifying on server..." -ForegroundColor Cyan
ssh.exe $ssh "test -f `"$remoteFigures/task4_brush_top1.png`" && echo OK || echo MISSING"
Write-Host "Done. Check: https://zhkun.xyz/static/nyxviz/figures/task4_brush_top1.png" -ForegroundColor Green
