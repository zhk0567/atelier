# One-shot upload: figures (~178MB) + Nyx dat (~800MB) to production ECS.
# Run in an interactive terminal (will prompt for SSH password if no key).
#
#   Set-Location F:\commercial\atelier
#   .\scripts\upload_nyxviz_all.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$ssh = if ($env:ATELIER_SSH) { $env:ATELIER_SSH } else { "root@39.106.117.118" }
$remoteRoot = if ($env:ATELIER_REMOTE) { $env:ATELIER_REMOTE.TrimEnd('/') } else { "/opt/atelier" }
$nyxVizRoot = if ($env:NYXVIZ_ROOT) { $env:NYXVIZ_ROOT } else { "F:\commercial\NyxViz" }

Write-Host "=== NyxViz fast upload ===" -ForegroundColor Cyan
Write-Host "Target: $ssh ($remoteRoot)" -ForegroundColor DarkGray
Write-Host "You may be asked for SSH password twice (figures + nyx)." -ForegroundColor Yellow

ssh.exe -o ConnectTimeout=15 $ssh "echo connected && df -h /opt | tail -1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "SSH failed. Check password or add your public key to the server." -ForegroundColor Red
    exit 1
}

# --- figures ---
$localFigures = Join-Path (Get-Location) "static\nyxviz\figures"
if (-not (Test-Path (Join-Path $localFigures "task4_brush_top1.png"))) {
    Write-Host "Missing figures. Run .\scripts\sync_nyxviz_video.ps1 first." -ForegroundColor Red
    exit 1
}

$figTar = Join-Path $env:TEMP "nyxviz-figures.tar"
Write-Host "[1/4] Packing figures..." -ForegroundColor Cyan
& tar.exe -cf $figTar -C (Join-Path (Get-Location) "static\nyxviz") figures
$figMb = [math]::Round((Get-Item $figTar).Length / 1MB, 1)
Write-Host "      figures.tar = $figMb MB"

Write-Host "[2/4] Uploading figures (scp)..." -ForegroundColor Cyan
scp.exe $figTar "${ssh}:/tmp/nyxviz-figures.tar"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

ssh.exe $ssh "mkdir -p `"$remoteRoot/static/nyxviz/figures`" && tar -xf /tmp/nyxviz-figures.tar -C `"$remoteRoot/static/nyxviz`" && rm -f /tmp/nyxviz-figures.tar"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Remove-Item $figTar -Force -ErrorAction SilentlyContinue
Write-Host "      figures OK" -ForegroundColor Green

# --- Nyx dat ---
$localNyx = Join-Path $nyxVizRoot "Nyx"
if (-not (Test-Path (Join-Path $localNyx "0000.dat"))) {
    Write-Host "Missing $localNyx — set NYXVIZ_ROOT or copy .dat files." -ForegroundColor Red
    exit 1
}

$nyxTar = Join-Path $env:TEMP "nyxviz-nyx.tar"
Write-Host "[3/4] Packing Nyx .dat (100 files)..." -ForegroundColor Cyan
Push-Location $localNyx
& tar.exe -cf $nyxTar *.dat
Pop-Location
$nyxMb = [math]::Round((Get-Item $nyxTar).Length / 1MB, 1)
Write-Host "      nyx.tar = $nyxMb MB"

Write-Host "[4/4] Uploading Nyx dat (scp, may take several minutes)..." -ForegroundColor Cyan
scp.exe $nyxTar "${ssh}:/tmp/nyxviz-nyx.tar"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

ssh.exe $ssh "mkdir -p `"$remoteRoot/static/nyxviz/Nyx`" && tar -xf /tmp/nyxviz-nyx.tar -C `"$remoteRoot/static/nyxviz/Nyx`" && rm -f /tmp/nyxviz-nyx.tar"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Remove-Item $nyxTar -Force -ErrorAction SilentlyContinue
Write-Host "      nyx dat OK" -ForegroundColor Green

Write-Host ""
Write-Host "Verify:" -ForegroundColor Cyan
ssh.exe $ssh "test -f `"$remoteRoot/static/nyxviz/figures/task4_brush_top1.png`" && test -f `"$remoteRoot/static/nyxviz/Nyx/0000.dat`" && echo ALL_OK || echo CHECK_FAILED"
Write-Host "Browser:" -ForegroundColor Cyan
Write-Host "  https://zhkun.xyz/static/nyxviz/figures/task4_brush_top1.png"
Write-Host "  https://zhkun.xyz/static/nyxviz/Nyx/0000.dat"
Write-Host "  https://zhkun.xyz/static/nyxviz/video.html?record=1&scene=intro"
Write-Host "Done." -ForegroundColor Green
