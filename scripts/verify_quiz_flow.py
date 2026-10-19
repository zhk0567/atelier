"""Smoke-test the quiz submission, user lookup, and admin deletion flow."""

from __future__ import annotations

import os
import re
import sys
import tempfile
from pathlib import Path


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="atelier-quiz-") as temp_dir:
        os.environ["ATELIER_QUIZ_DB"] = str(Path(temp_dir) / "quiz.sqlite3")
        project_root = Path(__file__).resolve().parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        from fastapi.testclient import TestClient

        from app import app
        from app.admin_auth import admin_csrf_token, create_session_token
        from app.quiz_data import (
            ATTENTION_BY_KEY,
            ATTEMPT_QUESTION_COUNT,
            QUESTIONS,
            build_attempt_questions,
        )

        with TestClient(app) as client:
            assert len(QUESTIONS) == 120
            sample = build_attempt_questions()
            assert len(sample) == ATTEMPT_QUESTION_COUNT == 30
            assert sum(question["group"] == "attention" for question in sample) == 1

            landing = client.get("/quiz/neurosis")
            assert landing.status_code == 200
            assert 'name="consent"' in landing.text
            assert "data-nq-consent-card" in landing.text
            assert landing.text.count("data-nq-slide") == 30
            order_match = re.search(r'name="order" value="([^"]+)"', landing.text)
            assert order_match is not None
            order_value = order_match.group(1)
            selected_keys = order_value.split(",")
            assert len(selected_keys) == 30
            assert len(set(selected_keys)) == 30
            assert sum(key in ATTENTION_BY_KEY for key in selected_keys) == 1
            privacy = client.get("/quiz/neurosis/privacy")
            assert privacy.status_code == 200
            assert "2026-10-20-v5" in privacy.text

            form = {
                "name": "自动化测试",
                "identifier": "TEST-2026",
                "consent": "yes",
                "duration_seconds": "42",
                "order": order_value,
                **{
                    key: (
                        ATTENTION_BY_KEY[key]["correct"]
                        if key in ATTENTION_BY_KEY
                        else "C"
                    )
                    for key in selected_keys
                },
            }
            submit = client.post(
                "/quiz/neurosis/submit",
                data=form,
                follow_redirects=False,
            )
            assert submit.status_code == 303
            result_url = submit.headers["location"]
            result = client.get(result_url)
            assert result.status_code == 200
            for marker in (
                "nq-gauge",
                "状态说明书",
                "内耗组合技",
                "7 DAY RESET",
                "data-nq-plan-token",
            ):
                assert marker in result.text, marker

            with TestClient(app) as anonymous:
                direct = anonymous.get(result_url)
                assert direct.status_code == 403
                assert "两项都匹配后才能查看" in direct.text

                missing_submit_identifier = dict(form)
                missing_submit_identifier["identifier"] = ""
                blocked_submit = anonymous.post(
                    "/quiz/neurosis/submit",
                    data=missing_submit_identifier,
                    follow_redirects=False,
                )
                assert blocked_submit.status_code == 422
                assert "请填写学号" in blocked_submit.text

                wrong_name = anonymous.post(
                    "/quiz/neurosis/records",
                    data={"name": "错误昵称", "identifier": "TEST-2026"},
                )
                assert "没有找到匹配记录" in wrong_name.text
                wrong_identifier = anonymous.post(
                    "/quiz/neurosis/records",
                    data={"name": "自动化测试", "identifier": "WRONG-ID"},
                )
                assert "没有找到匹配记录" in wrong_identifier.text
                missing_identifier = anonymous.post(
                    "/quiz/neurosis/records",
                    data={"name": "自动化测试", "identifier": ""},
                )
                assert missing_identifier.status_code == 422

                verified = anonymous.post(
                    "/quiz/neurosis/records",
                    data={"name": "自动化测试", "identifier": "TEST-2026"},
                )
                assert verified.status_code == 200
                assert anonymous.get(result_url).status_code == 200

            lookup = client.post(
                "/quiz/neurosis/records",
                data={"name": "自动化测试", "identifier": "TEST-2026"},
            )
            assert lookup.status_code == 200
            assert "查看结果" in lookup.text
            assert "/delete" not in lookup.text

            feedback_page = client.get("/quiz/neurosis/feedback")
            assert feedback_page.status_code == 200
            assert 'name="category"' in feedback_page.text
            assert 'name="message"' in feedback_page.text
            feedback_message = "自动化反馈：提交结果页排版有一点问题。"
            feedback_submit = client.post(
                "/quiz/neurosis/feedback",
                data={
                    "category": "问题反馈",
                    "name": "反馈测试用户",
                    "identifier": "FB-2026",
                    "message": feedback_message,
                    "website": "",
                },
                follow_redirects=False,
            )
            assert feedback_submit.status_code == 303
            feedback_sent = client.get("/quiz/neurosis/feedback?sent=1")
            assert "反馈已收到" in feedback_sent.text

            login_page = client.get("/ops/neurosis-7f3c9a2e")
            assert login_page.status_code == 200
            assert 'name="account"' in login_page.text
            assert 'name="passphrase"' in login_page.text
            assert 'autocomplete="new-password"' in login_page.text
            assert "data-login-credential" in login_page.text
            assert 'name="username"' not in login_page.text
            assert 'name="password"' not in login_page.text

            login_csrf = client.cookies.get("atelier_admin_csrf")
            rejected_login = client.post(
                "/ops/neurosis-7f3c9a2e/login",
                data={
                    "account": "wrong-account",
                    "passphrase": "wrong-passphrase",
                    "csrf": login_csrf,
                },
            )
            assert rejected_login.status_code == 401

            csrf = admin_csrf_token()
            client.cookies.set("atelier_admin_session", create_session_token())
            client.cookies.set("atelier_admin_csrf", csrf)
            dashboard = client.get("/ops/neurosis-7f3c9a2e")
            assert dashboard.status_code == 200
            assert "自动化测试" in dashboard.text
            assert "用户反馈" in dashboard.text

            match = re.search(r'/attempt/(\d+)"', dashboard.text)
            assert match is not None
            attempt_id = int(match.group(1))
            admin_note = "自动化备注：高中同学"
            note_saved = client.post(
                f"/ops/neurosis-7f3c9a2e/attempt/{attempt_id}/note",
                data={"csrf": csrf, "note": admin_note, "return_to": "dashboard"},
                follow_redirects=False,
            )
            assert note_saved.status_code == 303
            note_search = client.get(
                "/ops/neurosis-7f3c9a2e",
                params={"q": admin_note},
            )
            assert admin_note in note_search.text
            assert admin_note not in client.get(result_url).text
            exported = client.get("/ops/neurosis-7f3c9a2e/export.csv")
            assert exported.status_code == 200
            assert admin_note in exported.text

            feedback_admin = client.get("/ops/neurosis-7f3c9a2e/feedback")
            assert feedback_admin.status_code == 200
            assert feedback_message in feedback_admin.text
            assert "待处理" in feedback_admin.text
            feedback_match = re.search(r'/feedback/(\d+)/status"', feedback_admin.text)
            assert feedback_match is not None
            feedback_id = int(feedback_match.group(1))
            feedback_status = client.post(
                f"/ops/neurosis-7f3c9a2e/feedback/{feedback_id}/status",
                data={"csrf": csrf, "status": "resolved"},
                follow_redirects=False,
            )
            assert feedback_status.status_code == 303
            resolved_feedback = client.get(
                "/ops/neurosis-7f3c9a2e/feedback",
                params={"status": "resolved"},
            )
            assert feedback_message in resolved_feedback.text
            feedback_delete = client.post(
                f"/ops/neurosis-7f3c9a2e/feedback/{feedback_id}/delete",
                data={"csrf": csrf},
                follow_redirects=False,
            )
            assert feedback_delete.status_code == 303
            deleted_feedback = client.get("/ops/neurosis-7f3c9a2e/feedback")
            assert feedback_message not in deleted_feedback.text

            detail = client.get(f"/ops/neurosis-7f3c9a2e/attempt/{attempt_id}")
            assert detail.status_code == 200
            assert "删除记录" in detail.text
            assert admin_note in detail.text
            deleted = client.post(
                f"/ops/neurosis-7f3c9a2e/attempt/{attempt_id}/delete",
                data={"csrf": csrf},
                follow_redirects=False,
            )
            assert deleted.status_code == 303
            assert client.get(result_url).status_code == 404

            lookup_after = client.post(
                "/quiz/neurosis/records",
                data={"name": "自动化测试", "identifier": "TEST-2026"},
            )
            assert "没有找到匹配记录" in lookup_after.text

        print("quiz flow ok: submit -> result -> lookup -> admin delete -> lookup empty")


if __name__ == "__main__":
    main()
