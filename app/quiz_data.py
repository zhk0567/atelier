"""Questionnaire content, scoring, and result copy for the self-check."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

QUIZ_TITLE = "当代人精神状态深度自测"
QUIZ_PATH = "/quiz/neurosis"
QUIZ_MAX_SCORE = 87
QUIZ_VERSION = "v3-bank120-2026-10-19"
PRIVACY_VERSION = "2026-10-19-v4"
PRIVACY_DOC = "docs/NEUROSIS_PRIVACY.md"

QUIZ_INTRO = (
    "有些累，不是睡一觉就能解决的。",
    "你可以在人群里正常说笑，也可以在深夜突然怀疑一切。",
    "这份测试不负责给你下诊断，只负责把你最近的状态摊开看看。",
    "每次会从 120 道情境中随机抽取 30 道，含 1 道注意力检测。",
    "凭第一直觉作答；没有完全符合的选项时，选相对最接近的那个。",
    "提交后可用昵称 + 学号/查询码找回答题记录。",
)

QUIZ_NOTE = (
    "本测试仅供娱乐与自我觉察，不构成医学诊断。"
    "提交后会保存昵称、学号/查询码、答案、结果、用时和同意版本；"
    "答题前需勾选同意《数据收集与隐私保护协议》。"
)

GROUP_ORDER = ("social", "rumination", "existential", "action", "attachment", "core")

GROUPS: dict[str, dict[str, Any]] = {
    "social": {
        "name": "社交敏感",
        "short": "人群中的耗能",
        "high": (
            "你对他人的反馈非常敏感。群里冷场、消息不回、语气变化，都可能被你放大成"
            "“是不是我做错了”。你共情力强，但社交像持续耗电。"
        ),
        "low": "你对外界评价比较钝感，轻松自在，但有时也会错过别人递来的真实信号。",
    },
    "rumination": {
        "name": "深夜反刍",
        "short": "脑内回放机",
        "high": (
            "你的大脑像一台夜间自动播放器，反复回放白天的小事。你洞察力强，"
            "但很容易把思考变成自我惩罚。"
        ),
        "low": "你不太回头咀嚼过去，能放下就放下，但偶尔也会忽略情绪留下的余震。",
    },
    "existential": {
        "name": "存在虚无",
        "short": "意义与价值感",
        "high": (
            "你渴望意义，也常问“这一切到底为了什么”。你能看见结构，"
            "但容易滑向虚无，或者用忙碌遮住真正的困惑。"
        ),
        "low": "你更关注眼前的生活，不太追问宏大意义，但有时也可能用“别想太多”回避问题。",
    },
    "action": {
        "name": "行动与代偿",
        "short": "拖延与身体信号",
        "high": (
            "压力上来时，你容易僵住：知道该做，却迟迟动不了；越拖越焦虑，"
            "再用刷手机、熬夜或情绪化进食来代偿。你的要求很高，只是行动被卡住了。"
        ),
        "low": "你的执行和生活秩序相对稳定，但也要留意身体是否在用疲惫替你喊停。",
    },
    "attachment": {
        "name": "关系依恋",
        "short": "靠近与失去",
        "high": (
            "你在关系中高度警觉：渴望被爱，又害怕被看穿；别人靠近时想确认，"
            "别人冷淡时又先推开。你重视连接，但常把安全感交给对方的反应。"
        ),
        "low": "你在关系中边界感较强，能保护自己，但有时也会把真实需求藏得太深。",
    },
    "core": {
        "name": "精神底牌",
        "short": "自我评价与懂事",
        "high": (
            "你对自己的状态有很强的觉知，也可能对自己非常苛刻。你擅长分析自己，"
            "但“清醒”有时会变成另一种压力：看见了，却还没允许自己改变。"
        ),
        "low": "你的自我评价相对稳定，不容易被标签带走，但也要留意是否把真实疲惫合理化了。",
    },
}

DIMENSION_GUIDES: dict[str, dict[str, Any]] = {
    "social": {
        "scene": "消息发出去后的两小时，是你最漫长的时区。",
        "trigger": "已读不回、群里突然安静、对方语气变短。",
        "recovery": "先把“对方在忙”当成默认解释，再去做一件十分钟内能完成的小事。",
        "mantra": "别人的沉默，不是我的判决书。",
        "keywords": ("读空气", "关系雷达", "社交后遗症"),
        "weather": "人际场局部有雾",
    },
    "rumination": {
        "scene": "白天负责生活，夜里负责审判白天。",
        "trigger": "躺下之后突然想起的一句尴尬发言。",
        "recovery": "给复盘设一个十分钟的闹钟，铃响后只写“明天再做的一步”。",
        "mantra": "想明白，不等于要想到天亮。",
        "keywords": ("夜间回放", "脑内剪辑", "复盘成瘾"),
        "weather": "夜间有持续性脑内降雨",
    },
    "existential": {
        "scene": "别人在过日子，你在追问日子为什么值得过。",
        "trigger": "看到别人的进展，或者某一个突然安静下来的夜晚。",
        "recovery": "把“人生有没有意义”缩小成“今天这件事对我有没有一点意义”。",
        "mantra": "先活在一个具体的今天里。",
        "keywords": ("意义侦探", "虚无感", "价值校准"),
        "weather": "局部能见度低，容易迷失方向",
    },
    "action": {
        "scene": "你知道该做什么，也知道自己为什么还没开始。",
        "trigger": "任务太多、标准太高、身体状态又不在线。",
        "recovery": "把任务拆到五分钟，只要求启动，不要求今天完成。",
        "mantra": "先动一下，动力可以晚点到。",
        "keywords": ("启动困难", "死线冲刺", "代偿性熬夜"),
        "weather": "行动区有逆风，起步需要额外能量",
    },
    "attachment": {
        "scene": "越在意的人，越容易被你拿来测试安全感。",
        "trigger": "回复变慢、语气变淡、关系里出现一点不确定。",
        "recovery": "把“他是不是不爱我了”改写成“我现在需要什么”，然后直接说出来。",
        "mantra": "我值得被爱，不需要先通过一场考试。",
        "keywords": ("靠近型刺猬", "安全感确认", "关系预警"),
        "weather": "关系区有短时强对流",
    },
    "core": {
        "scene": "你既是当事人，也是法官，还是全程录像的人。",
        "trigger": "犯错、被夸、被比较，或者发现自己又没做到。",
        "recovery": "把一句“我怎么这么差”换成“我这次哪里可以调整”。",
        "mantra": "觉察不是用来惩罚自己的。",
        "keywords": ("自我审计", "高要求", "清醒着内耗"),
        "weather": "自我评价区持续低压",
    },
}

PERSONAS: dict[str, tuple[str, str, str, str]] = {
    "social": ("人形读空气机", "关系雷达", "社交续航告急", "人群过载警报"),
    "rumination": ("夜间剪辑师", "脑内回放员", "反刍永动机", "凌晨三点导演"),
    "existential": ("意义观察员", "价值追问者", "虚无游客", "宇宙级空心人"),
    "action": ("行动派候补", "启动困难户", "死线驯兽师", "瘫痪型选手"),
    "attachment": ("关系安全员", "靠近型刺猬", "失联预警器", "亲密关系雷达"),
    "core": ("清醒观察员", "自我审计师", "高要求本我", "自我PUA研究员"),
}

SEVERITY_WEATHER = (
    ("轻盈", "晴，偶有微风"),
    ("波动", "多云，局部有阵雨"),
    ("高压", "阴，夜间有持续性降雨"),
    ("警报", "雷暴预警，请优先照顾自己"),
)

SEVERITY_REFRAIMES = (
    "状态稳定不代表没有感受。你也会累，只是恢复得更快。",
    "偶尔的情绪波动不是性格缺陷，它更像身体发来的待办提醒。",
    "你不是想太多，你只是长期把雷达开得太亮，忘了给自己留一块安静的地方。",
    "现在需要的不是再努力一点，而是先减少负荷，让自己重新有被接住的空间。",
)

SUPPORT_NEEDS = {
    "social": "需要的不是“别想太多”，而是一个明确、稳定的回应。",
    "rumination": "需要的不是立刻振作，而是有人陪你把这页翻过去。",
    "existential": "需要的不是大道理，而是一件今天就能感到真实的小事。",
    "action": "需要的不是更多催促，而是把第一步缩小到真的做得动。",
    "attachment": "需要的不是反复试探，而是一次直接、具体的确认。",
    "core": "需要的不是继续分析自己，而是允许自己暂时不及格。",
}

COMBINATION_NOTES = {
    ("social", "rumination"): "一边读空气，一边把空气录下来反复播放。",
    ("social", "existential"): "在人群里寻找意义，又在散场后怀疑自己是否存在。",
    ("social", "action"): "怕被看见做得不够好，于是干脆迟迟不开始。",
    ("social", "attachment"): "最怕关系出错，所以把对方的每个表情都当成信号。",
    ("social", "core"): "对外高度雷达，对内高度审判。",
    ("rumination", "existential"): "夜里把人生从头复盘，得出的结论通常是“我不行”。",
    ("rumination", "action"): "想得越久，动得越少；动得越少，想得越多。",
    ("rumination", "attachment"): "白天忍住不说，晚上把聊天记录逐字重读。",
    ("rumination", "core"): "你既是被告，也是法官，还是全程录像的人。",
    ("existential", "action"): "一边觉得一切没意义，一边为没完成的事焦虑。",
    ("existential", "attachment"): "想被坚定选择，又怀疑自己凭什么被选择。",
    ("existential", "core"): "你对自己的理解很深，对自己的耐心很少。",
    ("action", "attachment"): "关系一有波动就停摆，计划也跟着一起塌。",
    ("action", "core"): "知道该怎么做，却总觉得现在的自己还不配开始。",
    ("attachment", "core"): "把“被爱”当成考试，把每次冷淡当成扣分。",
}

MICRO_PLAN = (
    ("01", "抓到一个耗电瞬间", "记下今天最触发你的一幕，不解释，只记录。"),
    ("02", "只做五分钟", "把最想逃开的事拆到五分钟，做完就停。"),
    ("03", "给情绪一个名字", "不是“我不行”，而是“我现在很焦虑/很委屈”。"),
    ("04", "无手机散步", "走十五分钟，不听歌不刷屏，让大脑降噪。"),
    ("05", "说一句真实需求", "“我现在需要安静/陪伴/一个拥抱。”"),
    ("06", "不审判地回看", "写下一件这周做成的小事，不许加“但是”。"),
    ("07", "再测一次", "回来看哪一维变了，不追求变好，只观察变化。"),
)


def _q(
    number: int,
    group: str,
    title: str,
    prompt: str,
    options: tuple[str, str, str, str],
    *,
    weight: int = 1,
) -> dict[str, Any]:
    return {
        "number": number,
        "key": f"q{number:02d}",
        "group": group,
        "group_name": "注意力检测" if group == "attention" else GROUPS[group]["name"],
        "weight": weight,
        "title": title,
        "prompt": prompt,
        "options": [
            {"letter": letter, "text": text}
            for letter, text in zip("ABCD", options)
        ],
    }


_QUESTIONS_PATH = Path(__file__).with_name("quiz_bank.json")
_BANK_ROWS = json.loads(_QUESTIONS_PATH.read_text(encoding="utf-8"))

QUESTIONS: tuple[dict[str, Any], ...] = tuple(
    _q(
        int(row["number"]),
        str(row["group"]),
        str(row["title"]),
        str(row["prompt"]),
        tuple(str(option) for option in row["options"]),
    )
    for row in _BANK_ROWS
)

if len(QUESTIONS) != 120:
    raise RuntimeError("quiz_bank.json must contain exactly 120 questions")

for _group in GROUP_ORDER:
    if sum(question["group"] == _group for question in QUESTIONS) != 20:
        raise RuntimeError(f"quiz_bank.json group {_group} must contain 20 questions")


ATTENTION_QUESTIONS: tuple[dict[str, Any], ...] = (
    {
        "number": 121,
        "key": "a1",
        "group": "attention",
        "group_name": "注意力检测",
        "weight": 0,
        "title": "注意力检测",
        "prompt": "为了确认你在认真看题，请直接选 C：",
        "options": [
            {"letter": "A", "text": "我偏不选C"},
            {"letter": "B", "text": "选B显正常"},
            {"letter": "C", "text": "我选C"},
            {"letter": "D", "text": "偏要选D"},
        ],
        "correct": "C",
    },
    {
        "number": 122,
        "key": "a2",
        "group": "attention",
        "group_name": "注意力检测",
        "weight": 0,
        "title": "注意力检测",
        "prompt": "这道题请选择 B，不要选择其他选项：",
        "options": [
            {"letter": "A", "text": "我还是要选A"},
            {"letter": "B", "text": "我选B"},
            {"letter": "C", "text": "我偏要选C"},
            {"letter": "D", "text": "我偏要选D"},
        ],
        "correct": "B",
    },
    {
        "number": 123,
        "key": "a3",
        "group": "attention",
        "group_name": "注意力检测",
        "weight": 0,
        "title": "注意力检测",
        "prompt": "请忽略其他选项，直接选 A：",
        "options": [
            {"letter": "A", "text": "我选A"},
            {"letter": "B", "text": "选B更安全"},
            {"letter": "C", "text": "我想选C"},
            {"letter": "D", "text": "我偏要选D"},
        ],
        "correct": "A",
    },
    {
        "number": 124,
        "key": "a4",
        "group": "attention",
        "group_name": "注意力检测",
        "weight": 0,
        "title": "注意力检测",
        "prompt": "请直接选择 D：",
        "options": [
            {"letter": "A", "text": "我偏不选D"},
            {"letter": "B", "text": "我想选B"},
            {"letter": "C", "text": "选C显得正常"},
            {"letter": "D", "text": "我选D"},
        ],
        "correct": "D",
    },
    {
        "number": 125,
        "key": "a5",
        "group": "attention",
        "group_name": "注意力检测",
        "weight": 0,
        "title": "注意力检测",
        "prompt": "请选择 C，证明你没有在盲选：",
        "options": [
            {"letter": "A", "text": "我闭眼选A"},
            {"letter": "B", "text": "我随手选B"},
            {"letter": "C", "text": "我认真选C"},
            {"letter": "D", "text": "我叛逆选D"},
        ],
        "correct": "C",
    },
    {
        "number": 126,
        "key": "a6",
        "group": "attention",
        "group_name": "注意力检测",
        "weight": 0,
        "title": "注意力检测",
        "prompt": "这道题请直接选 B：",
        "options": [
            {"letter": "A", "text": "我偏不选B"},
            {"letter": "B", "text": "我选B"},
            {"letter": "C", "text": "我选C"},
            {"letter": "D", "text": "我选D"},
        ],
        "correct": "B",
    },
)

QUESTION_BY_KEY = {question["key"]: question for question in QUESTIONS}
ATTENTION_BY_KEY = {question["key"]: question for question in ATTENTION_QUESTIONS}
QUESTION_LOOKUP = {**QUESTION_BY_KEY, **ATTENTION_BY_KEY}

CORE_QUESTIONS_PER_ATTEMPT = 29
ATTEMPT_QUESTION_COUNT = 30


def build_attempt_questions() -> list[dict[str, Any]]:
    rng = random.SystemRandom()
    short_group = rng.choice(GROUP_ORDER)
    selected: list[dict[str, Any]] = []
    for group in GROUP_ORDER:
        pool = [question for question in QUESTIONS if question["group"] == group]
        quota = 4 if group == short_group else 5
        selected.extend(rng.sample(pool, quota))
    selected.append(rng.choice(ATTENTION_QUESTIONS))
    rng.shuffle(selected)
    return selected


def selection_from_order(order_raw: str) -> list[dict[str, Any]] | None:
    keys = [key.strip() for key in order_raw.split(",") if key.strip()]
    if len(keys) != ATTEMPT_QUESTION_COUNT or len(set(keys)) != ATTEMPT_QUESTION_COUNT:
        return None
    if any(key not in QUESTION_LOOKUP for key in keys):
        return None
    selected = [QUESTION_LOOKUP[key] for key in keys]
    attention = [question for question in selected if question["group"] == "attention"]
    core = [question for question in selected if question["group"] != "attention"]
    if len(attention) != 1 or len(core) != CORE_QUESTIONS_PER_ATTEMPT:
        return None
    counts = {
        group: sum(question["group"] == group for question in core)
        for group in GROUP_ORDER
    }
    if sorted(counts.values()) != [4, 5, 5, 5, 5, 5]:
        return None
    return selected


BANDS: tuple[dict[str, Any], ...] = (
    {
        "min": 0,
        "max": 10,
        "emoji": "🟢",
        "title": "情绪绝缘体",
        "tagline": "别人发疯，你睡觉。",
        "profile": "你的钝感力很强，极少被情绪拖着走。事情过了就过了，很少在脑内重播。",
        "symptoms": ("对负面反馈反应慢", "不常反刍", "情绪来得快去得也快"),
        "inner_os": "“这有什么好想的？”",
        "strength": "稳定、抗压，不容易被别人的情绪带着跑。",
        "watchout": "可能忽略身体和关系里的细微信号，也容易把别人的痛苦当成“想太多”。",
        "prescription": ("保持规律作息", "偶尔主动问问身边人的状态", "别把“没事”当成唯一答案"),
        "challenge": "今天认真问一个朋友：你最近真的还好吗？",
        "share": "我是【情绪绝缘体】，精神状态遥遥领先。",
    },
    {
        "min": 11,
        "max": 19,
        "emoji": "🟢",
        "title": "没心没肺快乐小狗",
        "tagline": "一顿好吃的就能续命。",
        "profile": "情绪来得快，去得也快。你不爱记仇，也不太反刍，生活里的小确幸就足够把你捞回来。",
        "symptoms": ("不太记仇", "难过一阵就能恢复", "容易因为小事重新开心"),
        "inner_os": "“算了，先吃饭。”",
        "strength": "恢复力强，能把生活过得很具体。",
        "watchout": "有时会用“我没事”略过真正的问题。",
        "prescription": ("保留你的快乐来源", "难过时多停一分钟", "把身体状态也当成情绪的一部分"),
        "challenge": "今天写下三件让你觉得“还不错”的小事。",
        "share": "我是【没心没肺快乐小狗】，胃比心更需要保护。",
    },
    {
        "min": 20,
        "max": 29,
        "emoji": "🟢",
        "title": "正常波动现代人",
        "tagline": "偶尔焦虑，但日子还在轨道上。",
        "profile": "你有正常范围的焦虑和疲惫，也会被没钱、没对象、工作和比较影响，但整体仍能维持生活秩序。",
        "symptoms": ("偶尔失眠", "偶尔怀疑自己", "大多数时候还能继续做事"),
        "inner_os": "“今天有点烦，但明天应该会好。”",
        "strength": "现实感强，能在压力和日常之间保持平衡。",
        "watchout": "忙起来容易把疲惫常态化。",
        "prescription": ("减少无意义的信息摄入", "给焦虑留一个固定的处理时间", "保持运动或散步"),
        "challenge": "卸载一个让你反复比较的 App，试一天。",
        "share": "我是【正常波动现代人】，偶尔破防，整体还在线。",
    },
    {
        "min": 30,
        "max": 37,
        "emoji": "🟡",
        "title": "轻度内耗·偶尔emo",
        "tagline": "白天哈哈，半夜唉。",
        "profile": "你大部分时候正常运转，但某些时刻会突然掉进情绪里。一条没回的消息，足够你在脑内演完一部长剧。",
        "symptoms": ("偶尔过度解读", "夜里容易想多", "第二天又能装作没事"),
        "inner_os": "“我是不是想多了？应该是吧。”",
        "strength": "感受力细腻，能捕捉到别人忽略的情绪。",
        "watchout": "容易把小信号放大成对自己的否定。",
        "prescription": ("消息没回先默认对方在忙", "睡前做一件不刷屏的事", "把脑内剧情写下来再判断"),
        "challenge": "今天有一条消息，故意等三十分钟再回复。",
        "share": "我是【轻度内耗·偶尔emo】，白天正常，半夜开会。",
    },
    {
        "min": 38,
        "max": 44,
        "emoji": "🟡",
        "title": "间歇性自我怀疑",
        "tagline": "被夸也怀疑，被冷落更怀疑。",
        "profile": "别人夸你，你会想是不是客套；别人没理你，你立刻反思自己做错了什么。你的自我评价很容易被外界反馈牵动。",
        "symptoms": ("需要反复确认", "被夸会心虚", "容易把沉默理解为否定"),
        "inner_os": "“他们是不是只是客气？”",
        "strength": "你很敏锐，也很愿意调整自己。",
        "watchout": "把别人的反应当成自我价值的评分器。",
        "prescription": ("每天客观记录一件做成的事", "区分事实和猜测", "减少反复求证"),
        "challenge": "收到夸奖时只回“谢谢”，不解释、不否认。",
        "share": "我是【间歇性自我怀疑】，正在练习相信自己一次。",
    },
    {
        "min": 45,
        "max": 52,
        "emoji": "🟡",
        "title": "薛定谔的正常人",
        "tagline": "表面稳定，回家卸妆。",
        "profile": "你在外面靠谱、稳定，常常是朋友倾诉的对象。但一回到家躺下，真正的疲惫才开始浮上来。",
        "symptoms": ("人前稳定", "人后叹气", "习惯先照顾别人"),
        "inner_os": "“我没事，我只是有点累。”",
        "strength": "可靠、体贴，能给别人安全感。",
        "watchout": "长期把自己的需求排在最后。",
        "prescription": ("允许自己表达负能量", "不要每次都当倾听者", "给自己安排无目的休息"),
        "challenge": "今天对一个人说一句真实的“我有点累”。",
        "share": "我是【薛定谔的正常人】，看起来没事，其实需要休息。",
    },
    {
        "min": 53,
        "max": 58,
        "emoji": "🟠",
        "title": "深夜反刍机器",
        "tagline": "一到夜里，大脑自动开机。",
        "profile": "夜晚会把白天的小事放大。你想复盘，却常常复盘成自我审判；越想找到最优解，越睡不着。",
        "symptoms": ("睡前回放细节", "反复寻找正确答案", "越想越清醒"),
        "inner_os": "“如果当时那样说就好了。”",
        "strength": "反思能力强，愿意对自己负责。",
        "watchout": "把反刍误当成解决问题。",
        "prescription": ("睡前一小时远离手机", "给复盘设置十分钟上限", "写下明天能做的一步"),
        "challenge": "今晚睡前只写一句“明天再说”，然后停笔。",
        "share": "我是【深夜反刍机器】，今晚准备早点关机。",
    },
    {
        "min": 59,
        "max": 64,
        "emoji": "🟠",
        "title": "社交敏感与重度伪装",
        "tagline": "最怕冷场，也最怕被看穿。",
        "profile": "你非常在意氛围，聊天时总想接住每个人。对方回复慢一点，你已经开始撤回、补救、重新组织语言。",
        "symptoms": ("害怕冷场", "反复检查措辞", "社交后需要长时间恢复"),
        "inner_os": "“是不是我说错话了？”",
        "strength": "共情力强，能让别人感到被照顾。",
        "watchout": "把维持气氛当成自己的责任。",
        "prescription": ("允许沉默存在", "少做一次气氛救火员", "把注意力放回自己的感受"),
        "challenge": "今天在一次聊天里，不主动找新话题。",
        "share": "我是【社交敏感与重度伪装】，正在练习不救场。",
    },
    {
        "min": 65,
        "max": 70,
        "emoji": "🟠",
        "title": "半永久内耗患者",
        "tagline": "精神电量常年偏低。",
        "profile": "你每天都在硬撑，觉得周围人不太理解自己。想摆烂又不敢，想休息又愧疚，电量一直在低处徘徊。",
        "symptoms": ("长期疲惫", "做什么都提不起劲", "休息时也在担心没做的事"),
        "inner_os": "“我只是需要停一下，但我不敢。”",
        "strength": "责任感很强，撑着也把很多事完成了。",
        "watchout": "把“还能撑”当成不需要帮助。",
        "prescription": ("安排一天彻底的无目的休息", "减少同时进行的任务", "把求助说出口"),
        "challenge": "今天删掉待办清单里一件并不重要的事。",
        "share": "我是【半永久内耗患者】，今天开始给自己省一点电。",
    },
    {
        "min": 71,
        "max": 74,
        "emoji": "🟠",
        "title": "情绪寄生体",
        "tagline": "别人的一点温度，能决定你一天。",
        "profile": "你极度缺乏安全感。别人对你好一点，你容易过度依赖；别人冷淡一点，你会觉得世界塌了。你的情绪重心很容易落在别人身上。",
        "symptoms": ("高度关注对方反应", "害怕被丢下", "情绪随关系波动"),
        "inner_os": "“他是不是不要我了？”",
        "strength": "你投入、真诚，重视每一段关系。",
        "watchout": "把自我稳定交给别人的即时反馈。",
        "prescription": ("把情绪重心收回自己", "建立不依赖某一个人的支持网络", "在关系外保留自己的生活"),
        "challenge": "今天做一件只为自己开心、不需要发朋友圈的事。",
        "share": "我是【情绪寄生体】，正在把重心收回自己身上。",
    },
    {
        "min": 75,
        "max": 78,
        "emoji": "🔴",
        "title": "精神电量仅剩1%",
        "tagline": "一件小事就可能让你掉眼泪。",
        "profile": "你的承受阈值已经很低。打不开瓶盖、被打断说话，都可能成为压垮情绪的最后一根稻草。",
        "symptoms": ("容易突然崩溃", "对小事过度反应", "恢复时间变长"),
        "inner_os": "“我真的撑不住了。”",
        "strength": "你还在坚持，说明你比想象中更有韧性。",
        "watchout": "独自硬扛会让电量继续下降。",
        "prescription": ("先去人多、安全的地方走走", "联系一个可信任的人", "必要时寻求专业帮助"),
        "challenge": "今天给一个信任的人发一句：“我最近有点撑不住。”",
        "share": "我是【精神电量仅剩1%】，今天先给自己充电。",
    },
    {
        "min": 79,
        "max": 81,
        "emoji": "🔴",
        "title": "备忘录连环杀手",
        "tagline": "把每次失败都记录在案。",
        "profile": "你的备忘录里有大量自我剖析。你把尴尬、失败和后悔逐条存档，再反复拿出来审判自己。",
        "symptoms": ("反复记录负面事件", "习惯性自我批判", "很难允许事情过去"),
        "inner_os": "“我要把这件事想明白。”",
        "strength": "自我觉察深，表达和复盘能力强。",
        "watchout": "把自我惩罚包装成“成长”。",
        "prescription": ("清空一条最旧的自我批评", "给反思加一个行动出口", "写下今天做得不错的一件事"),
        "challenge": "打开备忘录，删掉一条已经过期的自责。",
        "share": "我是【备忘录连环杀手】，正在停止反复审判自己。",
    },
    {
        "min": 82,
        "max": 83,
        "emoji": "🔴",
        "title": "自我PUA大师",
        "tagline": "成绩是运气，问题全是自己。",
        "profile": "取得成绩时，你觉得是运气；出了问题，你立刻认定是自己不够努力。你甚至开始习惯“痛苦的清醒感”。",
        "symptoms": ("难以认可自己", "把成功归因于外部", "对失败过度负责"),
        "inner_os": "“我只是这次运气好。”",
        "strength": "要求高、反省深，愿意变得更好。",
        "watchout": "用高标准持续惩罚自己。",
        "prescription": ("记录一次真实的努力", "把“应该”换成“可以”", "接受自己的平庸和伟大"),
        "challenge": "今天把一句“我怎么这么差”改成“我这次哪里可以调整”。",
        "share": "我是【自我PUA大师】，正在练习对自己公平一点。",
    },
    {
        "min": 84,
        "max": 86,
        "emoji": "🔴",
        "title": "濒临宕机",
        "tagline": "表面风平浪静，内心千疮百孔。",
        "profile": "你不太愿意找人倾诉，觉得没人真正懂。你可能认真推演过“消失”的场景，也在用最后的力气维持日常。",
        "symptoms": ("强烈的孤独感", "觉得无人理解", "出现消失或逃离的念头"),
        "inner_os": "“如果我不在了，会有人发现吗？”",
        "strength": "你仍然在寻找出口，这说明你还没有放弃自己。",
        "watchout": "把危险信号当成普通的“想太多”。",
        "prescription": ("立刻联系一个信任的人", "不要独处太久", "必要时联系专业心理援助或紧急服务"),
        "challenge": "今天把一个真实感受告诉一个真人，不用组织语言。",
        "share": "我是【濒临宕机】，今天决定先找个人说说话。",
    },
    {
        "min": 87,
        "max": 87,
        "emoji": "⚫",
        "title": "不可名状的精神黑洞",
        "tagline": "你看透了很多，却还没能接住自己。",
        "profile": "你几乎把每一道题都答到了最重的一端。你对自己的状态非常清醒，甚至已经为内耗建了一套完整的台账。",
        "symptoms": ("长期高压", "强烈的自我审视", "对意义和关系都感到疲惫"),
        "inner_os": "“我知道，但我停不下来。”",
        "strength": "你的觉察力很强，能看见别人看不见的层次。",
        "watchout": "把“看得透”当成不去行动的借口。",
        "prescription": ("关掉手机，去晒太阳", "和真实的活人说话", "考虑寻求专业心理支持"),
        "challenge": "现在给一个真人发三个字：“在干嘛。”",
        "share": "我是【不可名状的精神黑洞】，今天先去找个活人说话。",
    },
)

HIDDEN_RESULTS: tuple[dict[str, str], ...] = (
    {
        "id": "rebel",
        "emoji": "🎲",
        "title": "赛博反骨型患者",
        "body": "你不仅内耗，你还戏多。明知道怎么做能让自己舒服，偏要走最难的路。在关系里，你喜欢用推开对方来测试对方。",
    },
    {
        "id": "pure-love",
        "emoji": "💘",
        "title": "纯爱战神应声倒地",
        "body": "关系是你痛苦的最大来源。你极度渴求被爱，容易在关系中失去自我，也容易把对方的每个反应都当成爱的证据。",
    },
    {
        "id": "avoidant",
        "emoji": "🪞",
        "title": "回避型依恋晚期",
        "body": "只要有人靠近，你就会亮出刺。你害怕被抛弃，所以先抛弃别人；你害怕被看穿，所以一直戴着面具。",
    },
)

LEGACY_GROUP_NAMES = {
    "A": "行为疯癫",
    "B": "反刍与自我监控",
    "C": "价值与存在",
    "D": "社交与孤独",
    "E": "灵魂拷问",
}


def group_max_scores(
    questions: tuple[dict[str, Any], ...] | list[dict[str, Any]] | None = None,
) -> dict[str, int]:
    active = questions if questions is not None else QUESTIONS
    return {
        group: sum(q["weight"] * 3 for q in active if q["group"] == group)
        for group in GROUP_ORDER
    }


def band_for_score(
    score: int,
    max_score: int = QUIZ_MAX_SCORE,
) -> dict[str, Any]:
    for band in BANDS:
        if band["min"] <= score <= band["max"]:
            return band
    return BANDS[-1] if score > max_score else BANDS[0]


def top_dimensions(
    group_scores: dict[str, int],
    max_scores: dict[str, int] | None = None,
) -> list[str]:
    if not group_scores:
        return []
    max_scores = max_scores or group_max_scores()
    ratios = {
        group: int(group_scores.get(group, 0)) / max(1, int(max_scores.get(group, 1)))
        for group in GROUP_ORDER
    }
    highest = max(ratios.values())
    if highest <= 0:
        return []
    ranked = sorted(GROUP_ORDER, key=lambda group: ratios[group], reverse=True)
    top = [ranked[0]]
    for group in ranked[1:]:
        if highest - ratios[group] <= 0.12:
            top.append(group)
        else:
            break
    return top[:3]


def hidden_results(answers: dict[str, str]) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    attention_question = next(
        (
            question
            for question in ATTENTION_QUESTIONS
            if question["key"] in answers
        ),
        None,
    )
    if (
        attention_question
        and answers.get(attention_question["key"], "").upper()
        != attention_question["correct"]
    ):
        found.append(HIDDEN_RESULTS[0])

    attachment_keys = [
        f"q{number:02d}"
        for number in range(81, 101)
        if f"q{number:02d}" in answers
    ]
    if len(attachment_keys) >= 4 and all(
        answers.get(key, "").upper() == "D" for key in attachment_keys
    ):
        found.append(HIDDEN_RESULTS[1])

    avoidant_keys = ("q81", "q83", "q84")
    if all(
        key in answers and answers.get(key, "").upper() == "D"
        for key in avoidant_keys
    ):
        found.append(HIDDEN_RESULTS[2])
    return found


def _severity_index(score: int, max_score: int) -> int:
    ratio = score / max(1, max_score)
    if ratio <= 30 / 90:
        return 0
    if ratio <= 54 / 90:
        return 1
    if ratio <= 76 / 90:
        return 2
    return 3


def result_extras(
    score: int,
    max_score: int,
    top: list[str],
    answers: dict[str, str],
) -> dict[str, Any]:
    severity_index = _severity_index(score, max_score)
    severity_label, weather_headline = SEVERITY_WEATHER[severity_index]
    primary = top[0] if top else ""
    primary_guide = DIMENSION_GUIDES.get(
        primary,
        {
            "scene": "最近的状态比较平稳，没有哪一维长期抢占你的注意力。",
            "trigger": "偶尔的疲惫、比较或突发任务。",
            "recovery": "保持睡眠、运动和一个可以说真话的人。",
            "mantra": "状态有波动，不代表我不稳定。",
            "keywords": ("状态稳定", "恢复力在线", "轻度观察"),
            "weather": "整体晴好，局部偶有情绪云层",
        },
    )
    persona = PERSONAS.get(primary, ("状态观察员",) * 4)[severity_index]

    combo_title = "单核耗电"
    combo_note = "当前没有特别突出的维度，像一张摊开的状态地图。"
    if len(top) >= 2:
        first, second = top[0], top[1]
        combo_title = f"{GROUPS[first]['name']} × {GROUPS[second]['name']}"
        combo_note = COMBINATION_NOTES.get(
            (first, second),
            "两个高耗能区域叠在一起，容易被同一件小事同时触发。",
        )

    keywords: list[str] = []
    for group in top[:3]:
        for keyword in DIMENSION_GUIDES[group]["keywords"]:
            if keyword not in keywords:
                keywords.append(keyword)
    if not keywords:
        keywords = ["状态稳定", "恢复力在线", "轻度观察"]

    plan = [
        {
            "day": day,
            "title": title,
            "detail": detail,
        }
        for day, title, detail in MICRO_PLAN
    ]
    if primary_guide:
        plan[0]["detail"] = f"记下今天最触发你的一幕：{primary_guide['trigger']}"
        plan[1]["detail"] = primary_guide["recovery"]

    crisis_keys = ("q53", "q107", "q111", "q117")
    crisis_flag = any(
        key in answers and answers.get(key, "").upper() == "D"
        for key in crisis_keys
    )
    support_note = ""
    if severity_index == 3 or crisis_flag:
        support_note = (
            "如果你最近出现伤害自己的想法，请立刻联系一个可信任的人，"
            "或拨打中国大陆心理援助热线 12356；如有紧迫危险，请拨打 120/110。"
            "你不需要一个人扛。"
        )

    score_percent = round(score / max(1, max_score) * 100)
    return {
        "energy": max(0, 100 - score_percent),
        "score_percent": score_percent,
        "severity_key": ("safe", "light", "mid", "heavy")[severity_index],
        "severity_label": severity_label,
        "persona": persona,
        "primary_group": primary,
        "primary_guide": primary_guide,
        "weather_headline": weather_headline,
        "weather_detail": primary_guide.get("weather", "状态整体平稳，暂无明显耗能区。"),
        "combo_title": combo_title,
        "combo_note": combo_note,
        "keywords": keywords,
        "reframe": SEVERITY_REFRAIMES[severity_index],
        "support_need": SUPPORT_NEEDS.get(
            primary,
            "需要的不是被迅速修好，而是被允许按自己的速度恢复。",
        ),
        "micro_plan": plan,
        "support_note": support_note,
    }


def score_answers(answers: dict[str, str]) -> dict[str, Any]:
    group_scores = {group: 0 for group in GROUP_ORDER}
    total = 0
    selected_core = [
        question for question in QUESTIONS if question["key"] in answers
    ]
    for question in selected_core:
        choice = answers.get(question["key"], "").upper()
        if choice not in ("A", "B", "C", "D"):
            continue
        points = "ABCD".index(choice) * int(question["weight"])
        total += points
        group = question["group"]
        if group in group_scores:
            group_scores[group] += points

    max_scores = group_max_scores(selected_core)
    max_score = sum(max_scores.values())
    band = band_for_score(total, max_score)
    top = top_dimensions(group_scores, max_scores)
    attention_question = next(
        (
            question
            for question in ATTENTION_QUESTIONS
            if question["key"] in answers
        ),
        None,
    )
    attention_choice = (
        answers.get(attention_question["key"], "").upper()
        if attention_question
        else ""
    )
    attention_ok = bool(
        attention_question
        and attention_choice == attention_question["correct"]
    )
    attention_note = ""
    if attention_question:
        attention_note = (
            "注意力在线，你确实认真看了题。"
            if attention_ok
            else "你看见了提示，但决定反着来。"
        )

    return {
        "total": total,
        "max_score": max_score,
        "band": band,
        "band_range": f"{band['min']}—{band['max']}",
        "group_scores": group_scores,
        "group_max_scores": max_scores,
        "top_dimensions": top,
        "attention_choice": attention_choice,
        "attention_correct": (
            attention_question["correct"] if attention_question else ""
        ),
        "attention_ok": attention_ok,
        "attention_note": attention_note,
        "hidden_results": hidden_results(answers),
        **result_extras(total, max_score, top, answers),
    }


def answer_rows(answers: dict[str, str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    selected = sorted(
        (
            question
            for question in (*QUESTIONS, *ATTENTION_QUESTIONS)
            if question["key"] in answers
        ),
        key=lambda question: int(question["number"]),
    )
    for question in selected:
        choice = answers.get(question["key"], "").upper()
        option = next((o for o in question["options"] if o["letter"] == choice), None)
        points = "ABCD".index(choice) * int(question["weight"]) if choice in "ABCD" else 0
        rows.append(
            {
                **question,
                "choice": choice,
                "choice_text": option["text"] if option else "未作答",
                "points": points,
            }
        )
    return rows


def dimension_details(
    group_scores: dict[str, int],
    max_scores: dict[str, int],
    top: list[str],
) -> list[dict[str, Any]]:
    details: list[dict[str, Any]] = []
    for group in GROUP_ORDER:
        score = int(group_scores.get(group, 0))
        maximum = int(max_scores.get(group, 1)) or 1
        percent = round(score / maximum * 100) if maximum else 0
        if percent >= 67:
            level = "high"
            level_label = "高耗能"
        elif percent >= 34:
            level = "mid"
            level_label = "波动"
        else:
            level = "low"
            level_label = "低耗能"
        details.append(
            {
                "id": group,
                "name": GROUPS[group]["name"],
                "short": GROUPS[group]["short"],
                "score": score,
                "max": maximum,
                "percent": percent,
                "level": level,
                "level_label": level_label,
                "is_top": group in top,
                "high": GROUPS[group]["high"],
                "low": GROUPS[group]["low"],
            }
        )
    return details
