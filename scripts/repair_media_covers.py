#!/usr/bin/env python3
"""Clear untrusted / mismatched browse covers so fetch can re-pull with tight matching.

Usage (repo root, Windows PowerShell)::

    Set-Location F:\\commercial\\atelier
    python scripts\\repair_media_covers.py
    python scripts\\repair_media_covers.py --apply
    python scripts\\fetch_media_covers.py --only anime --delay 1.0
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.fetch_media_covers import (  # noqa: E402
    ROOT as FETCH_ROOT,
    _load_meta,
    _save_meta,
    _titles_compatible,
)


def _has_file(cover_path: str) -> bool:
    if not cover_path.startswith("/static/"):
        return False
    return (FETCH_ROOT / cover_path.lstrip("/")).is_file()


# Subtitle still equals one of these → clear (legacy wrong hits).
KNOWN_BAD_SUBS: dict[str, set[str]] = {
    "Re：从零开始的异世界生活 Memory Snow(雪之会议)": {"レレレの天才バカボン"},
    "一起一起这里那里": {"로보카 폴리"},
    "三坪房间的侵略者！": {"ナノ・インベーダーズ"},
    "冰属性男子和酷酷女同事": {"めぞん一刻"},
    "品酒要在成为夫妻后": {"ダーティペア the Movie", "ダーティペア"},
    "夏日幻魂": {"SLAM DUNK 吠えろバスケットマン魂! 花道と流川の熱き夏"},
    "这个美术社大有问题！": {"サーバント×サービス"},
    "邻桌的怪同学": {"黒と金の開かない鍵。"},
    "酷爱电影的庞波小姐": {"小林さんちのメイドラゴン"},
    "青春之旅": {"最終楽章 響け！ユーフォニアム 前編"},
    "青春猪头少年不会梦到红书包女孩": {"小森さんは断れない！"},
    "100%鲜橙汁": {"South Block"},
    "超脱": {"间客"},
}

# Force-clear these titles regardless of current subtitle (confirmed wrong covers).
# Only titles still known-wrong after the latest refetch. Prefer rule-based
# clears (itunes mismatch / movie-anilist) for ongoing hygiene.
FORCE_CLEAR: dict[str, set[str]] = {
    "anime": set(),
    "movies": set(),
    "books": set(),
    "games": set(),
}


def _should_clear(kind: str, title: str, rec: dict) -> tuple[bool, str]:
    cover = (rec.get("cover_path") or "").strip()
    if not cover and not rec.get("matched") and not rec.get("checked"):
        return False, ""
    source = (rec.get("source") or "").strip().lower()
    subtitle = (rec.get("subtitle") or "").strip()

    if title in (FORCE_CLEAR.get(kind) or set()):
        return True, "force-clear"

    bad_subs = KNOWN_BAD_SUBS.get(title) or set()
    if subtitle and any(subtitle.startswith(b) or b in subtitle for b in bad_subs):
        return True, "known-bad-sub"

    if source in {"", "local"}:
        return True, "unprovenanced-local"

    # iTunes software store is full of mobile junk for PC game CN titles.
    # Require the store subtitle to match the EN Steam alias (not the CN title).
    if kind == "games" and source == "itunes_software":
        from scripts.fetch_media_covers import STEAM_TITLE_ALIASES

        alias = STEAM_TITLE_ALIASES.get(title, "")
        if alias:
            if not _titles_compatible(alias, subtitle or "", minimum=70):
                return True, "itunes-alias-mismatch"
        elif not subtitle or not _titles_compatible(title, subtitle, minimum=70):
            return True, "itunes-mismatch"

    # Live-action movies pulled from Anilist are almost always wrong.
    if kind == "movies" and source in {"anilist", "anilist_manga", "kitsu"}:
        anime_ok = {
            "声之形",
            "大鱼海棠",
            "天气之子",
            "姜子牙",
            "新神榜：哪吒重生",
            "浪浪山小妖怪",
            "海兽之子",
            "深海",
            "烟花",
            "白蛇2：青蛇劫起",
            "秒速五厘米",
            "罗小黑战记",
            "罗小黑战记2",
            "言语如苏打般涌现",
            "通往夏天的隧道",
            "间谍过家家 代号：白",
            "情书",
        }
        if title not in anime_ok:
            return True, "movie-anilist-liveaction"

    if kind == "books" and source == "itunes" and subtitle:
        # Author field wrongly matched to unrelated Western author.
        if not _titles_compatible(title, subtitle, minimum=40):
            # Keep when subtitle looks like a real CN/JP author already on the list.
            from scripts.fetch_media_covers import BOOK_TITLE_ALIASES

            alias = BOOK_TITLE_ALIASES.get(title, "")
            if alias and _titles_compatible(alias, subtitle, minimum=40):
                return False, ""
            # Only force when we already listed it, or latin author + CJK title with no alias hit.
            if title in (FORCE_CLEAR.get("books") or set()):
                return True, "book-author-mismatch"

    if rec.get("matched") and cover and not _has_file(cover):
        return True, "missing-file"
    return False, ""


def repair_kind(kind: str, apply: bool) -> dict:
    meta = _load_meta(kind)
    bucket = meta.setdefault("items", {})
    cleared = 0
    kept = 0
    reasons: dict[str, int] = {}
    deleted_files = 0
    for title, rec in list(bucket.items()):
        if not isinstance(rec, dict):
            continue
        bad, reason = _should_clear(kind, title, rec)
        if not bad:
            if (rec.get("cover_path") or "").strip():
                kept += 1
            continue
        reasons[reason] = reasons.get(reason, 0) + 1
        cleared += 1
        cover = (rec.get("cover_path") or "").strip()
        if apply:
            if cover.startswith("/static/") and _has_file(cover):
                path = FETCH_ROOT / cover.lstrip("/")
                try:
                    path.unlink()
                    deleted_files += 1
                except OSError:
                    pass
            rec.update(
                {
                    "matched": False,
                    "checked": False,
                    "cover_path": "",
                    "subtitle": "",
                    "score": None,
                    "episodes": None,
                    "year": None,
                    "date": "",
                    "tags": [],
                    "source": "",
                    "source_id": "",
                    "format": "",
                }
            )
            bucket[title] = rec
    if apply:
        _save_meta(kind, meta)
    return {
        "kind": kind,
        "cleared": cleared,
        "kept": kept,
        "deleted_files": deleted_files,
        "reasons": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Clear mismatched media covers for re-fetch")
    parser.add_argument("--apply", action="store_true", help="actually delete bad covers/meta")
    parser.add_argument(
        "--only",
        choices=["anime", "games", "books", "movies", "all"],
        default="all",
    )
    args = parser.parse_args()
    kinds = ["anime", "games", "books", "movies"] if args.only == "all" else [args.only]
    print(f"MODE={'APPLY' if args.apply else 'DRY-RUN'} kinds={kinds}")
    for kind in kinds:
        stats = repair_kind(kind, apply=args.apply)
        print(
            f"{kind}: clear={stats['cleared']} keep={stats['kept']} "
            f"deleted_files={stats['deleted_files']} reasons={stats['reasons']}"
        )
    if not args.apply:
        print("Re-run with --apply to commit, then fetch_media_covers.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
