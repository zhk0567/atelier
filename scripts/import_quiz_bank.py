"""Import the 120-question markdown bank into the app's JSON data file."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

GROUP_KEYS = (
    "social",
    "rumination",
    "existential",
    "action",
    "attachment",
    "core",
)

QUESTION_RE = re.compile(r"^\*\*(\d+)\.\s+(.+?)\*\*\s*$")
OPTION_RE = re.compile(r"^([ABCD])\.\s+(.+?)\s*$")


def _title_from_prompt(prompt: str, number: int) -> str:
    head = re.split(r"[：？?]", prompt, maxsplit=1)[0].strip("，。；： ")
    if len(head) > 20:
        first_clause = re.split(r"[，,]", head, maxsplit=1)[0].strip()
        if len(first_clause) >= 4:
            head = first_clause
    if len(head) > 20:
        head = head[:18].rstrip("，。；： ") + "…"
    return head if len(head) >= 4 else f"情境 {number}"


def parse_bank(text: str) -> list[dict]:
    group_index = -1
    current: dict | None = None
    questions: list[dict] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("### 维度"):
            group_index += 1
            current = None
            continue

        question_match = QUESTION_RE.match(line)
        if question_match:
            number = int(question_match.group(1))
            prompt = question_match.group(2).strip()
            current = {
                "number": number,
                "group": GROUP_KEYS[group_index],
                "title": _title_from_prompt(prompt, number),
                "prompt": prompt,
                "options": [],
            }
            questions.append(current)
            continue

        option_match = OPTION_RE.match(line)
        if option_match and current and len(current["options"]) < 4:
            current["options"].append(option_match.group(2))

    if len(questions) != 120:
        raise ValueError(f"Expected 120 questions, found {len(questions)}")
    if [q["number"] for q in questions] != list(range(1, 121)):
        raise ValueError("Question numbers must run from 1 to 120")
    for question in questions:
        if len(question["options"]) != 4:
            raise ValueError(f"Question {question['number']} must have four options")

    for group in GROUP_KEYS:
        count = sum(question["group"] == group for question in questions)
        if count != 20:
            raise ValueError(f"Group {group} must contain 20 questions, found {count}")

    return questions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("app/quiz_bank.json"),
    )
    args = parser.parse_args()

    questions = parse_bank(args.source.read_text(encoding="utf-8"))
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(questions, ensure_ascii=False, indent=2) + "\n")
    print(f"Wrote {len(questions)} questions to {args.output}")


if __name__ == "__main__":
    main()
