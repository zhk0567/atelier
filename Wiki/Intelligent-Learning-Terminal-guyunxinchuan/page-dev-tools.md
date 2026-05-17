<!-- wiki_page_id: page-dev-tools -->

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [tools\sync_stories_data.py](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/tools\sync_stories_data.py)
- [tools\sync_story_covers.py](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/tools\sync_story_covers.py)
- [tools\sync_shop_carousel.py](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/tools\sync_shop_carousel.py)
- [tools\sync_wenchuang_shop.py](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/tools\sync_wenchuang_shop.py)
- [tools\sync_basic_lesson_covers.py](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/tools\sync_basic_lesson_covers.py)
- [tools\sync_basic_lesson_videos.py](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/tools\sync_basic_lesson_videos.py)
</details>

# 开发工具与数据同步脚本

## 概述

本文档介绍了Intelligent-Learning-Terminal项目中用于数据同步和资源管理的一系列开发工具脚本。这些脚本位于`tools`目录下，用于同步故事数据、故事封面、商城轮播图、文创商品、基础课程封面和基础课程视频等资源。

## 脚本列表

| 脚本名称 | 功能描述 |
|----------|----------|
| sync_stories_data.py | 同步故事数据 |
| sync_story_covers.py | 同步故事封面 |
| sync_shop_carousel.py | 同步商城轮播图 |
| sync_wenchuang_shop.py | 同步文创商品 |
| sync_basic_lesson_covers.py | 同步基础课程封面 |
| sync_basic_lesson_videos.py | 同步基础课程视频 |

## 脚本功能详解

### sync_stories_data.py

该脚本负责从远程服务器同步故事数据到本地。主要功能包括：
- 通过API获取故事列表和详细信息
- 将故事数据保存为JSON格式到本地文件
- �增量更新机制，只同步有变化的数据

### sync_story_covers.py

用于同步故事封面图片资源：
- 根据故事ID下载对应的封面图片
- 支持多种图片格式（JPG、PNG等）
- 自动创建存储目录结构
- 跳过已存在且未修改的文件

### sync_shop_carousel.py

负责同步商城轮播图数据：
- 获取轮播图配置信息（图片URL、跳转链接、显示顺序）
- 下载轮播图图片资源
- 生成本地配置文件供前端使用

### sync_wenchuang_shop.py

用于同步文创商品数据：
- 同步文创商品的基本信息（名称、价格、描述等）
- 下载商品图片资源
- 更新商品库存状态

### sync_basic_lesson_covers.py

同步基础课程封面图片：
- 根据课程ID获取封面图片
- 支持不同分辨率的封面适配
- 优化图片加载性能

### sync_basic_lesson_videos.py

负责同步基础课程视频资源：
- 下载课程视频文件
- 支持断点续传
- 视频格式转换和压缩（如有需要）
- 生成视频封面预览图

## 使用方法

所有脚本均可通过命令行直接执行：

```bash
python tools\sync_stories_data.py
python tools\sync_story_covers.py
# 依此类推...
```

## 注意事项

1. 执行前请确保网络连接正常
2. 建议在开发或测试环境中先运行脚本验证
3. 生产环境使用时注意同步频率，避免对服务器造成过大压力
4. 脚本执行过程中会在控制台输出进度信息
5. 异常情况下会记录错误日志便于排查问题

## 依赖要求

这些脚本可能依赖以下Python库：
- requests（用于HTTP请求）
- tqdm（用于进度条显示）
- PIL/Pillow（用于图片处理，如有需要）
- 其他项目特定依赖请查看各脚本文件头部的import语句

## 贡献指南

如需修改或添加新的同步脚本：
1. 遵循现有脚本的命名规范和代码风格
2. 添加适当的错误处理和日志记录
3. 确保脚本具有良好的可读性和维护性
4. 在提交前进行充分测试</details>