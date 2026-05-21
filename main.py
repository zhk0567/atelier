"""Personal site — application entry (uvicorn)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import uvicorn

from app import app
from app.constants import SITE_NAME, load_site_identity

UVICORN_HOST = "127.0.0.1"
UVICORN_PORT = 8000


def _kill_listeners_on_port(port: int) -> None:
    if sys.platform != "win32":
        return
    my_pid = os.getpid()
    ps = (
        f"$ids = Get-NetTCPConnection -LocalPort {port} -State Listen -ErrorAction SilentlyContinue "
        f"| Select-Object -ExpandProperty OwningProcess -Unique; "
        f"foreach ($procId in $ids) {{ "
        f"  if ($procId -and $procId -ne 0 -and $procId -ne {my_pid}) {{ "
        f"    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue "
        f"}}}}"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
        check=False,
        timeout=20,
    )


load_site_identity()

if __name__ == "__main__":
    mp = Path(__file__).resolve()
    print(f"[atelier] starting uvicorn from: {mp}", flush=True)
    print(f"[atelier] SITE_NAME={SITE_NAME!r}", flush=True)
    print(f"[atelier] freeing port {UVICORN_PORT} (stop old listeners)…", flush=True)
    _kill_listeners_on_port(UVICORN_PORT)
    uvicorn.run(
        "main:app",
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        reload=True,
    )
