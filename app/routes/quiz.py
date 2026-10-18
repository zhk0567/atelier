"""Interactive quiz page, server-side scoring, and result lookup."""

from __future__ import annotations

import random
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from app.context import site_context, templates
from app.quiz_data import (
    GROUPS,
    GROUP_ORDER,
    QUESTIONS,
    QUIZ_INTRO,
    QUIZ_MAX_SCORE,
    QUIZ_NOTE,
    QUIZ_PATH,
    QUIZ_TITLE,
    dimension_details,
    score_answers,
)
from app.quiz_store import get_attempt_by_token, save_attempt

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
    by_key = {question["key"]: question for question in QUESTIONS}
    keys = [key.strip() for key in order_raw.split(",") if key.strip()]
    if len(keys) == len(QUESTIONS) and set(keys) == set(by_key):
        return [by_key[key] for key in keys]
    questions = list(QUESTIONS)
    random.SystemRandom().shuffle(questions)
    return questions


def _render_quiz(
    request: Request,
    *,
    answers: dict[str, str] | None = None,
    name: str = "",
    identifier: str = "",
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
            "quiz_intro": QUIZ_INTRO,
            "quiz_note": QUIZ_NOTE,
            "quiz_max_score": QUIZ_MAX_SCORE,
            "questions": ordered_questions,
            "question_order": order_value,
            "groups": GROUPS,
            "group_order": GROUP_ORDER,
            "page_quiz": True,
            "answers": answers or {},
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


@router.post(QUIZ_PATH + "/submit")
async def quiz_submit(request: Request):
    form = await request.form()
    name = _clean_text(_form_text(form, "name"), 40)
    identifier = _clean_text(_form_text(form, "identifier"), 60)
    question_order = _form_text(form, "order")
    answers: dict[str, str] = {}
    missing: list[int] = []

    for question in QUESTIONS:
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
            error="请先填写昵称或代号，再提交答卷。",
            question_order=question_order,
            status_code=422,
        )
    if missing:
        return _render_quiz(
            request,
            answers=answers,
            name=name,
            identifier=identifier,
            error=f"还有 {len(missing)} 道题未作答，请补全后再提交。",
            question_order=question_order,
            status_code=422,
        )

    try:
        duration_seconds = int(_form_text(form, "duration_seconds") or "0")
    except ValueError:
        duration_seconds = 0

    result = score_answers(answers)
    token = save_attempt(
        name=name,
        identifier=identifier,
        answers=answers,
        result=result,
        duration_seconds=duration_seconds,
        user_agent=request.headers.get("user-agent", ""),
    )
    return RedirectResponse(url=f"{QUIZ_PATH}/result/{token}", status_code=303)


@router.get(QUIZ_PATH + "/result/{token}", response_class=HTMLResponse)
async def quiz_result(request: Request, token: str):
    record = get_attempt_by_token(token)
    if not record:
        raise HTTPException(status_code=404)
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
        f"我测出来是【{result['band']['title']}】，"
        f"主导维度：{top_names}。"
        f"你呢？{request.url_for('quiz_page')}"
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
