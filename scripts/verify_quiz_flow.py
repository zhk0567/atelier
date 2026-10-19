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
            assert "2026-10-19-v4" in privacy.text

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

            csrf = admin_csrf_token()
            client.cookies.set("atelier_admin_session", create_session_token())
            client.cookies.set("atelier_admin_csrf", csrf)
            dashboard = client.get("/ops/neurosis-7f3c9a2e")
            assert dashboard.status_code == 200
            assert "自动化测试" in dashboard.text

            match = re.search(r'/attempt/(\d+)"', dashboard.text)
            assert match is not None
            attempt_id = int(match.group(1))
            detail = client.get(f"/ops/neurosis-7f3c9a2e/attempt/{attempt_id}")
            assert detail.status_code == 200
            assert "删除记录" in detail.text
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
