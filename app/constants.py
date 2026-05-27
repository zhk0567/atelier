"""Site copy and identity (templates receive these via context)."""

from __future__ import annotations

import json
from pathlib import Path

from app.config import ATELIER_ROOT

SITE_NAME = "zhk"
SITE_TITLE = "zhk · 创作者与工程师"
TAGLINE = "用数据与工程，把算法做成能上线、好用、可维护的产品"
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
    "link_github": "GitHub",
    "email_copied": "邮箱已复制到剪贴板",
    "email_copy_failed": "复制失败，请手动选择复制",
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
    "link_all_projects": "项目",
    "label_all_projects_page": "项目",
    "projects_page_lead": "与 GitHub 仓库同步的完整列表；首页仅展示置顶项目。",
    "badge_pinned": "置顶",
    "back_home": "返回首页",
    "label_main_page": "主页面",
    "label_nav": "导航菜单",
    "search_placeholder": "搜索项目、Wiki、博客…",
    "search_hint": "按 / 聚焦 · ↑↓ 选择 · Enter 打开",
    "search_no_results": "未找到匹配页面",
    "search_nav_filter": "侧栏已筛选",
    "label_stats": "统计",
    "label_featured_projects": "特色项目",
    "label_data_portal": "数据分类",
    "wiki_footer_note": "个人站点",
    "wiki_attribution": "部分图标来自 Minecraft Wiki（CC BY-SA 3.0）",
    "label_wallpaper": "壁纸",
    "wallpaper_random": "随机",
    "label_contact": "快速联系",
    "ph_name": "姓名",
    "ph_email": "邮箱",
    "ph_message": "留言内容",
    "btn_send": "发送演示",
    "label_travel": "个人旅游",
    "travel_index_lead": "徒步与旅途中的风景记录。",
    "travel_back_index": "全部旅行",
    "label_blog": "博客",
    "link_blog_enter": "进入博客",
    "label_blog_series": "系列",
    "label_blog_projects": "项目",
    "label_blog_hotspot": "热点",
    "link_hotspot_series": "热点专题",
    "blog_hotspot_lead": "追踪 AI、神经科技与人机交互等领域的前沿观察与思辨。",
    "label_blog_topics": "专题",
    "blog_topics_lead": "独立主题的科普与兴趣文章，单篇成文、随时阅读。",
    "blog_series_lead": "按技术栈或题系统整的连载指南，适合系统阅读与长期查阅。",
    "link_framework_guides": "Framework 技术栈指南",
    "link_algorithm_guides": "Algorithm 算法与刷题",
    "blog_home_lead": "技术专题与连载指南，按系列浏览。",
    "blog_series_unit": "篇",
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

# HTML pages: short private cache (reduces repeat load on 2GB VPS)
HTML_CACHE_HEADERS = {
    "Cache-Control": "private, max-age=120, stale-while-revalidate=300",
}

STATIC_CACHE_HEADERS = {
    "Cache-Control": "public, max-age=604800, immutable",
}

WALLPAPER_CACHE_HEADERS = {
    "Cache-Control": "public, max-age=3600",
}


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
