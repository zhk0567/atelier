"""Interactive quiz page, server-side scoring, and result lookup."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.config import ATELIER_ROOT
from app.context import site_context, templates
from app.markdown.render import markdown_to_html, postprocess_content_html
from app.quiz_access import grant_result_access, has_result_access
from app.quiz_data import (
    GROUPS,
    GROUP_ORDER,
    LEGACY_GROUP_NAMES,
    PRIVACY_DOC,
    PRIVACY_VERSION,
    QUIZ_INTRO,
    QUIZ_MAX_SCORE,
    QUIZ_NOTE,
    QUIZ_PATH,
    QUIZ_TITLE,
    QUIZ_VERSION,
    build_attempt_questions,
    dimension_details,
    selection_from_order,
    score_answers,
)
from app.quiz_store import get_attempt_by_token, list_user_attempts, save_attempt

router = APIRouter()

_NO_STORE_HEADERS = {
    "Cache-Control": "no-store, max-age=0",
    "Pragma": "no-cache",
    "X-Robots-Tag": "noindex, nofollow, noarchive",
    "Referrer-Policy": "no-referrer",
}


def _form_text(form: Any, key: str) -> str:
    value = form.get(key, "")
    return value if isinstance(value, str) else ""


def _clean_text(value: str, max_length: int) -> str:
    return " ".join(value.split())[:max_length]


def _ordered_questions(order_raw: str = "") -> list[dict[str, Any]]:
    selected = selection_from_order(order_raw)
    return selected if selected is not None else build_attempt_questions()


def _render_quiz(
    request: Request,
    *,
    answers: dict[str, str] | None = None,
    name: str = "",
    identifier: str = "",
    consent: bool = False,
    error: str = "",
    question_order: str = "",
    status_code: int = 200,
) -> HTMLResponse:
    ordered_questions = _ordered_questions(question_order)
    order_value = ",".join(question["key"] for question in ordered_questions)
    return templates.TemplateResponse(
        request=request,
        name="quiz_neurosis.html",
        context={
            **site_context(),
            "quiz_title": QUIZ_TITLE,
            "quiz_path": QUIZ_PATH,
            "privacy_path": f"{QUIZ_PATH}/privacy",
            "privacy_version": PRIVACY_VERSION,
            "quiz_intro": QUIZ_INTRO,
            "quiz_note": QUIZ_NOTE,
            "quiz_max_score": QUIZ_MAX_SCORE,
            "questions": ordered_questions,
            "question_order": order_value,
            "groups": GROUPS,
            "group_order": GROUP_ORDER,
            "page_quiz": True,
            "answers": answers or {},
            "consent": consent,
            "student_name": name,
            "student_identifier": identifier,
            "error": error,
        },
        status_code=status_code,
        headers=_NO_STORE_HEADERS,
    )


@router.get(QUIZ_PATH, response_class=HTMLResponse)
async def quiz_page(request: Request):
    return _render_quiz(request)


@router.get(QUIZ_PATH + "/privacy", response_class=HTMLResponse)
async def quiz_privacy(request: Request):
    raw = (ATELIER_ROOT / PRIVACY_DOC).read_text(encoding="utf-8")
    html_body, _ = postprocess_content_html(
        markdown_to_html(raw),
        heading_tags=("h2", "h3"),
    )
    return templates.TemplateResponse(
        request=request,
        name="quiz_privacy.html",
        context={
            **site_context(),
            "page_quiz": True,
            "quiz_title": QUIZ_TITLE,
            "quiz_path": QUIZ_PATH,
            "privacy_version": PRIVACY_VERSION,
            "privacy_html": html_body,
        },
        headers=_NO_STORE_HEADERS,
    )


def _render_records(
    request: Request,
    *,
    name: str = "",
    identifier: str = "",
    records: list[dict[str, Any]] | None = None,
    error: str = "",
    status_code: int = 200,
) -> HTMLResponse:
    enriched: list[dict[str, Any]] = []
    group_names = {key: value["name"] for key, value in GROUPS.items()}
    for record in records or []:
        is_legacy = record.get("quiz_version") != QUIZ_VERSION
        names = LEGACY_GROUP_NAMES if is_legacy else group_names
        max_score = max(1, int(record.get("max_score") or 1))
        enriched.append(
            {
                **record,
                "is_legacy": is_legacy,
                "score_percent": round(int(record.get("score") or 0) / max_score * 100),
                "dimension_names": [
                    names.get(group_id, group_id)
                    for group_id in record.get("top_dimensions", [])
                ],
            }
        )
    return templates.TemplateResponse(
        request=request,
        name="quiz_records.html",
        context={
            **site_context(),
            "page_quiz": True,
            "quiz_title": QUIZ_TITLE,
            "quiz_path": QUIZ_PATH,
            "privacy_path": f"{QUIZ_PATH}/privacy",
            "lookup_name": name,
            "lookup_identifier": identifier,
            "records": enriched,
            "error": error,
            "groups": GROUPS,
            "legacy_groups": LEGACY_GROUP_NAMES,
        },
        status_code=status_code,
        headers=_NO_STORE_HEADERS,
    )


@router.get(QUIZ_PATH + "/records", response_class=HTMLResponse)
async def quiz_records_page(request: Request):
    return _render_records(request)


@router.post(QUIZ_PATH + "/records", response_class=HTMLResponse)
async def quiz_records_lookup(request: Request):
    form = await request.form()
    name = _clean_text(_form_text(form, "name"), 40)
    identifier = _clean_text(_form_text(form, "identifier"), 60)
    if not name or not identifier:
        return _render_records(
            request,
            name=name,
            identifier=identifier,
            error="请同时填写昵称和学号/查询码，才能查看自己的记录。",
            status_code=422,
        )
    records = list_user_attempts(name, identifier)
    response = _render_records(
        request,
        name=name,
        identifier=identifier,
        records=records,
    )
    grant_result_access(
        response,
        request,
        [record["token"] for record in records],
    )
    return response


@router.post(QUIZ_PATH + "/submit")
async def quiz_submit(request: Request):
    form = await request.form()
    name = _clean_text(_form_text(form, "name"), 40)
    identifier = _clean_text(_form_text(form, "identifier"), 60)
    question_order = _form_text(form, "order")
    consent = _form_text(form, "consent") == "yes"
    answers: dict[str, str] = {}
    missing: list[int] = []

    selected = selection_from_order(question_order)
    if selected is None:
        return _render_quiz(
            request,
            name=name,
            identifier=identifier,
            consent=consent,
            error="本轮题目信息已失效，请重新开始测试。",
            status_code=422,
        )

    for question in selected:
        choice = _form_text(form, question["key"]).strip().upper()
        if choice not in ("A", "B", "C", "D"):
            missing.append(int(question["number"]))
        else:
            answers[question["key"]] = choice

    if not name:
        return _render_quiz(
            request,
            answers=answers,
            name=name,
            identifier=identifier,
            consent=consent,
            error="请先填写昵称或代号，再提交答卷。",
            question_order=question_order,
            status_code=422,
        )
    if not identifier:
        return _render_quiz(
            request,
            answers=answers,
            name=name,
            identifier=identifier,
            consent=consent,
            error="请填写学号/查询码，用于之后找回答题记录。",
            question_order=question_order,
            status_code=422,
        )
    if not consent:
        return _render_quiz(
            request,
            answers=answers,
            name=name,
            identifier=identifier,
            consent=False,
            error="请先阅读并同意《数据收集与隐私保护协议》，再提交答卷。",
            question_order=question_order,
            status_code=422,
        )
    if missing:
        return _render_quiz(
            request,
            answers=answers,
            name=name,
            identifier=identifier,
            consent=consent,
            error=f"还有 {len(missing)} 道题未作答，请补全后再提交。",
            question_order=question_order,
            status_code=422,
        )

    try:
        duration_seconds = int(_form_text(form, "duration_seconds") or "0")
    except ValueError:
        duration_seconds = 0

    result = score_answers(answers)
    consent_at = datetime.now().astimezone().isoformat(timespec="seconds")
    token = save_attempt(
        name=name,
        identifier=identifier,
        answers=answers,
        result=result,
        duration_seconds=duration_seconds,
        user_agent=request.headers.get("user-agent", ""),
        quiz_version=QUIZ_VERSION,
        consent_version=PRIVACY_VERSION,
        consent_at=consent_at,
    )
    response = RedirectResponse(url=f"{QUIZ_PATH}/result/{token}", status_code=303)
    grant_result_access(response, request, [token])
    return response


@router.get(QUIZ_PATH + "/result/{token}", response_class=HTMLResponse)
async def quiz_result(request: Request, token: str):
    record = get_attempt_by_token(token)
    if not record:
        raise HTTPException(status_code=404)
    if not has_result_access(request, token):
        return _render_records(
            request,
            error="请先用提交时的昵称和学号/查询码验证身份；两项都匹配后才能查看这条结果。",
            status_code=403,
        )
    if record.get("quiz_version") != QUIZ_VERSION:
        legacy_top = "、".join(
            LEGACY_GROUP_NAMES.get(group_id, group_id)
            for group_id in record.get("top_dimensions", [])
        ) or "—"
        return templates.TemplateResponse(
            request=request,
            name="quiz_legacy_result.html",
            context={
                **site_context(),
                "page_quiz": True,
                "quiz_title": QUIZ_TITLE,
                "quiz_path": QUIZ_PATH,
                "record": record,
                "legacy_top": legacy_top,
            },
            headers=_NO_STORE_HEADERS,
        )
    result = score_answers(record["answers"])
    dimensions = dimension_details(
        result["group_scores"],
        result["group_max_scores"],
        result["top_dimensions"],
    )
    top_names = "、".join(
        GROUPS[group_id]["name"] for group_id in result["top_dimensions"]
    ) or "各维度均低"
    share_text = (
        f"我在《{QUIZ_TITLE}》里测出【{result['band']['title']}】，"
        f"精神电量 {result['energy']}%，主导维度：{top_names}。"
        f"你是哪一种？{request.url_for('quiz_page')}"
    )
    return templates.TemplateResponse(
        request=request,
        name="quiz_result.html",
        context={
            **site_context(),
            "quiz_title": QUIZ_TITLE,
            "quiz_path": QUIZ_PATH,
            "quiz_note": QUIZ_NOTE,
            "record": record,
            "result": result,
            "dimensions": dimensions,
            "groups": GROUPS,
            "share_text": share_text,
            "page_quiz": True,
        },
        headers=_NO_STORE_HEADERS,
    )
