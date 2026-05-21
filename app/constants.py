"""Site copy and identity (templates receive these via context)."""

from __future__ import annotations

import json
from pathlib import Path

from app.config import ATELIER_ROOT

SITE_NAME = "zhk"
SITE_TITLE = "zhk · 创作者与工程师"
TAGLINE = "用数据与工程，把算法做成能上线的产品"
HERO_SUBTITLE = "数据科学 · Android / Kotlin · 计算机视觉"
BIO = (
    "数据科学与大数据技术在读，主攻 Python / Kotlin 与 Android，做 CV、语音与 OCR 从训练到端侧落地。"
    "项目以移动应用与视觉为主；数模省一、美赛 H 奖、华数杯 O 奖，英语六级。"
)
FOCUS = "Python · CV / OCR · 移动与多模态"
AVAILABILITY = "在读学生 · 项目与竞赛导向"
LOCATION = "中国"
EMAIL = "3283409866@qq.com"
GITHUB = "https://github.com/zhk0567"
LINKEDIN = "https://linkedin.com"
TWITTER = "https://x.com"

UI = {
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
    "browse_lead": "",
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
    "wiki_footer_note": "个人 Wiki",
    "wiki_attribution": "部分图标来自 Minecraft Wiki（CC BY-SA 3.0）",
    "label_wallpaper": "动态壁纸",
    "wallpaper_random": "随机",
    "wallpaper_none": "无壁纸",
    "label_contact": "快速联系",
    "ph_name": "姓名",
    "ph_email": "邮箱",
    "ph_message": "留言内容",
    "btn_send": "发送演示",
    "label_blog": "博客",
    "link_framework_guides": "Framework 技术栈指南",
    "blog_home_lead": "Framework 官方指南连载与其它技术笔记。",
    "label_wiki_toc": "本文档",
    "link_wiki_index": "目录总览",
    "wiki_pager_prev": "上一页",
    "wiki_pager_next": "下一页",
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

HTML_NO_CACHE = {"Cache-Control": "no-cache, must-revalidate", "Pragma": "no-cache"}


def load_site_identity() -> tuple[str, str]:
    global SITE_NAME, SITE_TITLE
    path = ATELIER_ROOT / "site_identity.json"
    default_name = "zhk"
    default_title = "zhk · 创作者与工程师"
    if not path.is_file():
        SITE_NAME, SITE_TITLE = default_name, default_title
        return SITE_NAME, SITE_TITLE
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError, TypeError):
        SITE_NAME, SITE_TITLE = default_name, default_title
        return SITE_NAME, SITE_TITLE
    SITE_NAME = str(data.get("site_name", default_name)).strip() or default_name
    SITE_TITLE = str(data.get("site_title", default_title)).strip() or default_title
    return SITE_NAME, SITE_TITLE


load_site_identity()
