# 博客文章

个人博客 Markdown 源稿。每篇文章一个子目录：`index.md` + `images/`。

| 文章 | 状态 | 说明 |
|------|------|------|
| [认识简谱](./认识简谱/index.md) | 已发布 | 音乐入门 |
| [Framework 系列](./framework-guides/README.md) | 已发布 | 124 篇技术栈博文 · [/blog/series/framework](/blog/series/framework) |
| [Algorithm 系列](./algorithm-guides/README.md) | 连载中 | 82 篇专题双语指南 · [/blog/series/algorithm](/blog/series/algorithm) |
| [认识简谱/配图清单](./认识简谱/配图清单.md) | — | 配图文件名 |

**目录约定**

```
Blog/
└── <文章名>/
    ├── index.md      # 正文
    ├── images/       # 文内配图
    ├── 配图清单.md   # 可选
    └── _meta/        # 生成过程、提示词等（非正文）
```

发布到站点时，可将 `images/` 镜像到 `static/blog/<slug>/`（见根目录 README）。
