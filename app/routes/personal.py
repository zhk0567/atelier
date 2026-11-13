from __future__ import annotations

import re
import time
from threading import Lock

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from app.admin_auth import client_ip
from app.constants import HTML_NO_CACHE
from app.context import site_context, templates
from app.personal import load_personal, personal_stats
from app.wishes_store import approved_wishes, save_wish

router = APIRouter()

WISH_PATH = "/personal/wish"
_WISH_MIN = 2
_WISH_MAX = 280
_NAME_MAX = 20

_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

_WISH_LOCK = Lock()
_WISH_HITS: dict[str, list[float]] = {}
_WISH_WINDOW = 10 * 60
_WISH_MAX_PER_WINDOW = 5


def _clean_line(value: str, limit: int) -> str:
    text = _CONTROL.sub("", value or "")
    return " ".join(text.split())[:limit]


def _clean_wish(value: str) -> str:
    text = _CONTROL.sub("", (value or "").replace("\r\n", "\n").replace("\r", "\n"))
    lines = [" ".join(line.split()) for line in text.split("\n")]
    return "\n".join(line for line in lines if line)[:_WISH_MAX]


def _wish_limited(ip: str) -> bool:
    now = time.monotonic()
    with _WISH_LOCK:
        hits = [stamp for stamp in _WISH_HITS.get(ip, []) if now - stamp < _WISH_WINDOW]
        _WISH_HITS[ip] = hits
        return len(hits) >= _WISH_MAX_PER_WINDOW


def _record_wish(ip: str) -> None:
    now = time.monotonic()
    with _WISH_LOCK:
        hits = [stamp for stamp in _WISH_HITS.get(ip, []) if now - stamp < _WISH_WINDOW]
        hits.append(now)
        _WISH_HITS[ip] = hits[-_WISH_MAX_PER_WINDOW:]
        if len(_WISH_HITS) > 5000:
            for key in [k for k, v in _WISH_HITS.items() if not v]:
                _WISH_HITS.pop(key, None)


def _public_wishes() -> list[dict]:
    rows = approved_wishes(60)
    for row in rows:
        row["display_name"] = row.get("name") or "匿名"
        stamp = row.get("published_at") or row.get("created_at") or ""
        row["published_date"] = stamp[:10].replace("-", ".")
    return rows


def _wants_json(request: Request) -> bool:
    return "application/json" in request.headers.get("accept", "").lower()


def _wish_context() -> dict:
    return {
        **site_context(),
        "page_personal": True,
        "wish_path": WISH_PATH,
        "wish_max": _WISH_MAX,
        "wish_min": _WISH_MIN,
        "name_max": _NAME_MAX,
    }


def _render_wish_page(
    request: Request,
    *,
    name: str = "",
    wish: str = "",
    error: str = "",
    status_code: int = 200,
) -> HTMLResponse:
    response = templates.TemplateResponse(
        request=request,
        name="personal_wish.html",
        context={
            **_wish_context(),
            "wish_name": name,
            "wish_text": wish,
            "error": error,
        },
        status_code=status_code,
        headers=HTML_NO_CACHE,
    )
    return response


@router.get("/personal", response_class=HTMLResponse)
async def personal_page(request: Request, wish_sent: int = 0):
    personal = load_personal()
    wishes = _public_wishes()
    return templates.TemplateResponse(
        request=request,
        name="personal.html",
        context={
            **site_context(),
            "page_personal": True,
            "personal": personal,
            "personal_stats": personal_stats(personal),
            "personal_wishes": wishes,
            "wish_sent": bool(wish_sent),
            "wish_path": WISH_PATH,
        },
        headers=HTML_NO_CACHE,
    )


@router.get(WISH_PATH, response_class=HTMLResponse)
async def wish_form(request: Request):
    return _render_wish_page(request)


@router.post(WISH_PATH)
async def wish_submit(request: Request):
    form = await request.form()
    name = _clean_line(str(form.get("name", "")), _NAME_MAX)
    wish = _clean_wish(str(form.get("wish", "")))
    honeypot = str(form.get("website", "")).strip()
    wants_json = _wants_json(request)

    def fail(message: str, status_code: int) -> HTMLResponse | JSONResponse:
        if wants_json:
            return JSONResponse(
                {"ok": False, "error": message},
                status_code=status_code,
                headers=HTML_NO_CACHE,
            )
        return _render_wish_page(
            request,
            name=name,
            wish=wish,
            error=message,
            status_code=status_code,
        )

    if honeypot:
        # Bots fill hidden fields; accept silently so they do not retry.
        if wants_json:
            return JSONResponse({"ok": True, "message": "已收到。"}, headers=HTML_NO_CACHE)
        return RedirectResponse(url="/personal?wish_sent=1#wishes", status_code=303)

    ip = client_ip(request)
    if _wish_limited(ip):
        return fail("提交得有点快，十分钟后再试。", 429)

    if len(wish) < _WISH_MIN:
        return fail(f"至少写 {_WISH_MIN} 个字吧。", 422)

    try:
        save_wish(
            name=name,
            wish=wish,
            source=request.headers.get("referer", "")[:300],
            user_agent=request.headers.get("user-agent", ""),
        )
    except Exception as exc:
        print(f"[atelier] save_wish failed: {exc}", flush=True)
        return fail("服务器刚才没接住，稍后再试一次。", 503)

    _record_wish(ip)
    if wants_json:
        return JSONResponse(
            {
                "ok": True,
                "message": "收到了。审核通过后，它会出现在页面最下面。",
            },
            headers=HTML_NO_CACHE,
        )
    return RedirectResponse(url="/personal?wish_sent=1#wishes", status_code=303)
