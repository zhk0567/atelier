#!/usr/bin/env python3
"""Generate or rotate the Echo sync Bearer token.

Usage (from atelier root):
  python scripts/generate_echo_sync_token.py

Prints the plaintext token ONCE. Store it in Echo desktop / Android settings.
Only a PBKDF2 digest is saved under instance/.echo_sync_digest.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.echo_sync.auth import generate_token, set_token  # noqa: E402


def main() -> None:
    token = generate_token()
    set_token(token)
    print("=" * 60)
    print("Echo sync token generated.")
    print("Save this token now — it will not be shown again:")
    print()
    print(token)
    print()
    print("Configure clients with:")
    print("  Base URL: https://zhkun.xyz")
    print("  Authorization: Bearer <token>")
    print("=" * 60)


if __name__ == "__main__":
    main()
