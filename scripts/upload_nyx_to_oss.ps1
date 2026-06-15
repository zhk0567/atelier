# Upload NyxViz Nyx/*.dat to Aliyun OSS (external CDN for atelier video demo)
#
# Prerequisites:
#   - Aliyun OSS CLI (ossutil) configured, or use ossutil64.exe in PATH
#   - Bucket with public-read or signed URL + CORS for zhkun.xyz
#
# Usage (from atelier root):
#   $env:NYXVIZ_ROOT = "F:\commercial\NyxViz"
#   $env:OSS_BUCKET = "oss://your-bucket/nyx"
#   .\scripts\upload_nyx_to_oss.ps1
#
# CORS (OSS console -> Bucket -> Cross-Origin Resource Sharing):
#   AllowedOrigin: https://zhkun.xyz, http://127.0.0.1:8000
#   AllowedMethod: GET, HEAD
#   AllowedHeader: *
#   ExposeHeader: Content-Length, Content-Type, ETag
#
# Optional CDN: bind data.zhkun.xyz to bucket, Cache-Control on .dat:
#   public, max-age=31536000, immutable
#
# Build with CDN base:
#   $env:VITE_NYX_DATA_BASE = "https://data.zhkun.xyz/nyx/"
#   .\scripts\sync_nyxviz_video.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$NyxVizRoot = if ($env:NYXVIZ_ROOT) { $env:NYXVIZ_ROOT } else { "F:\commercial\NyxViz" }
$NyxDir = Join-Path $NyxVizRoot "Nyx"
$Bucket = $env:OSS_BUCKET

if (-not $Bucket) {
    Write-Host "Set OSS_BUCKET, e.g. oss://my-bucket/nyx" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $NyxDir)) {
    Write-Host "Nyx data dir missing: $NyxDir" -ForegroundColor Red
    exit 1
}

$ossutil = Get-Command ossutil -ErrorAction SilentlyContinue
if (-not $ossutil) {
    $ossutil = Get-Command ossutil64 -ErrorAction SilentlyContinue
}
if (-not $ossutil) {
    Write-Host "ossutil not found. Install Aliyun ossutil or upload manually." -ForegroundColor Red
    Write-Host "See docs/NYXVIZ_DEPLOY.md" -ForegroundColor DarkGray
    exit 1
}

$files = Get-ChildItem -Path $NyxDir -Filter "*.dat" -File
if ($files.Count -eq 0) {
    Write-Host "No .dat files in $NyxDir" -ForegroundColor Red
    exit 1
}

Write-Host "Uploading $($files.Count) files to $Bucket ..." -ForegroundColor Cyan
& $ossutil.Source cp $NyxDir "${Bucket}/" -r --update --meta "Cache-Control:public,max-age=31536000,immutable"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "Upload complete." -ForegroundColor Green
Write-Host "Verify: curl -I `"https://data.zhkun.xyz/nyx/0099.dat`"" -ForegroundColor DarkGray
