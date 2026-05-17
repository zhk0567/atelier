# Clean common dev ports on Windows (PowerShell)
# Run from repo:  powershell -ExecutionPolicy Bypass -File .\scripts\clean-dev-ports.ps1

$ErrorActionPreference = "SilentlyContinue"
$ports = @(3000, 5173, 8000, 8001, 8002, 8003, 8080, 8888)

Write-Host "=== Listening PIDs before cleanup ===" -ForegroundColor Cyan
foreach ($port in $ports) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    foreach ($c in $conns) {
        if ($null -eq $c.OwningProcess -or $c.OwningProcess -eq 0) { continue }
        $p = Get-Process -Id $c.OwningProcess -ErrorAction SilentlyContinue
        $pn = if ($p) { $p.ProcessName } else { "?" }
        Write-Host "  Port $port  PID $($c.OwningProcess)  $pn"
    }
}

Write-Host "`n=== Stopping listeners on those ports ===" -ForegroundColor Yellow
foreach ($port in $ports) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    foreach ($c in $conns) {
        if ($null -eq $c.OwningProcess -or $c.OwningProcess -eq 0) { continue }
        Write-Host "  Stop PID $($c.OwningProcess) (port $port)"
        Stop-Process -Id $c.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

Start-Sleep -Seconds 1
Write-Host "`n=== Remaining listeners (should be empty for listed ports) ===" -ForegroundColor Green
foreach ($port in $ports) {
    $conns = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($conns) {
        foreach ($c in $conns) {
            Write-Host "  STILL LISTEN: port $port PID $($c.OwningProcess)"
        }
    }
}
Write-Host "`nDone. Start site:  cd F:\commercial\atelier  ;  python main.py" -ForegroundColor Cyan
