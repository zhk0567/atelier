"""Lucky fortune-stick content for /fortune (entertainment only)."""

from __future__ import annotations

import json
import random
import re
from datetime import datetime
from functools import lru_cache
from typing import Any

from app.config import ATELIER_ROOT

FORTUNE_PATH = "/fortune"
FORTUNE_TITLE = "好运签"
DATA_PATH = ATELIER_ROOT / "data" / "fortune_sticks.json"

_ICON_FALLBACK = "crafting_table"

_LEVEL_BLURB = {
    "best": "上上开局，气场明亮。",
    "good": "吉意临门，宜主动一步。",
    "ok": "中平向好，稳中求进。",
    "mild": "小吉可喜，积少成多。",
    "plain": "平常即安，守中为上。",
    "low": "先安身心，来日可期。",
}

_SOFT_PAUSE = {
    "best": "吉意已足，不必再给自己加码焦虑。",
    "good": "好事在路上，先把眼前这一步走稳。",
    "ok": "不必强求立刻见效，给事情一点呼吸。",
    "mild": "小喜也够用，别把期待一下子拉满。",
    "plain": "平常心最好，今天适合守成与休整。",
    "low": "先把身心安顿好，重要决策可以明天再说。",
}

_DEFAULT_JOYS = [
    "今天也允许自己慢慢来。",
    "先把一件小事做开心。",
    "给自己留一口甜，再出门。",
    "温柔一点，也算胜利。",
    "先开心，再把事想清楚。",
]

# Pastel dimension readout — soft labels only (开心优先 · 仅供娱乐)
_TONE_SCORE = {
    "best": 5,
    "good": 4,
    "ok": 4,
    "mild": 3,
    "plain": 3,
    "low": 2,
}

_TONE_TAG = {
    "best": "上佳",
    "good": "向好",
    "ok": "平稳",
    "mild": "小吉",
    "plain": "平常",
    "low": "宜缓",
}

_DIM_META = (
    {"id": "overall", "label": "综合运势", "hue": "sky", "glyph": "★"},
    {"id": "love", "label": "爱情运势", "hue": "rose", "glyph": "♥"},
    {"id": "career", "label": "事业学业", "hue": "lilac", "glyph": "业"},
    {"id": "wealth", "label": "财富运势", "hue": "amber", "glyph": "¤"},
    {"id": "health", "label": "健康运势", "hue": "mint", "glyph": "+"},
)

_DIM_PROSE: dict[str, dict[str, tuple[str, ...]]] = {
    "overall": {
        "best": (
            "整体气场明亮，事务推进顺滑，适合把想做的事轻轻推进一步。",
            "今天运势偏开朗，日常小事也容易办成，保持轻松节奏即可。",
        ),
        "good": (
            "运势稳中带升，做事有回应；先完成一件小事，好运感会更清晰。",
            "整体向好，节奏舒服。把注意力放在眼前这一步，就够开心了。",
        ),
        "ok": (
            "整体平稳偏暖，日常事务可顺势推进，不必给自己加压。",
            "运势中平向好，适合稳稳做事、温柔对待自己。",
        ),
        "mild": (
            "小吉临门，积少成多。今天的小进展，也值得给自己鼓鼓掌。",
            "运势轻盈偏喜，适合把期待调成「刚好」，开心最重要。",
        ),
        "plain": (
            "平常即安。今天适合守成与休整，把心安顿好再出门。",
            "运势平和，没有大起大落。慢一点、稳一点，也是好运。",
        ),
        "low": (
            "先把身心安顿好，重要决定可以缓一缓；明天往往更清亮。",
            "今天宜轻装：少比较、多呼吸。照顾好自己，就是最好的运势。",
        ),
    },
    "love": {
        "best": (
            "情感气场温柔明亮。单身者易遇善意；有伴者适合真诚表达。",
            "心动信号偏清晰。自然相处、好好说话，比套路更灵。",
        ),
        "good": (
            "感情线向好，互动更轻松。一句关心，就能让关系暖起来。",
            "适合温和靠近：共同话题比开场白重要，慢一点更舒服。",
        ),
        "ok": (
            "情感平稳，没有大波动。单身宜自在；有伴宜互相体谅。",
            "中平偏暖。先把自己过好，缘分会跟得更轻松。",
        ),
        "mild": (
            "小确幸在靠近：一次愉快对话、一个微笑，都算收获。",
            "感情有轻喜，不必急着定性。收藏美好瞬间就很好。",
        ),
        "plain": (
            "感情线平常。先养自己的状态，比硬社交更吸引人。",
            "今日宜温柔自处。合适的相遇不怕晚一点。",
        ),
        "low": (
            "今天别硬凑热闹。状态不对就先回家，真正的缘分不怕晚。",
            "情感宜缓行：少内耗、多休息。把自己安好，比急着遇见更重要。",
        ),
    },
    "career": {
        "best": (
            "事业学业思路清晰、执行有力，适合推进关键任务或复习重点。",
            "学习工作气场开朗。先做最难那一件，后面会顺很多。",
        ),
        "good": (
            "进度有回应，协作也更顺。主动同步一句，能省半天扯皮。",
            "学业事业向好。把待办拆小，完成三件比空想十件更解压。",
        ),
        "ok": (
            "事业学业平稳推进。按清单走，完整比完美更重要。",
            "节奏踏实即可。卡住就换档，给大脑一点呼吸。",
        ),
        "mild": (
            "小进展可喜：修一个小问题、背完一页，也算胜利。",
            "事业学业轻升。积少成多，心态会更稳。",
        ),
        "plain": (
            "今天适合稳住节奏，别和别人的进度硬比。",
            "平常发挥就好。守住核心任务，比加码焦虑更有用。",
        ),
        "low": (
            "先减负：拒绝无效完美，保护精力也是职业技能。",
            "今天宜轻装推进。列三件明日必做，睡够再战更聪明。",
        ),
    },
    "wealth": {
        "best": (
            "财运气场开朗。到账前想清用途：必要优先，冲动往后排。",
            "进账征兆偏明。好运也要接得住——先稳现金流。",
        ),
        "good": (
            "财运向好，细水长流更安心。跟进一次未结事项往往更灵。",
            "收支节奏舒服。小惊喜可以开心收下，别扩大消费。",
        ),
        "ok": (
            "财富线平稳。做一次小复盘：订阅、外卖、冲动购。",
            "中平偏稳。把钱放在真正需要的地方，心就安。",
        ),
        "mild": (
            "可能有小额甜头。开心收下，落袋为安最稳当。",
            "财运轻喜。小省也是到的钱，温柔记账即可。",
        ),
        "plain": (
            "守成为上。今天不宜大额冲动决策，平常心最好。",
            "财运平常。先把必要开销安顿好，其他慢慢来。",
        ),
        "low": (
            "先稳住现金流：能推迟的消费就推迟，别跟自己较劲。",
            "今天宜省心花钱。照顾好吃饭与必要开支，运势会回头。",
        ),
    },
    "health": {
        "best": (
            "精力回升、身体偏轻盈。睡够、喝水、走动，心情也会亮。",
            "健康气场明亮。规律作息比补剂玄学更实在。",
        ),
        "good": (
            "调养得法。肩膀僵就伸展两分钟，眼睛酸就看远处。",
            "身体向好。规律吃饭、适度走动，比硬撑更划算。",
        ),
        "ok": (
            "健康平稳。久坐起身、窗边透气，都是小小的药。",
            "劳逸搭配即可。允许短暂休息，状态会更稳。",
        ),
        "mild": (
            "小憩有益。闭目一刻或散步十分钟，醒来世界轻三分。",
            "健康轻吉。给身体一点温柔，比硬刚更聪明。",
        ),
        "plain": (
            "听身体说话。不舒服就减强度，健康是长线副本。",
            "今天宜早睡一步。平常养护，少一分后悔。",
        ),
        "low": (
            "今天以养为主：少熬夜、少刺激，必要时好好休息。",
            "先安顿身心。休息也是前进，别拿硬撑当勇敢。",
        ),
    },
}

_THEME_DIM_BIAS: dict[str, dict[str, int]] = {
    "love_m": {"love": 1},
    "love_f": {"love": 1},
    "single": {"love": 1},
    "grad": {"career": 1},
    "exam": {"career": 1},
    "work": {"career": 1},
    "project": {"career": 1},
    "focus": {"career": 1},
    "money": {"wealth": 1},
    "health": {"health": 1},
    "family": {"love": 1, "health": 1},
    "helper": {"overall": 1},
    "travel": {"overall": 1, "health": 1},
    "luck": {"overall": 1},
}

_KEYWORD_DIM_HINTS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("缘", "爱", "情", "邂逅", "脱单", "心动"), "love"),
    (("考", "学", "业", "工", "项目", "签", "卷", "职"), "career"),
    (("财", "钱", "账", "到账", "红包", "花"), "wealth"),
    (("身", "眠", "睡", "养", "气", "健康", "息"), "health"),
)

@lru_cache(maxsize=1)
def load_fortune_pack() -> dict[str, Any]:
    raw = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    themes = []
    for row in raw.get("themes") or []:
        if not isinstance(row, dict) or not row.get("id"):
            continue
        icon = str(row.get("icon") or _ICON_FALLBACK)
        if icon.endswith("_fallback"):
            icon = str(row.get("icon_fallback") or _ICON_FALLBACK)
        themes.append(
            {
                "id": str(row["id"]),
                "label": str(row.get("label") or row["id"]),
                "icon": icon,
            }
        )
    levels = [
        {
            "id": str(row["id"]),
            "label": str(row.get("label") or row["id"]),
            "weight": max(1, int(row.get("weight") or 1)),
            "tone": str(row.get("tone") or "ok"),
        }
        for row in (raw.get("levels") or [])
        if isinstance(row, dict) and row.get("id")
    ]
    sticks = []
    for row in raw.get("sticks") or []:
        if not isinstance(row, dict):
            continue
        themes_list = row.get("themes") or ["*"]
        if not isinstance(themes_list, list):
            themes_list = ["*"]
        keywords = row.get("keywords") or []
        if not isinstance(keywords, list):
            keywords = []
        sticks.append(
            {
                "themes": [str(t) for t in themes_list],
                "level": str(row.get("level") or "ping"),
                "title": str(row.get("title") or "签"),
                "verse": str(row.get("verse") or ""),
                "counsel": str(row.get("counsel") or ""),
                "keywords": [str(k) for k in keywords if str(k).strip()],
                "soft_pause": str(row.get("soft_pause") or "").strip(),
            }
        )
    joys = [str(j) for j in (raw.get("daily_joys") or []) if str(j).strip()]
    return {
        "disclaimer": str(raw.get("disclaimer") or "开心最重要 · 仅供娱乐。"),
        "themes": themes,
        "levels": levels,
        "sticks": sticks,
        "daily_joys": joys or list(_DEFAULT_JOYS),
    }


def clear_fortune_cache() -> None:
    load_fortune_pack.cache_clear()


def fortune_bootstrap() -> dict[str, Any]:
    """Lightweight payload for first paint (no stick texts, no theme list)."""
    pack = load_fortune_pack()
    return {
        "disclaimer": pack["disclaimer"],
        "levels": pack["levels"],
    }


def _shichen_label(now: datetime | None = None) -> str:
    hour = (now or datetime.now()).hour
    if hour < 1 or hour >= 23:
        return "子时"
    if hour < 3:
        return "丑时"
    if hour < 5:
        return "寅时"
    if hour < 7:
        return "卯时"
    if hour < 9:
        return "辰时"
    if hour < 11:
        return "巳时"
    if hour < 13:
        return "午时"
    if hour < 15:
        return "未时"
    if hour < 17:
        return "申时"
    if hour < 19:
        return "酉时"
    if hour < 21:
        return "戌时"
    return "亥时"


def _seed_line(now: datetime | None = None) -> str:
    dt = now or datetime.now()
    return f"求签时辰 · {dt.month}月{dt.day}日 {_shichen_label(dt)}"


def _pick_daily_joy(joys: list[str], now: datetime | None = None) -> str:
    dt = now or datetime.now()
    key = f"{dt.year}-{dt.month}-{dt.day}"
    h = 0
    for ch in key:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    pool = joys or _DEFAULT_JOYS
    return pool[h % len(pool)]


def _keywords_for(stick: dict[str, Any], theme_map: dict[str, str], level_label: str) -> list[str]:
    if stick.get("keywords"):
        return list(stick["keywords"])[:5]
    keys: list[str] = []
    title = stick.get("title") or ""
    if title:
        keys.append(title[:6])
    verse = stick.get("verse") or ""
    parts = re.split(r"[，。、；！？,\s]+", verse)
    for part in parts:
        part = part.strip()
        if 2 <= len(part) <= 8 and part not in keys:
            keys.append(part)
        if len(keys) >= 3:
            break
    for tid in stick.get("themes") or []:
        if tid == "*":
            continue
        label = theme_map.get(tid)
        if label and label not in keys:
            keys.append(label)
        if len(keys) >= 4:
            break
    if level_label and level_label not in keys:
        keys.append(level_label)
    return keys[:5]


def _stable_salt(*parts: str) -> int:
    h = 2166136261
    for part in parts:
        for ch in part:
            h ^= ord(ch)
            h = (h * 16777619) & 0xFFFFFFFF
    return h


def _clamp_score(n: int) -> int:
    return max(1, min(5, n))


def _tone_from_score(score: int) -> str:
    if score >= 5:
        return "best"
    if score >= 4:
        return "good"
    if score == 3:
        return "mild"
    if score == 2:
        return "plain"
    return "low"


def _dim_bias_for_stick(stick: dict[str, Any], keywords: list[str]) -> dict[str, int]:
    bias: dict[str, int] = {}
    for tid in stick.get("themes") or []:
        for dim_id, delta in (_THEME_DIM_BIAS.get(str(tid)) or {}).items():
            bias[dim_id] = bias.get(dim_id, 0) + delta
    blob = " ".join(
        [
            str(stick.get("title") or ""),
            str(stick.get("verse") or ""),
            str(stick.get("counsel") or ""),
            *keywords,
        ]
    )
    for needles, dim_id in _KEYWORD_DIM_HINTS:
        if any(n in blob for n in needles):
            bias[dim_id] = bias.get(dim_id, 0) + 1
    return bias


def _pick_dim_prose(dim_id: str, tone: str, salt: int) -> str:
    pool = (_DIM_PROSE.get(dim_id) or {}).get(tone) or (_DIM_PROSE["overall"].get(tone) or ())
    if not pool:
        pool = _DIM_PROSE["overall"]["ok"]
    return pool[salt % len(pool)]


def _build_dimensions(
    stick: dict[str, Any],
    tone: str,
    keywords: list[str],
) -> list[dict[str, Any]]:
    base = _TONE_SCORE.get(tone, 3)
    bias = _dim_bias_for_stick(stick, keywords)
    title = str(stick.get("title") or "")
    dims: list[dict[str, Any]] = []
    for meta in _DIM_META:
        dim_id = meta["id"]
        salt = _stable_salt(title, dim_id, tone, *keywords[:3])
        wobble = (salt % 3) - 1  # -1, 0, +1
        score = _clamp_score(base + bias.get(dim_id, 0) + wobble)
        # Soft ceiling: never paint every dimension as peak from one lucky stick
        if dim_id != "overall" and score >= 5 and base < 5:
            score = 4
        dim_tone = _tone_from_score(score)
        # Keep overall aligned with stick tone label feel
        if dim_id == "overall":
            dim_tone = tone if tone in _TONE_TAG else dim_tone
            score = _clamp_score(_TONE_SCORE.get(dim_tone, score))
        dims.append(
            {
                "id": dim_id,
                "label": meta["label"],
                "hue": meta["hue"],
                "glyph": meta["glyph"],
                "score": score,
                "max_score": 5,
                "tag": _TONE_TAG.get(dim_tone, _TONE_TAG["ok"]),
                "tone": dim_tone,
                "text": _pick_dim_prose(dim_id, dim_tone, salt),
            }
        )
    return dims


def _enrich_draw(
    stick: dict[str, Any],
    level: dict[str, Any],
    pack: dict[str, Any],
) -> dict[str, Any]:
    tone = level.get("tone") or "ok"
    theme_map = {t["id"]: t["label"] for t in pack["themes"]}
    joy_path = stick.get("counsel") or "去做让自己安心的一小步。"
    soft = stick.get("soft_pause") or _SOFT_PAUSE.get(tone) or _SOFT_PAUSE["ok"]
    keywords = _keywords_for(stick, theme_map, level["label"])
    dimensions = _build_dimensions(stick, tone, keywords)
    return {
        "level": {
            "id": level["id"],
            "label": level["label"],
            "tone": tone,
            "blurb": _LEVEL_BLURB.get(tone, _LEVEL_BLURB["ok"]),
        },
        "stick": {
            "title": stick["title"],
            "verse": stick["verse"],
            "counsel": stick["counsel"],
        },
        "keywords": keywords,
        "dimensions": dimensions,
        "joy_path": joy_path,
        "soft_pause": soft,
        "daily_joy": _pick_daily_joy(pack["daily_joys"]),
        "seed": _seed_line(),
    }


def _weighted_draw(pool: list[dict[str, Any]], pack: dict[str, Any]) -> dict[str, Any] | None:
    levels = pack["levels"]
    if not pool:
        return None
    level_map = {lv["id"]: lv for lv in levels}
    by_level: dict[str, list[dict[str, Any]]] = {}
    for stick in pool:
        lid = stick.get("level") or "ping"
        by_level.setdefault(lid, []).append(stick)
    available = [lv for lv in levels if by_level.get(lv["id"])]
    if not available:
        available = levels
    if not available:
        stick = random.choice(pool)
        level = {
            "id": stick.get("level") or "ping",
            "label": stick.get("level") or "签",
            "tone": "ok",
        }
        return _enrich_draw(stick, level, pack)
    total = sum(max(1, lv["weight"]) for lv in available)
    r = random.random() * total
    chosen_level = available[-1]
    for lv in available:
        r -= max(1, lv["weight"])
        if r <= 0:
            chosen_level = lv
            break
    candidates = by_level.get(chosen_level["id"]) or pool
    stick = random.choice(candidates)
    level = level_map.get(stick["level"], chosen_level)
    return _enrich_draw(stick, level, pack)


def draw_any() -> dict[str, Any] | None:
    """Server-side weighted draw from the full stick pool (no wish filter)."""
    pack = load_fortune_pack()
    return _weighted_draw(pack["sticks"], pack)


def sticks_for_theme(theme_id: str) -> list[dict[str, Any]]:
    pack = load_fortune_pack()
    tid = (theme_id or "").strip()
    if not tid:
        return []
    known = {t["id"] for t in pack["themes"]}
    if tid not in known:
        return []
    themed = [s for s in pack["sticks"] if tid in (s.get("themes") or [])]
    shared = [s for s in pack["sticks"] if "*" in (s.get("themes") or [])]
    return themed + shared if themed else shared


def draw_for_theme(theme_id: str) -> dict[str, Any] | None:
    """Legacy themed draw; kept for compatibility."""
    pack = load_fortune_pack()
    tid = (theme_id or "").strip()
    theme = next((t for t in pack["themes"] if t["id"] == tid), None)
    if not theme:
        return None
    payload = _weighted_draw(sticks_for_theme(tid), pack)
    if not payload:
        return None
    return {
        "theme": {"id": theme["id"], "label": theme["label"]},
        **payload,
    }
