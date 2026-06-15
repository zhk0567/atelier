# Upload Nyx/*.dat volume data to production ECS (same-origin hosting).
#
# Usage (from atelier root):
#   $env:ATELIER_SSH = "root@39.106.117.118"
#   $env:ATELIER_REMOTE = "/opt/atelier"
#   $env:NYXVIZ_ROOT = "F:\commercial\NyxViz"   # optional
#   .\scripts\upload_nyxviz_dat.ps1
#
# Source priority: static/nyxviz/Nyx/ then NYXVIZ_ROOT/Nyx/

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$ssh = if ($env:ATELIER_SSH) { $env:ATELIER_SSH } else { "root@39.106.117.118" }
$remoteRoot = if ($env:ATELIER_REMOTE) { $env:ATELIER_REMOTE.TrimEnd('/') } else { "/opt/atelier" }
$remoteNyx = "$remoteRoot/static/nyxviz/Nyx"
$localBundled = Join-Path (Get-Location) "static\nyxviz\Nyx"
$nyxVizRoot = if ($env:NYXVIZ_ROOT) { $env:NYXVIZ_ROOT } else { "F:\commercial\NyxViz" }
$localSource = if (Test-Path (Join-Path $localBundled "0000.dat")) { $localBundled } else { Join-Path $nyxVizRoot "Nyx" }

if (-not (Test-Path (Join-Path $localSource "0000.dat"))) {
    Write-Host "Missing 0000.dat under $localSource" -ForegroundColor Red
    Write-Host "Run: `$env:NYXVIZ_INCLUDE_DAT='1'; .\scripts\sync_nyxviz_video.ps1" -ForegroundColor Yellow
    exit 1
}

$files = Get-ChildItem $localSource -Filter "*.dat" -File
$mb = [math]::Round(($files | Measure-Object Length -Sum).Sum / 1MB, 1)
Write-Host "Uploading $($files.Count) .dat files ($mb MB) -> ${ssh}:${remoteNyx}/" -ForegroundColor Cyan

$archive = Join-Path $env:TEMP "nyxviz-nyx.tar"
if (Test-Path $archive) { Remove-Item $archive -Force }
Push-Location $localSource
try {
    & tar.exe -cf $archive *.dat
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} finally {
    Pop-Location
}

$remoteArchive = "/tmp/nyxviz-nyx.tar"
scp.exe $archive "${ssh}:${remoteArchive}"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

ssh.exe $ssh "mkdir -p `"$remoteNyx`" && tar -xf `"$remoteArchive`" -C `"$remoteNyx`" && rm -f `"$remoteArchive`""
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Remove-Item $archive -Force -ErrorAction SilentlyContinue

Write-Host "Verifying on server..." -ForegroundColor Cyan
ssh.exe $ssh "test -f `"$remoteNyx/0000.dat`" && test -f `"$remoteNyx/0099.dat`" && echo OK || echo MISSING"
Write-Host "Done. Check: https://zhkun.xyz/static/nyxviz/Nyx/0000.dat" -ForegroundColor Green
