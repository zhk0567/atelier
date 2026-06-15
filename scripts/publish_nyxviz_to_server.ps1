# Build NyxViz locally and upload static/nyxviz/ to production ECS via scp.
#
# Usage (from atelier root):
#   $env:NYXVIZ_INCLUDE_DAT = "1"          # optional: include Nyx/*.dat (~800MB)
#   $env:ATELIER_SSH = "root@your-ecs-ip"
#   $env:ATELIER_REMOTE = "/opt/atelier"   # optional
#   .\scripts\publish_nyxviz_to_server.ps1
#
# Requires OpenSSH scp on Windows (Settings -> Optional Features -> OpenSSH Client).

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$ssh = $env:ATELIER_SSH
if (-not $ssh) {
    Write-Host "Set ATELIER_SSH, e.g. root@47.x.x.x" -ForegroundColor Red
    exit 1
}

$remoteRoot = if ($env:ATELIER_REMOTE) { $env:ATELIER_REMOTE.TrimEnd('/') } else { "/opt/atelier" }
$remoteNyx = "$remoteRoot/static/nyxviz"

& "$PSScriptRoot\sync_nyxviz_video.ps1"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

& "$PSScriptRoot\verify_nyxviz_static.ps1"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$localNyx = Join-Path (Get-Location) "static\nyxviz"
Write-Host "Uploading $localNyx -> ${ssh}:${remoteNyx}/" -ForegroundColor Cyan

# Ensure remote directory exists
ssh $ssh "mkdir -p `"$remoteNyx`""

# Upload full bundle (video.html, assets, stats, figures)
scp -r "$localNyx\*" "${ssh}:${remoteNyx}/"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Restarting atelier on server..." -ForegroundColor Cyan
ssh $ssh "systemctl restart atelier 2>/dev/null || true"

Write-Host "Done. Verify: https://zhkun.xyz/static/nyxviz/video.html?record=1&scene=intro" -ForegroundColor Green
