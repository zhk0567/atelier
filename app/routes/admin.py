"""Hidden administrator console for quiz attempt records."""

from __future__ import annotations

import csv
import io
import math
from datetime import datetime

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from app.admin_auth import (
    ADMIN_PATH,
    admin_csrf_token,
    admin_session_ok,
    clear_admin_session,
    clear_login_failures,
    client_ip,
    csrf_valid,
    login_limited,
    record_login_failure,
    set_admin_session,
    set_csrf_cookie,
    verify_credentials,
)
from app.constants import SITE_NAME
from app.context import templates
from app.quiz_data import (
    GROUPS,
    answer_rows,
    dimension_details,
    score_answers,
)
from app.quiz_store import (
    all_attempts,
    dashboard_stats,
    get_attempt_by_id,
    list_attempts,
)

router = APIRouter(include_in_schema=False)

_ADMIN_HEADERS = {
    "Cache-Control": "no-store, max-age=0",
    "Pragma": "no-cache",
    "X-Robots-Tag": "noindex, nofollow, noarchive",
    "Referrer-Policy": "no-referrer",
}

_PAGE_SIZE = 50


def _csv_safe(value: object) -> str:
    text = "" if value is None else str(value)
    return "'" + text if text.startswith(("=", "+", "-", "@")) else text


def _login_response(
    request: Request,
    *,
    error: str = "",
    status_code: int = 200,
) -> HTMLResponse:
    response = templates.TemplateResponse(
        request=request,
        name="admin_login.html",
        context={
            "site_name": SITE_NAME,
            "admin_path": ADMIN_PATH,
            "csrf_token": admin_csrf_token(),
            "error": error,
        },
        status_code=status_code,
        headers=_ADMIN_HEADERS,
    )
    set_csrf_cookie(response)
    return response


def _dashboard_response(
    request: Request,
    *,
    query: str = "",
    page: int = 1,
    status_code: int = 200,
) -> HTMLResponse:
    query = query.strip()[:80]
    page = max(1, int(page))
    offset = (page - 1) * _PAGE_SIZE
    records, total = list_attempts(
        query=query,
        limit=_PAGE_SIZE,
        offset=offset,
    )
    pages = max(1, math.ceil(total / _PAGE_SIZE))
    if page > pages and total:
        page = pages
        offset = (page - 1) * _PAGE_SIZE
        records, total = list_attempts(
            query=query,
            limit=_PAGE_SIZE,
            offset=offset,
        )
    response = templates.TemplateResponse(
        request=request,
        name="admin_dashboard.html",
        context={
            "site_name": SITE_NAME,
            "admin_path": ADMIN_PATH,
            "csrf_token": admin_csrf_token(),
            "records": records,
            "stats": dashboard_stats(),
            "query": query,
            "page": page,
            "pages": pages,
            "total": total,
            "page_size": _PAGE_SIZE,
            "group_names": {key: value["name"] for key, value in GROUPS.items()},
        },
        status_code=status_code,
        headers=_ADMIN_HEADERS,
    )
    set_csrf_cookie(response)
    return response


@router.get(ADMIN_PATH, response_class=HTMLResponse)
async def admin_home(
    request: Request,
    q: str = "",
    page: int = 1,
):
    if not admin_session_ok(request):
        return _login_response(request)
    return _dashboard_response(request, query=q, page=page)


@router.post(ADMIN_PATH + "/login")
async def admin_login(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    csrf: str = Form(""),
):
    ip = client_ip(request)
    if login_limited(ip):
        return _login_response(
            request,
            error="尝试次数过多，请十分钟后再试。",
            status_code=429,
        )
    if not csrf_valid(request, csrf):
        return _login_response(
            request,
            error="登录页面已过期，请重新打开入口。",
            status_code=400,
        )
    if not verify_credentials(username.strip(), password):
        record_login_failure(ip)
        return _login_response(
            request,
            error="账号或密码错误。",
            status_code=401,
        )
    clear_login_failures(ip)
    response = RedirectResponse(url=ADMIN_PATH, status_code=303)
    set_admin_session(response, request)
    return response


@router.post(ADMIN_PATH + "/logout")
async def admin_logout(request: Request, csrf: str = Form("")):
    if not admin_session_ok(request):
        return RedirectResponse(url=ADMIN_PATH, status_code=303)
    if not csrf_valid(request, csrf):
        raise HTTPException(status_code=400)
    response = RedirectResponse(url=ADMIN_PATH, status_code=303)
    clear_admin_session(response)
    return response


@router.get(ADMIN_PATH + "/attempt/{attempt_id}", response_class=HTMLResponse)
async def admin_attempt(request: Request, attempt_id: int):
    if not admin_session_ok(request):
        return RedirectResponse(url=ADMIN_PATH, status_code=303)
    record = get_attempt_by_id(attempt_id)
    if not record:
        raise HTTPException(status_code=404)
    result = score_answers(record["answers"])
    dimensions = dimension_details(
        result["group_scores"],
        result["group_max_scores"],
        result["top_dimensions"],
    )
    response = templates.TemplateResponse(
        request=request,
        name="admin_attempt.html",
        context={
            "site_name": SITE_NAME,
            "admin_path": ADMIN_PATH,
            "csrf_token": admin_csrf_token(),
            "record": record,
            "result": result,
            "dimensions": dimensions,
            "answer_rows": answer_rows(record["answers"]),
        },
        headers=_ADMIN_HEADERS,
    )
    set_csrf_cookie(response)
    return response


@router.get(ADMIN_PATH + "/export.csv")
async def admin_export(request: Request):
    if not admin_session_ok(request):
        return RedirectResponse(url=ADMIN_PATH, status_code=303)
    records = all_attempts()
    output = io.StringIO()
    output.write("\ufeff")
    writer = csv.writer(output)
    writer.writerow(
        [
            "ID",
            "提交时间",
            "昵称/代号",
            "班级/学号",
            "得分",
            "满分",
            "结果",
            "分数段",
            "主导维度",
            "注意力检测",
            "答题用时(秒)",
            "逐题答案",
        ]
    )
    for record in records:
        writer.writerow(
            [
                record["id"],
                record["created_at"],
                _csv_safe(record["name"]),
                _csv_safe(record["identifier"]),
                record["score"],
                record["max_score"],
                _csv_safe(record["band_title"]),
                record["band_range"],
                _csv_safe(
                    "/".join(
                        GROUPS[group_id]["name"]
                        for group_id in record["top_dimensions"]
                        if group_id in GROUPS
                    )
                ),
                record["attention_choice"],
                record["duration_seconds"],
                " ".join(
                    f"{row['number']}:{row['choice'] or '-'}"
                    for row in answer_rows(record["answers"])
                ),
            ]
        )
    filename = f"neurosis-attempts-{datetime.now().astimezone().date().isoformat()}.csv"
    return Response(
        content=output.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={
            **_ADMIN_HEADERS,
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )
