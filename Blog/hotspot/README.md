# Hotspot 热点栏目

追踪 AI、神经科技与人机交互等领域的前沿观察与思辨。

## 供稿规范

| 项 | 建议 |
|----|------|
| 篇幅 | 1500–4000 字，单篇成文 |
| 字段 | `slug`、`title`、`summary`、`category`、`tags`、`published_at`（可选） |
| 状态 | `draft` 连载稿不在站点列表展示；`published` 后出现在 `/blog/series/hotspot` |
| 体裁 | 技术热点解读、读书/论文笔记、行业观察，非万字教程 |

## 发布流程

1. 在 `Blog/hotspot/{slug}/index.md` 撰写正文（可含 frontmatter）。
2. 在 [manifest.json](./manifest.json) 的 `posts` 中追加条目并设 `status: published`。
3. 重启 FastAPI（manifest 有内存缓存）或等待缓存失效。
4. 可选：运行 `python scripts/build_blog_search_index.py` 更新搜索索引。

## 站点入口

- 系列页：`/blog/series/hotspot`
- 博客首页「热点」区块
