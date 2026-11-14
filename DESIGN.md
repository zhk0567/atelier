---
name: zhk atelier
description: Minecraft Wiki Vector skin for a personal engineering portfolio
colors:
  progressive: "#2851a3"
  progressive-hover: "#1f4085"
  progressive-active: "#162f63"
  visited: "#5a4f9e"
  base: "#1a1c1e"
  emphasized: "#0a0c0e"
  subtle: "#3d4248"
  placeholder: "#5c6168"
  inverted: "#ffffff"
  border-base: "#8b9199"
  border-subtle: "#b8bcc4"
  bg-base: "#ffffff"
  bg-neutral: "#e4e6ea"
  bg-neutral-subtle: "#f4f5f7"
  bg-progressive-subtle: "#e3edff"
  surface-elevated: "#ffffff"
  surface-solid: "#ffffff"
  surface-solid-muted: "#eef0f3"
  progressive-dark: "#7eb0ff"
  base-dark: "#eceef2"
  bg-base-dark: "#1e2022"
  surface-solid-dark: "#2e3033"
  button-progressive: "#3a971e"
  button-progressive-dark: "#137342"
  admin-accent: "#315bd6"
  admin-danger: "#b52d3c"
typography:
  display:
    fontFamily: "system-ui, -apple-system, Segoe UI, Noto Sans SC, PingFang SC, sans-serif"
    fontSize: "clamp(1.75rem, 4vw, 2.25rem)"
    fontWeight: 700
    lineHeight: 1.25
  headline:
    fontFamily: "system-ui, -apple-system, Segoe UI, Noto Sans SC, PingFang SC, sans-serif"
    fontSize: "1.2em"
    fontWeight: 700
    lineHeight: 1.35
  title:
    fontFamily: "Linux Libertine, Noto Serif SC, Georgia, Times New Roman, serif"
    fontSize: "1.35rem"
    fontWeight: 600
    lineHeight: 1.4
  body:
    fontFamily: "system-ui, -apple-system, Segoe UI, Noto Sans SC, PingFang SC, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.65
  label:
    fontFamily: "system-ui, -apple-system, Segoe UI, Noto Sans SC, PingFang SC, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 500
    lineHeight: 1.4
rounded:
  base: "3px"
  sm: "4px"
  md: "6px"
  lg: "10px"
  admin: "12px"
spacing:
  section: "1rem"
  layout-gap: "1rem"
  content-max: "60rem"
  sidebar: "11.5rem"
  header: "3.375rem"
  touch-min: "2.75rem"
components:
  link-progressive:
    textColor: "{colors.progressive}"
  button-wiki:
    backgroundColor: "{colors.bg-neutral-subtle}"
    textColor: "{colors.base}"
    rounded: "{rounded.md}"
    padding: "0.45rem 0.85rem"
  button-progressive-portal:
    backgroundColor: "{colors.button-progressive}"
    textColor: "{colors.inverted}"
    rounded: "{rounded.sm}"
    padding: "0.55rem 1rem"
  panel-glass:
    backgroundColor: "{colors.surface-solid}"
    rounded: "{rounded.lg}"
  tag-chip:
    backgroundColor: "{colors.bg-progressive-subtle}"
    textColor: "{colors.progressive}"
    rounded: "{rounded.sm}"
    padding: "0.15rem 0.45rem"
  admin-button-primary:
    backgroundColor: "{colors.admin-accent}"
    textColor: "{colors.inverted}"
    rounded: "{rounded.admin}"
    padding: "0.55rem 1rem"
---

# Design System: zhk atelier

## Overview

**Creative North Star: "The Codex Atelier"**

A personal engineering site dressed as a living Vector/Codex wiki: wallpaper behind frosted panels, progressive blue links, green portal CTAs, and Minecraft-adjacent iconography used as texture — never as parody. Density stays informational (lists, sections, sidebars) rather than marketing-card grids.

Quiz and admin keep scoped skins (`.nq-*`, `.na-*`) so Operate tasks stay scan-first while the public shell stays wiki-true.

**Key Characteristics:**
- Vector progressive blue + portal green CTAs
- Light/dark via `data-theme`, wallpaper scrims
- Sharp-small radii (3–10px), soft elevated shadows
- System/Noto SC stacks; serif reserved for reading titles
- Rejected: purple-gradient “AI default”, Inter-as-identity, nested card dashboards, eyebrow kickers

## Colors

Progressive blue for links and focus; portal green for primary home CTAs; visited purple for history; neutrals carry glass panels over wallpaper.

### Primary
- **Progressive Blue** (`#2851a3`): links, focus rings, interactive emphasis
- **Portal Green** (`#3a971e`): home progressive buttons

### Secondary
- **Visited Violet** (`#5a4f9e`): visited links only

### Neutral
- Light surfaces `#fff` / `#f4f5f7` / `#e4e6ea`; dark `#1e2022` / `#2e3033`
- Text `#1a1c1e` → subtle `#3d4248`; dark inverted accordingly

### Admin / Quiz accents
- Admin accent `#315bd6`, danger `#b52d3c` — Operate-only, do not bleed into wiki chrome

## Typography

Sans for UI chrome and portal; serif optional for long-form reading titles. Body line-height ~1.65; content measure capped near `60rem`.

## Layout

- Header fixed height `3.375rem`; sidebar ~`11.5rem`; content max `60rem` (home portal uncapped)
- Breakpoints: 480 / 720 / 900
- Spacing: tight within sections, clearer gaps between `.mp-section` / wiki panels
- Touch min ~`2.75rem` for primary controls

## Elevation & Depth

- Subtle `0 1px 3px` and elevated `0 4px 16px` + 1px outline
- Wallpaper + blur scrim is structural (readability), not decorative glass for its own sake
- Lift on hover for interactive panels/buttons via `--shadow-lift`

## Shapes

- Small Vector radii (`3–10px`); admin uses slightly softer `12px`
- Panel borders from `--panel-border` / glass edge tokens
- Minecraft texture buttons keep inset edges and image icons

## Components

- **Wiki header / search / sidebar**: shared chrome in `wiki/base.html`
- **Portal sections / project cards / subnav**: `.mp-*` in `mp-portal.css`
- **Tags, tables, collapsibles**: wiki tokens
- **Quiz**: `.nq-*` flow controls, progress, result hierarchy
- **Admin**: `.na-*` panels, tables, danger actions

## Do's and Don'ts

**Do**
- Keep progressive/visited semantics stable across themes
- Polish empty, loading, error, and focus states on every interactive path
- Bump CSS `?v=` when shipping visual changes

**Don't**
- Replace the Vector world with a generic SaaS landing look
- Nest cards or invent metric-hero strips on the home portal
- Change quiz scoring, admin auth path, or factual site copy without approval
