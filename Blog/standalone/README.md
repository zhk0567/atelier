# Standalone 博文 manifest

课程笔记、专题等不在 Framework / Algorithm / Hotspot 系列内的博文，在此注册。

## 文件

- [manifest.json](./manifest.json) — `series_meta` + `posts`

## 字段

| 字段 | 说明 |
|------|------|
| `series` | `course-notes`、`topics` 等，对应 `/blog/series/{id}` |
| `features` | 可选 `toc`、`pyecharts` |
| `toc_depth` | `2` 仅 h2；`3` 含 h3 |
| `chapter` | 课程笔记排序 |
| `status` | `published` / `draft` |

## 维护

```powershell
python scripts\init_dataviz_chapter_scaffold.py   # 数据可视化章节脚手架
python scripts\build_blog_search_index.py       # 更新博客搜索索引
python scripts\site\audit_content.py            # 内容审计
```
