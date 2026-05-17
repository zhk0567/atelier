"""Personal site — single Python entry point."""

import json
import os
import re
import subprocess
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

import markdown
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from site_data import (
    BLOG_DIR,
    build_data_hubs,
    get_blog_post,
    get_browse_page,
    get_spreadsheet_context,
    load_site_data,
    merge_projects_catalog,
)


def _kill_listeners_on_port(port: int) -> None:
    """End processes already listening on *port* so a new dev server can bind (Windows)."""
    if sys.platform != "win32":
        return
    my_pid = os.getpid()
    # Note: PowerShell reserved $PID — use $procId in foreach.
    ps = (
        f"$ids = Get-NetTCPConnection -LocalPort {port} -State Listen -ErrorAction SilentlyContinue "
        f"| Select-Object -ExpandProperty OwningProcess -Unique; "
        f"foreach ($procId in $ids) {{ "
        f"  if ($procId -and $procId -ne 0 -and $procId -ne {my_pid}) {{ "
        f"    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue "
        f"}}}}"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
        check=False,
        timeout=20,
    )


UVICORN_HOST = "127.0.0.1"
UVICORN_PORT = 8000


def _atelier_root() -> Path:
    return Path(__file__).resolve().parent


def _load_site_identity() -> tuple[str, str]:
    """Display name / title — prefer site_identity.json next to main.py (single source of truth)."""
    path = _atelier_root() / "site_identity.json"
    default_name = "zhk"
    default_title = "zhk · 创作者与工程师"
    if not path.is_file():
        return default_name, default_title
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError, TypeError):
        return default_name, default_title
    name = str(data.get("site_name", default_name)).strip() or default_name
    title = str(data.get("site_title", default_title)).strip() or default_title
    return name, title


SITE_NAME, SITE_TITLE = _load_site_identity()
TAGLINE = "用数据与工程，把算法做成能上线的产品"
HERO_SUBTITLE = "数据科学 · Android / Kotlin · 计算机视觉"
BIO = (
    "数据科学与大数据技术在读，主攻 Python / Kotlin 与 Android，做 CV、语音与 OCR 从训练到端侧落地。"
    "项目以移动应用与视觉为主；数模省一、美赛 H 奖、华数杯 O 奖，英语六级。"
)
FOCUS = "Python · CV / OCR · 移动与多模态"
AVAILABILITY = "在读学生 · 项目与竞赛导向"
LOCATION = "中国"
EMAIL = "hello@example.com"
GITHUB = "https://github.com/zhk0567"
LINKEDIN = "https://linkedin.com"
TWITTER = "https://x.com"

# UI copy (all Chinese lives here — templates stay ASCII-only)
UI = {
    "badge_available": "可接项目",
    "copyright_prefix": "©",
    "sep_dot": "·",
    "toggle_theme": "切换主题",
    "label_profile": "个人概览",
    "hello": "你好，我是",
    "fact_focus": "方向",
    "fact_status": "状态",
    "fact_email": "邮箱",
    "fact_education": "教育",
    "fact_reading": "阅读",
    "btn_email": "邮件联系",
    "label_about": "关于我",
    "stat_years": "开发经验",
    "stat_years_unit": "年+",
    "stat_projects": "开源项目",
    "stat_projects_unit": "个",
    "stat_skills": "技术栈",
    "stat_skills_unit": "项",
    "stat_clients": "竞赛与建模",
    "stat_clients_unit": "项+",
    "highlight_1": "CV / OCR 落地",
    "highlight_2": "Android / Kotlin",
    "highlight_3": "语音与多模态",
    "highlight_4": "数模与算法实践",
    "label_skills": "数据入口",
    "browse_lead": "以下内容来自 zhita_settings.xlsx，按工作表分类浏览。",
    "skill_fe": "前端 React / TS",
    "skill_be": "后端 Python / API",
    "skill_ui": "设计 UI / 动效",
    "skill_ops": "工程化 DevOps",
    "label_projects": "精选项目",
    "link_all_projects": "全部项目",
    "label_all_projects_page": "全部项目",
    "projects_page_lead": "与 GitHub 仓库同步的完整列表；首页仅展示置顶项目。",
    "badge_pinned": "置顶",
    "back_home": "返回首页",
    "label_main_page": "主页面",
    "label_nav": "导航菜单",
    "search_placeholder": "搜索本站…",
    "label_stats": "统计",
    "label_featured_projects": "特色项目",
    "label_data_portal": "数据分类",
    "wiki_footer_note": "个人 Wiki · 数据来自 zhita_settings.xlsx",
    "wiki_attribution": "部分图标来自 Minecraft Wiki（CC BY-SA 3.0）",
    "label_wallpaper": "动态壁纸",
    "wallpaper_random": "随机",
    "wallpaper_none": "无壁纸",
    "label_contact": "快速联系",
    "ph_name": "姓名",
    "ph_email": "邮箱",
    "ph_message": "留言内容",
    "btn_send": "发送演示",
}

STATS = [
    {"value": 5, "unit": UI["stat_years_unit"], "label": UI["stat_years"]},
    {"value": 6, "unit": UI["stat_projects_unit"], "label": UI["stat_projects"]},
    {"value": 12, "unit": UI["stat_skills_unit"], "label": UI["stat_skills"]},
    {"value": 7, "unit": UI["stat_clients_unit"], "label": UI["stat_clients"]},
]

SKILLS = [
    {"name": UI["skill_fe"], "width": "92%"},
    {"name": UI["skill_be"], "width": "88%"},
    {"name": UI["skill_ui"], "width": "85%"},
    {"name": UI["skill_ops"], "width": "78%"},
]

HIGHLIGHTS = [UI["highlight_1"], UI["highlight_2"], UI["highlight_3"], UI["highlight_4"]]

# ── Projects (synced with Wiki/) ───────────────────────────────────────────────
# Homepage shows only PINNED_PROJECT_IDS (like GitHub pinned repos).
PINNED_PROJECT_IDS = (
    "learning-terminal",
    "clothing-classification",
    "framework",
    "english-speaking-trainer",
)

ALL_PROJECTS = [
    {
        "id": "learning-terminal",
        "title": "古韵薪传 · 智能学习终端",
        "summary": "多端智能学习终端：Web 与微信小程序协同，覆盖故事内容管理、主题系统、状态管理与构建部署。",
        "category": "教育 · 全栈",
        "year": "2025",
        "tags": ["Web", "微信小程序", "React", "主题系统"],
        "github": "https://github.com/zhk0567/Intelligent-Learning-Terminal/tree/guyunxinchuan",
        "wiki_slug": "Intelligent-Learning-Terminal-guyunxinchuan",
        "thumb": 1,
        "highlights": [
            "Web 与小程序双端架构",
            "可复用组件库与导航路由",
            "数据流与故事内容管理",
        ],
    },
    {
        "id": "clothing-classification",
        "title": "服装图像深度学习分类",
        "summary": "基于 ResNet18 与 DeepFashion 数据集的服装图像分类系统，含训练流水线、数据分片与模型集成。",
        "category": "深度学习 · CV",
        "year": "2025",
        "tags": ["Java", "ResNet18", "DeepFashion", "Kotlin"],
        "github": "https://github.com/zhk0567/Clothing---Classification",
        "wiki_slug": "Clothing-Classification",
        "thumb": 2,
        "highlights": [
            "完整训练与评估流程",
            "拍照 / 上传图片分类",
            "后端 API 与模型部署",
        ],
    },
    {
        "id": "framework",
        "title": "Framework 多技术栈示例",
        "summary": "汇集 Laravel、Symfony、.NET、Go、Node、Python 等后端与 React Native、Svelte、Astro 等前端的模块化全栈参考实现。",
        "category": "架构 · 全栈",
        "year": "2025",
        "tags": ["Laravel", "Go", "React Native", "Astro"],
        "github": "https://github.com/zhk0567/Framework",
        "wiki_slug": "Framework",
        "thumb": 3,
        "highlights": [
            "多后端技术栈对照",
            "多前端框架示例",
            "API 与部署实践",
        ],
    },
    {
        "id": "english-speaking-trainer",
        "title": "英语口语训练应用",
        "summary": "基于 TED Talks 与 Psych2Go 内容的 Android 口语训练：文章阅读、语音模仿、单词查询与悬浮球查词。",
        "category": "移动 · 教育",
        "year": "2025",
        "tags": ["Android", "Kotlin", "语音识别", "口语"],
        "github": "https://github.com/zhk0567/English-Speaking-Trainer",
        "wiki_slug": "English-Speaking-Trainer",
        "thumb": 4,
        "highlights": [
            "跟读与发音反馈",
            "单词查询系统",
            "悬浮球快捷查词",
        ],
    },
    {
        "id": "nexus",
        "title": "NEXUS Unified 智能语音交互平台",
        "summary": "企业级智能语音交互：实时 ASR、DeepSeek 对话、Edge-TTS 合成，Jetpack Compose UI，支持连续对话与故事阅读。",
        "category": "Android · 语音 AI",
        "year": "2025",
        "tags": ["Kotlin", "ASR", "TTS", "Compose"],
        "github": "https://github.com/zhk0567/NEXUS",
        "wiki_slug": "NEXUS",
        "thumb": 5,
        "highlights": [
            "Dolphin ASR + DeepSeek + Edge-TTS",
            "实时语音通话与历史记录",
            "故事阅读与企业级监控",
        ],
    },
    {
        "id": "algorithm",
        "title": "Algorithm 算法与数据结构",
        "summary": "Python / C++ 双语言算法仓库：完整数据结构实现、LeetCode 题解、学习路线与面试高频专题。",
        "category": "算法 · 面试",
        "year": "2025",
        "tags": ["Python", "C++", "LeetCode", "数据结构"],
        "github": "https://github.com/zhk0567/Algorithm",
        "wiki_slug": "Algorithm",
        "thumb": 6,
        "highlights": [
            "线性 / 树 / 图与高级专题",
            "LeetCode 题解与刷题指南",
            "并发与数学工具链",
        ],
    },
]
# ─────────────────────────────────────────────────────────────────────────────

BASE_DIR = _atelier_root()
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"
WIKI_DIR = BASE_DIR / "Wiki"
WALLPAPER_EXTS = {".mp4", ".webm", ".mov", ".jpg", ".jpeg", ".png", ".webp", ".gif"}
WALLPAPER_VIDEO_EXTS = {".mp4", ".webm", ".mov"}
_WALLPAPER_PATHS: dict[str, Path] = {}
WIKI_IMG_DIR = STATIC_DIR / "img" / "wiki"
WIKI_MANIFEST_PATH = WIKI_IMG_DIR / "manifest.json"

HUB_ICON_FILES: dict[str, str] = {
    "projects": "crafting_table",
    "certs": "item_map",
    "hobbies": "item_compass",
    "books": "item_book",
    "anime": "bookshelf",
    "movies": "bookshelf",
    "games": "item_compass",
    "school": "oak_planks",
    "articles": "item_book",
}

templates = Jinja2Templates(directory=TEMPLATES_DIR)
_HTML_NO_CACHE = {"Cache-Control": "no-cache, must-revalidate", "Pragma": "no-cache"}

_WIKI_LINK_RE = re.compile(r"^- \[(.+?)\]\(\./(.+?)\)\s*$")
_WIKI_BOILERPLATE_RES = (
    re.compile(r"基于.*README.*生成", re.I),
    re.compile(r"请参考源仓库", re.I),
    re.compile(r"如需最新详细信息", re.I),
    re.compile(r"wiki\s*页面基于", re.I),
    re.compile(r"此\s*wiki\s*页面基于", re.I),
    re.compile(r"本文档基于.*仓库", re.I),
    re.compile(r"文档内容生成", re.I),
)
_WIKI_SKIP_SECTION_RE = re.compile(
    r"^##\s*(相关文件|相关链接|Relevant\s*Files?|Source\s*Files?|参考资料)\s*$",
    re.I,
)
_WIKI_GITHUB_LINK_RE = re.compile(
    r"\[([^\]]+)\]\((https?://(?:www\.)?(?:github|gitee)\.com/[^)]+)\)",
    re.I,
)


def _sanitize_wiki_markdown(raw: str) -> str:
    """Strip auto-generated disclaimers, source-file sections, and repo deep links."""
    out: list[str] = []
    skip_section = False
    for line in raw.splitlines():
        if _WIKI_SKIP_SECTION_RE.match(line.strip()):
            skip_section = True
            continue
        if skip_section:
            if line.startswith("## "):
                skip_section = False
            else:
                continue
        stripped = line.strip()
        if any(p.search(stripped) for p in _WIKI_BOILERPLATE_RES):
            continue
        if re.match(r"^\*?\s*Sources?:", stripped, re.I):
            continue
        if re.match(r"^[-*]\s*\[README\.md\]", stripped, re.I):
            continue
        if re.match(r"^[-*]\s*\[.*README\.md.*\]\(https?://", stripped, re.I):
            continue
        line = _WIKI_GITHUB_LINK_RE.sub(r"\1", line)
        line = re.sub(r"\[([^\]]+)\]\(\./[^)]+\)", r"\1", line)
        out.append(line)
    return "\n".join(out).strip() + "\n"


def _sanitize_wiki_html(html: str) -> str:
    html = re.sub(
        r"<p>[^<]*(?:基于|参考).*README[^<]*(?:生成|源仓库)[^<]*</p>",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r"<p>\s*<em>?Sources?:[^<]*</em>?\s*</p>",
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<a\s+href="https?://(?:www\.)?(?:github|gitee)\.com/[^"]*"[^>]*>(.*?)</a>',
        r"\1",
        html,
        flags=re.I,
    )
    html = re.sub(r"<p>\s*</p>", "", html)
    return html


@asynccontextmanager
async def _lifespan(app: FastAPI):
    main_path = Path(__file__).resolve()
    print(f"[atelier] loaded main.py from: {main_path}", flush=True)
    print(f"[atelier] SITE_NAME={SITE_NAME!r} SITE_TITLE={SITE_TITLE!r}", flush=True)
    yield


app = FastAPI(
    title="Personal Site",
    docs_url=None,
    redoc_url=None,
    lifespan=_lifespan,
)


def _media_type_for_path(path: Path) -> str:
    ext = path.suffix.lower()
    return {
        ".mp4": "video/mp4",
        ".webm": "video/webm",
        ".mov": "video/quicktime",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "application/octet-stream")


def list_wallpapers() -> list[dict]:
    """Scan data/ for wallpaper files; stable ids wp-0, wp-1, …"""
    global _WALLPAPER_PATHS
    _WALLPAPER_PATHS.clear()
    if not DATA_DIR.is_dir():
        return []
    files = sorted(
        (p for p in DATA_DIR.iterdir() if p.is_file() and p.suffix.lower() in WALLPAPER_EXTS),
        key=lambda p: p.name.lower(),
    )
    items: list[dict] = []
    for i, path in enumerate(files):
        wid = f"wp-{i}"
        _WALLPAPER_PATHS[wid] = path
        items.append({
            "id": wid,
            "label": path.stem,
            "url": f"/wallpaper/{wid}",
            "is_video": path.suffix.lower() in WALLPAPER_VIDEO_EXTS,
        })
    return items


def load_wiki_assets() -> dict[str, str]:
    """Asset stem -> public URL for files that exist under static/img/wiki/."""
    out: dict[str, str] = {}
    if WIKI_IMG_DIR.is_dir():
        for path in WIKI_IMG_DIR.glob("*.png"):
            out[path.stem] = f"/static/img/wiki/{path.name}"
        for path in WIKI_IMG_DIR.glob("*.gif"):
            out[path.stem] = f"/static/img/wiki/{path.name}"
    return out


def build_hub_icons(assets: dict[str, str]) -> dict[str, str]:
    fallback = assets.get("crafting_table", "/static/img/wiki/crafting_table.png")
    return {
        hub_id: assets.get(stem, fallback)
        for hub_id, stem in HUB_ICON_FILES.items()
    }


def build_wiki_nav(hubs: list[dict]) -> list[dict]:
    """Sidebar navigation groups for wiki layout."""
    portal_children = [
        {"label": h["label"], "url": h["url"], "external": False}
        for h in hubs
    ]
    return [
        {"label": "站点", "children": [
            {"label": "主页面", "url": "/", "external": False},
            {"label": "全部项目", "url": "/projects", "external": False},
        ]},
        {"label": "数据分类", "children": portal_children},
    ]


def _site_context() -> dict:
    hubs: list[dict] = []
    try:
        data = load_site_data()
        sheet = get_spreadsheet_context()
        hubs = build_data_hubs(data, len(get_all_projects()))
    except Exception as exc:
        print(f"[atelier] zhita_settings.xlsx load failed: {exc}", flush=True)
        sheet = {}
    site_name = sheet.get("site_name", SITE_NAME)
    sn = (site_name or "").strip()
    mark = sn[:4] if sn else "?"
    ui = {**UI, **sheet.get("ui", {})}
    wiki_assets = load_wiki_assets()
    return {
        "site_name": site_name,
        "brand_mark": mark,
        "site_title": sheet.get("site_title", SITE_TITLE),
        "tagline": sheet.get("tagline", TAGLINE),
        "hero_subtitle": sheet.get("hero_subtitle", HERO_SUBTITLE),
        "bio": sheet.get("bio", BIO),
        "focus": sheet.get("focus", FOCUS),
        "availability": sheet.get("availability", AVAILABILITY),
        "location": LOCATION,
        "email": EMAIL,
        "github": GITHUB,
        "linkedin": LINKEDIN,
        "twitter": TWITTER,
        "year": datetime.now().year,
        "ui": ui,
        "stats": sheet.get("stats", STATS),
        "data_hubs": hubs,
        "wiki_nav": build_wiki_nav(hubs),
        "wiki_assets": wiki_assets,
        "hub_icons": build_hub_icons(wiki_assets),
        "wallpapers": list_wallpapers(),
        "highlights": sheet.get("highlights", HIGHLIGHTS),
        "certificates": sheet.get("certificates", []),
        "education_line": sheet.get("education_line", ""),
        "reading_line": sheet.get("reading_line", ""),
        "books_featured": sheet.get("books_featured", []),
        "games_count": sheet.get("games_count", 0),
    }


def get_all_projects() -> list[dict]:
    try:
        return merge_projects_catalog(ALL_PROJECTS)
    except Exception as exc:
        print(f"[atelier] project merge failed: {exc}", flush=True)
        return list(ALL_PROJECTS)


def get_pinned_projects() -> list[dict]:
    by_id = {p["id"]: p for p in get_all_projects()}
    return [by_id[i] for i in PINNED_PROJECT_IDS if i in by_id]


def get_project(project_id: str) -> dict | None:
    return next((p for p in get_all_projects() if p["id"] == project_id), None)


def list_wiki_pages(wiki_slug: str) -> list[dict[str, str]]:
    index_path = WIKI_DIR / wiki_slug / "index.md"
    if not index_path.is_file():
        return []
    pages: list[dict[str, str]] = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        match = _WIKI_LINK_RE.match(line.strip())
        if match:
            pages.append({
                "title": match.group(1),
                "view_url": f"/docs/{wiki_slug}/{match.group(2)}",
            })
    return pages


_BLOG_FRONTMATTER_RE = re.compile(r"^---\s*\r?\n.*?\r?\n---\s*\r?\n", re.DOTALL)


def render_blog_markdown(slug: str) -> tuple[dict[str, str], str]:
    """Return (post meta, HTML body) for a published blog slug."""
    post = get_blog_post(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    folder = post.get("folder", "")
    index_path = BLOG_DIR / folder / "index.md"
    if not index_path.is_file():
        raise HTTPException(status_code=404, detail="Blog post not found")
    raw = index_path.read_text(encoding="utf-8")
    raw = _BLOG_FRONTMATTER_RE.sub("", raw, count=1)
    raw = re.sub(
        r"!\[([^\]]*)\]\(images/([^)]+)\)",
        rf"![\1](/static/blog/{slug}/\2)",
        raw,
    )
    html = markdown.markdown(raw, extensions=["tables", "fenced_code", "nl2br"])
    return post, html


def render_wiki_markdown(wiki_slug: str, page: str) -> str:
    safe = Path(page).name
    file_path = WIKI_DIR / wiki_slug / safe
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Wiki page not found")
    if file_path.resolve().parent != (WIKI_DIR / wiki_slug).resolve():
        raise HTTPException(status_code=404, detail="Wiki page not found")
    raw = file_path.read_text(encoding="utf-8")
    raw = re.sub(r"<!--.*?-->", "", raw, flags=re.DOTALL)
    raw = _sanitize_wiki_markdown(raw)
    html = markdown.markdown(raw, extensions=["tables", "fenced_code", "nl2br"])
    return _sanitize_wiki_html(html)


@app.get("/api/site", include_in_schema=False)
@app.get("/atelier-site.json", include_in_schema=False)
async def api_site():
    """Who is this server? Open in browser if the homepage shows the wrong name."""
    return JSONResponse(
        {
            "site_name": SITE_NAME,
            "site_title": SITE_TITLE,
            "main_py": str(Path(__file__).resolve()),
            "identity_json": str((_atelier_root() / "site_identity.json").resolve()),
        },
        headers=_HTML_NO_CACHE,
    )


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return RedirectResponse(url="/static/favicon.svg", status_code=301)


@app.get("/")
async def index(request: Request):
    pinned = get_pinned_projects()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            **_site_context(),
            "projects": pinned,
            "project_count": len(pinned),
            "total_project_count": len(get_all_projects()),
        },
        headers=_HTML_NO_CACHE,
    )


@app.get("/browse/{hub_id}")
async def browse_hub(request: Request, hub_id: str):
    page = get_browse_page(hub_id)
    if not page:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        request=request,
        name="browse.html",
        context={
            **_site_context(),
            **page,
            "item_count": sum(
                len(s.get("items", [])) for s in page.get("sections", [])
            )
            if page.get("sections")
            else len(page.get("items", [])),
        },
        headers=_HTML_NO_CACHE,
    )


@app.get("/projects")
async def projects_list(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="projects.html",
        context={
            **_site_context(),
            "projects": get_all_projects(),
            "pinned_ids": set(PINNED_PROJECT_IDS),
            "project_count": len(get_all_projects()),
        },
        headers=_HTML_NO_CACHE,
    )


@app.get("/project/{project_id}")
async def project_detail(request: Request, project_id: str):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(
        request=request,
        name="project.html",
        context={
            **_site_context(),
            "project": project,
            "wiki_pages": list_wiki_pages(project["wiki_slug"]),
            "wiki_index_url": f"/docs/{project['wiki_slug']}/index.md",
        },
        headers=_HTML_NO_CACHE,
    )


@app.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str):
    post, html_body = render_blog_markdown(slug)
    return templates.TemplateResponse(
        request=request,
        name="blog_post.html",
        context={
            **_site_context(),
            "post": post,
            "content_html": html_body,
        },
        headers=_HTML_NO_CACHE,
    )


@app.get("/docs/{wiki_slug}/{page}", response_class=HTMLResponse)
async def wiki_doc(request: Request, wiki_slug: str, page: str):
    project = next((p for p in get_all_projects() if p["wiki_slug"] == wiki_slug), None)
    html_body = render_wiki_markdown(wiki_slug, page)
    return templates.TemplateResponse(
        request=request,
        name="wiki.html",
        context={
            **_site_context(),
            "wiki_slug": wiki_slug,
            "page": page,
            "content_html": html_body,
            "project": project,
            "project_url": f"/project/{project['id']}" if project else "/",
        },
        headers=_HTML_NO_CACHE,
    )


@app.get("/wiki", include_in_schema=False)
@app.get("/wiki/{path:path}", include_in_schema=False)
async def wiki_raw_forbidden(path: str = ""):
    """Raw Markdown under /wiki is not exposed; use /docs/... for reading."""
    raise HTTPException(status_code=404, detail="Not found")


@app.get("/wallpaper/{wp_id}", include_in_schema=False)
async def serve_wallpaper(wp_id: str):
    if wp_id not in _WALLPAPER_PATHS:
        list_wallpapers()
    path = _WALLPAPER_PATHS.get(wp_id)
    if not path or not path.is_file():
        raise HTTPException(status_code=404, detail="Wallpaper not found")
    try:
        path.resolve().relative_to(DATA_DIR.resolve())
    except ValueError:
        raise HTTPException(status_code=404, detail="Wallpaper not found") from None
    return FileResponse(path, media_type=_media_type_for_path(path))


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


if __name__ == "__main__":
    mp = Path(__file__).resolve()
    print(f"[atelier] starting uvicorn from: {mp}", flush=True)
    print(f"[atelier] SITE_NAME={SITE_NAME!r}", flush=True)
    print(f"[atelier] freeing port {UVICORN_PORT} (stop old listeners)…", flush=True)
    _kill_listeners_on_port(UVICORN_PORT)
    uvicorn.run(
        "main:app",
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        reload=False,
    )
