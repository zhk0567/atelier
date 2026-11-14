# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- Primary: visitors browsing zhk’s personal site — recruiters, peers, classmates, and curious readers who want projects, writing, and contact context.
- Secondary: the site owner (zhk) operating the neurosis quiz admin and reviewing visitor wishes / feedback.
- Quiz visitors: people taking the optional “精神状态深度自测” for curiosity; not clinical users.

## Product Purpose

zhk’s personal atelier at zhkun.xyz: a FastAPI + Jinja2 portfolio that showcases projects (with Wiki docs), technical blog series, travel notes, personal rules/wishes, and a lighthearted multi-question quiz — so visitors can understand what zhk builds and how to reach them.

Success: a visitor can find projects/writing quickly, read comfortably in light or dark theme, and complete optional quiz / wish / feedback flows without friction.

## Positioning

A Minecraft Wiki–inspired Vector skin on a living personal engineering site (not a generic portfolio template): wallpaper, glass panels, progressive links, and wiki-like navigation over real project Wikis, Framework/Algorithm guides, and competition-backed work.

## Operating Context

- Local: Windows + PowerShell, `.\run.ps1` → `http://127.0.0.1:8000`
- Production: Alibaba Cloud ECS + systemd + Nginx + HTTPS (zhkun.xyz); deploy only after explicit owner approval
- Content: Jinja2 templates, Markdown blogs/Wikis, xlsx browse hubs, SQLite for quiz/wishes
- Themes: light/dark via `data-theme` + localStorage; optional wallpaper layer

## Capabilities and Constraints

- Public: home, projects, project detail, Wiki docs, xlsx browse, blog index/series/posts, travel, personal code + visitor wish form, neurosis quiz + privacy/records/feedback/results
- Private: admin under `/ops/neurosis-7f3c9a2e` (login, dashboard, attempts, feedback, wishes)
- Do not change quiz scoring logic, routes, or deploy configs during design polish
- Do not invent testimonials, credentials, or metrics beyond site copy / `app/constants.py` / content files
- Brand visual commitment: preserve Minecraft Wiki / Vector world; polish and selective bolder on home — no wholesale rebrand

## Brand Commitments

- Name: **zhk** (`SITE_NAME`); title **zhk · 创作者与工程师**
- Tagline: 用数据与工程，把算法做成能上线的产品
- Voice: concise Chinese, engineering-forward, personal but not corporate
- Visual: zh.minecraft.wiki–aligned Vector/Codex tokens (`wiki.css`); green progressive CTAs on home portal (`mp-portal.css`); quiz and admin use scoped skins
- Attribution: partial icons from Minecraft Wiki (CC BY-SA 3.0)

## Evidence on Hand

- Live identity & copy: `app/constants.py`, `site_identity.json`
- Design tokens: `static/css/wiki.css`, `mp-portal.css`, `personal.css`, `neurosis-quiz.css`, `neurosis-admin.css`
- Templates: `templates/` (wiki shell + page templates)
- Content: `Blog/`, `Wiki/`, `config/projects.json`, travel & personal data under `data/`
- No fabricated case studies or third-party quotes

## Product Principles

1. **Wiki-first navigation** — search, sidebar, and progressive links beat marketing chrome.
2. **Preserve the Vector world** — refine consistency; do not swap identity for trendy defaults.
3. **Reading and operating are different modes** — blog/Wiki optimize comprehension; quiz/admin optimize task completion.
4. **Honest content only** — never invent awards, clients, or clinical claims for the quiz.
5. **Ship locally first** — owner reviews on localhost before any cloud deploy.

## Accessibility & Inclusion

- Target usable keyboard focus, visible focus rings, and touch-friendly targets on shared chrome.
- Support light and dark themes with readable contrast on wallpaper scrims.
- Quiz is entertainment / self-reflection copy — not medical advice; keep privacy path easy to find.
