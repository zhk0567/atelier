"""Generate full index.md for Chapter 9 blog (run once when updating content)."""

from __future__ import annotations

import re
from pathlib import Path

from code_highlight import highlighted_block, highlighted_snippet

ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = ROOT / "code"
OUT = ROOT / "index.md"

_RENDER_RE = re.compile(
    r'\.render\(str\(HTML_DIR\s*/\s*["\']([^"\']+)["\']\)\)'
)

FRONT = """---
title: 数据可视化技术 · 第九章 pyecharts
category: 课程笔记
tags: [pyecharts, 数据可视化, ECharts]
status: ready
---

# 第九章：可视化后起之秀——pyecharts

> 对应教材《Python 数据可视化（第 2 版）》第 9 章（约 p.211–238）。本文**按课本顺序**收录全书要点；文中出现的**每一个新方法**均附参数说明（与教材表述一致）。  
> 展示版源码：[`code/`](code/) · 生成资源：`python code/run_all.py`  
> **交互说明**：下文图表在**本页内嵌**（滚动进入视口后加载；同时最多 **2** 个 ECharts 实例；离开视口或切换标签页会卸载以节省性能）。亦可「新窗口打开」全屏操作。  
> **程序**：每幅图后附**核心 Python 代码**（与 `code/` 一致）；代码块用**色条 + 左边线**区分数据、建图链式、配置项、组合布局、渲染输出。

---

"""

CHART_HEIGHT: dict[str, str] = {
    "fig_9_02_bar.html": "340",
    "fig_9_03_line.html": "360",
    "fig_9_04_pie.html": "400",
    "fig_9_05_donut.html": "400",
    "fig_9_06_scatter.html": "380",
    "fig_9_07_effect_scatter.html": "380",
    "fig_9_08_bar3d.html": "540",
    "fig_9_09_sankey.html": "420",
    "fig_9_10_grid.html": "580",
    "fig_9_11_page.html": "720",
    "fig_9_13_tab.html": "400",
    "fig_9_15_timeline.html": "440",
    "fig_9_16_theme_roma.html": "340",
    "fig_9_17_django_embed.html": "360",
    "hupu_section_bar.html": "400",
    "hupu_hourly_line.html": "380",
}


PNG_PREVIEW = {
    "fig_9_02_bar",
    "fig_9_03_line",
    "fig_9_04_pie",
    "fig_9_05_donut",
    "fig_9_06_scatter",
    "fig_9_16_theme_roma",
    "hupu_section_bar",
    "hupu_hourly_line",
}


def chart_embed(name: str, cap: str, html: str) -> str:
    """In-page lazy iframe + optional PNG placeholder (see blog-pyecharts-embed.js)."""
    h = CHART_HEIGHT.get(html, "360")
    src = f"/static/blog/dataviz-ch09/{html}"
    if name in PNG_PREVIEW:
        preview = (
            f'<img src="/static/blog/dataviz-ch09/{name}.png" '
            f'alt="{cap}（静态预览）" width="600" height="300" '
            f'loading="lazy" decoding="async" />'
        )
    else:
        preview = '<div class="pyecharts-embed__skeleton" aria-hidden="true"></div>'
    return f"""<figure class="pyecharts-figure">
<div class="pyecharts-embed" data-src="{src}" data-height="{h}" role="region" aria-label="{cap}">
<div class="pyecharts-embed__placeholder">
{preview}
<span class="pyecharts-embed__hint">进入视口后加载交互图表（同时最多 2 个动画实例）</span>
</div>
</div>
<figcaption class="pyecharts-figure__caption">{cap} · <a href="{src}" target="_blank" rel="noopener noreferrer">新窗口打开</a></figcaption>
</figure>

"""


def img(name: str, cap: str, html: str | None = None) -> str:
    if html:
        return chart_embed(name, cap, html)
    return f"![{cap}](images/{name}.png)\n*{cap}*\n\n"


def embed_link(html: str, cap: str, name: str | None = None) -> str:
    stem = name or html.replace(".html", "")
    return chart_embed(stem, cap, html)


def param_table(rows: list[tuple[str, str, str]]) -> str:
    out = ["| 参数 | 类型/取值 | 说明 |", "|------|-----------|------|"]
    for a, b, c in rows:
        out.append(f"| `{a}` | {b} | {c} |")
    return "\n".join(out) + "\n"


def extract_core(module: str) -> str:
    """Pull chart logic from code/*.py (omit paths boilerplate)."""
    path = CODE_DIR / f"{module}.py"
    if not path.is_file():
        return f"# 未找到 code/{module}.py"
    raw = path.read_text(encoding="utf-8")
    if raw.lstrip().startswith('"""'):
        end = raw.find('"""', 3)
        if end != -1:
            raw = raw[end + 3 :].lstrip("\n")
    lines_out: list[str] = []
    skip_html = False
    for line in raw.splitlines():
        if skip_html:
            if '"""' in line:
                skip_html = False
                lines_out.append("    # Django 视图: return HttpResponse(embed)")
            continue
        stripped = line.strip()
        if stripped.startswith("if __name__"):
            break
        if "from _paths import" in line:
            continue
        if "ensure_dirs()" in line:
            continue
        if 'html = f"""' in line or "html = '''" in line:
            skip_html = True
            if "render_embed" not in "\n".join(lines_out):
                lines_out.append("    embed = bar.render_embed()")
            continue
        if "out.write_text" in line or line.strip().startswith("out = HTML_DIR"):
            continue
        if "preview_path" in line or "gif_path" in line:
            continue
        if "fig.savefig(preview_path" in line:
            continue
        if "anim.save(" in line:
            lines_out.append("    anim.save(\"ex05_sine_animation.gif\", writer=...)  # 100 帧")
            continue
        if "print(" in line and "gif skip" in line:
            continue
        if "plt.close" in line:
            continue
        if _RENDER_RE.search(line):
            lines_out.append(_RENDER_RE.sub(r'.render("\1")', line))
            continue
        lines_out.append(line)
    text = "\n".join(lines_out).strip("\n")
    return text


def prog(module: str, note: str = "") -> str:
    body = extract_core(module)
    extra = f" {note}" if note else ""
    return (
        f"\n**核心程序（`{module}.py`）**{extra}：\n\n"
        f"{highlighted_block(body)}\n"
        f"完整源码：[`code/{module}.py`](code/{module}.py)\n\n"
    )


BODY = FRONT + """
## 9.1 pyecharts 概述

### 9.1.1 认识 pyecharts

Matplotlib、Seaborn 常用，但前者交互弱、后者偏统计图。**pyecharts** 封装 ECharts，便于在 Python 中绘制可交互、可定制的图表。

**教材归纳的七个特点：**

1. **API 简洁**，支持链式调用。  
2. **图表类型多**（30+）。  
3. **支持 Jupyter** / JupyterLab。  
4. **可整合 Flask、Django** 等 Web 框架。  
5. **配置灵活**，易做出美观图表。  
6. **文档与示例丰富**。  
7. **地图支持**（400+ 地图文件、百度地图扩展等）。

**版本与安装（教材 2.0.4，Python 3.6–3.11）：**

```bash
pip install pyecharts==2.0.4
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyecharts==2.0.4
```

验证：`from pyecharts.charts import Bar` 无报错即安装成功。

---

### 9.1.2 认识 ECharts

ECharts 为百度开源、基于 **ZRender** 的 JavaScript 可视化库；支持 Canvas / SVG / VML，兼容主流浏览器与移动端。常见图：折线、柱形、散点、饼图、地图、热力、树图、旭日图、漏斗、仪表盘等；支持多图组合与丰富组件。

#### 图 9-1：ECharts 六大组件

> 教材 p.212 为**可交互气泡图**（含主/副标题、图例、工具箱、悬停提示框、视觉映射条、底部区域缩放）。请在纸质课本或扫描页对照；本站以下用各节 `render()` 的 HTML 复现交互效果。

""" + img("fig_9_02_bar", "图 9-2 柱形图（本章首图示例）", "fig_9_02_bar.html") + """

| 序号 | 组件 | 作用 |
|------|------|------|
| ① | **标题组件** | 主标题、副标题；默认左上角 |
| ② | **图例组件** | 系列名称；默认顶部；可点击显隐系列 |
| ③ | **工具箱组件** | 保存图片、缩放、还原、数据视图、切换图类型等 |
| ④ | **提示框组件** | 悬停显示数据详情 |
| ⑤ | **区域缩放组件** | 滑块/选区缩放查看局部数据 |
| ⑥ | **视觉映射组件** | 用颜色/大小映射数值区间，可筛选 |

---

### 9.1.3 pyecharts 数据集 Faker

`pyecharts.faker.Faker` 提供测试数据，便于无真实数据时练手。

**表 9-1 Faker 常用属性**

| 属性 | 测试数据 |
|------|----------|
| `clothes` | 衬衫、毛衣、领带、裤子、风衣、高跟鞋、袜子 |
| `fruits` | 草莓、芒果、葡萄、雪梨、西瓜、柠檬、车厘子 |
| `animal` | 河马、蟒蛇、老虎、大象、兔子、熊猫、狮子 |
| `dogs` | 哈士奇、萨摩耶、泰迪、金毛、牧羊犬、吉娃娃、柯基 |
| `week` | 周一至周日 |
| `provinces` | 广东省、北京市、上海市等 |
| `guangdong_city` | 汕头市、广州市等 |

**方法：**

| 方法 | 说明 |
|------|------|
| `Faker.choose()` | 从表 9-1 中**随机取一类**完整列表 |
| `Faker.values()` | 生成 **7 个** 随机整数，范围 **20–150** |

""" + highlighted_snippet(
    """from pyecharts.faker import Faker
print(Faker.fruits)
print(Faker.choose())
print(Faker.values())""",
    legend=True,
) + """

---

## 9.2 pyecharts 初体验

### 9.2.1 绘制第一个图表（四步法）

1. 导入模块/类  
2. 创建图表类对象  
3. 添加数据并设置配置项  
4. 渲染图表  

#### 方法：`Bar(init_opts=...)`

**`InitOpts` 常用参数（初始化配置，表 9-3 之「初始化配置项」）：**

""" + param_table([
    ("width", "str，如 `\"600px\"`", "画布宽度"),
    ("height", "str，如 `\"300px\"`", "画布高度"),
    ("theme", "`ThemeType` 枚举", "图表主题，默认 WHITE"),
    ("bg_color", "str", "背景色"),
    ("animation_opts", "`AnimationOpts`", "初始动画"),
    ("renderer", "str", "渲染器，如 canvas / svg"),
]) + """

#### 方法：`add_xaxis(xaxis_data, ...)`

| 参数 | 说明 |
|------|------|
| `xaxis_data` | X 轴类目或数值序列 |
| `is_scale` | 是否为数值轴自动缩放（折线/散点等常用） |
| `boundary_gap` | 类目轴留白，柱形图常为 True |

#### 方法：`add_yaxis(series_name, y_axis, *, ...)`

**柱形图 `Bar.add_yaxis` 教材强调：**

""" + param_table([
    ("series_name", "str", "系列名，出现在图例与提示框"),
    ("y_axis", "list", "Y 轴数据"),
    ("stack", "str", "堆叠组名，同组柱形堆叠"),
    ("category_gap", "str/int", "类目间柱间距"),
    ("gap", "str", "柱间间距"),
    ("label_opts", "`LabelOpts`", "柱顶/柱内标签"),
]) + """

#### 方法：`set_global_opts(...)`

**`set_global_opts` 教材列出的主要形参（表 9-3）：**

""" + param_table([
    ("title_opts", "`TitleOpts`", "标题组件"),
    ("legend_opts", "`LegendOpts`", "图例"),
    ("tooltip_opts", "`TooltipOpts`", "提示框"),
    ("toolbox_opts", "`ToolboxOpts`", "工具箱"),
    ("xaxis_opts", "`AxisOpts`", "X 轴"),
    ("yaxis_opts", "`AxisOpts`", "Y 轴"),
    ("visualmap_opts", "`VisualMapOpts`", "视觉映射"),
    ("datazoom_opts", "`DataZoomOpts` 或 list", "区域缩放"),
    ("axispointer_opts", "`AxisPointerOpts`", "坐标轴指示器"),
]) + """

**`TitleOpts` 常用参数：**

""" + param_table([
    ("title", "str", "主标题文字"),
    ("subtitle", "str", "副标题"),
    ("pos_left", "str/num", "距容器左侧，如 `\"center\"`、百分比"),
    ("pos_top", "str/num", "距容器顶部"),
    ("title_textstyle_opts", "`TextStyleOpts`", "主标题字体样式"),
]) + """

**`AxisOpts` 常用参数（轴名称教材示例）：**

""" + param_table([
    ("name", "str", "轴名称，如「销售额(万元)」"),
    ("name_location", "str", "`start` / `middle` / `center` / `end`"),
    ("name_gap", "int", "轴名称与轴线距离（像素）"),
    ("type_", "str", "`value` / `category` / `time` / `log`"),
    ("axislabel_opts", "`LabelOpts`", "刻度标签样式"),
    ("splitline_opts", "`SplitLineOpts`", "网格分割线"),
]) + """

#### 方法：`set_series_opts(...)`

**表 9-4 系列配置项类：**

| 配置项 | 类 | 说明 |
|--------|-----|------|
| 图元样式 | `ItemStyleOpts` | 颜色、边框、透明度 |
| 文本样式 | `TextStyleOpts` | 字体、大小、颜色 |
| 标签 | `LabelOpts` | 数据标签位置、格式 |
| 线样式 | `LineStyleOpts` | 线型、颜色、宽度 |
| 分割线 | `SplitLineOpts` | 网格线 |
| 标记点/线/域 | `MarkPointOpts` 等 | 标注极值等 |
| 涟漪特效 | `EffectOpts` | 特效散点用 |

**`LabelOpts` 常用参数：**

""" + param_table([
    ("is_show", "bool", "是否显示标签"),
    ("position", "str", "如 `top` / `bottom` / `inside`"),
    ("formatter", "str/callable", "标签格式，如 `{c}`"),
    ("color", "str", "文字颜色"),
    ("font_size", "int", "字号"),
]) + """

教材示例：`bar.set_series_opts(label_opts=opts.LabelOpts(position="top"))`。亦可用字典：`{"position": "top"}`。

#### 图 9-2 柱形图

""" + img("fig_9_02_bar", "图 9-2 柱形图示例", "fig_9_02_bar.html") + """
""" + prog("fig_9_02_bar", "— 四步法链式写法") + """

---

### 9.2.2 认识图表类（表 9-2）

| 类 | 说明 |
|----|------|
| `Line` | 折线图 |
| `Bar` | 柱形/条形图 |
| `Pie` | 饼图 |
| `Scatter` | 散点图 |
| `EffectScatter` | 涟漪特效散点 |
| `Boxplot` | 箱形图 |
| `Radar` | 雷达图 |
| `Bar3D` | 三维柱形图 |
| `Funnel` | 漏斗图 |
| `Sankey` | 桑基图 |

各类均继承 `Base`；构造方法名与类名相同。`Boxplot`、`Radar`、`Funnel` 等在本章其余小节未逐一出图，但**构造方式相同**：`Xxx(init_opts=...)` → `add_*` → `set_global_opts` → `render`。

---

### 9.2.3 认识配置项（全局 / 系列，补全表 9-3、9-4 各类参数）

配置项模块为 `pyecharts.options`（常写 `import pyecharts.options as opts`）。  
**全局**用 `chart.set_global_opts(...)`；**系列**用 `chart.set_series_opts(...)` 或写在 `add_yaxis` / `add` 的参数里。

#### `AnimationOpts`（表 9-3 · Echarts 动画）

""" + param_table([
    ("animation", "bool", "是否开启动画"),
    ("animation_threshold", "int", "动画阈值"),
    ("animation_duration", "int", "初始动画时长（ms）"),
    ("animation_easing", "str", "缓动效果，如 `cubicOut`"),
    ("animation_delay", "int", "初始动画延迟（ms）"),
    ("animation_duration_update", "int", "数据更新动画时长"),
    ("animation_easing_update", "str", "数据更新缓动"),
    ("animation_delay_update", "int", "数据更新延迟"),
]) + """

#### `ToolboxOpts`（工具箱）

""" + param_table([
    ("is_show", "bool", "是否显示工具箱"),
    ("orient", "str", "布局朝向 horizontal / vertical"),
    ("pos_left", "str/%", "工具箱水平位置"),
    ("pos_top", "str/%", "工具箱垂直位置"),
    ("feature", "dict", "各功能开关：saveAsImage、dataZoom、restore、dataView、magicType 等"),
]) + """

#### `LegendOpts`（图例）

""" + param_table([
    ("is_show", "bool", "是否显示图例"),
    ("type_", "str", "图例类型 plain / scroll"),
    ("pos_left", "str/%", "图例框左侧位置"),
    ("pos_top", "str/%", "图例框顶部位置"),
    ("orient", "str", "horizontal / vertical"),
    ("selected_mode", "bool/str", "图例选择模式"),
    ("selected_map", "dict", "系列默认选中状态"),
]) + """

#### `TooltipOpts`（提示框）

""" + param_table([
    ("is_show", "bool", "是否显示"),
    ("trigger", "str", "`item` 单点 / `axis` 坐标轴 / `none`"),
    ("trigger_on", "str", "`mousemove` / `click` 等"),
    ("formatter", "str/callable", "提示内容模板"),
    ("axis_pointer_type", "str", "指示线类型 line / shadow / cross"),
]) + """

#### `DataZoomOpts`（区域缩放）

""" + param_table([
    ("is_show", "bool", "是否显示"),
    ("type_", "str", "`slider` 滑块 / `inside` 内置"),
    ("range_start", "0–100", "窗口起始百分比"),
    ("range_end", "0–100", "窗口结束百分比"),
    ("orient", "str", "horizontal / vertical"),
]) + """

#### `VisualMapOpts`（视觉映射）

""" + param_table([
    ("is_show", "bool", "是否显示"),
    ("type_", "str", "continuous 连续 / piecewise 分段"),
    ("min_", "number", "映射下限"),
    ("max_", "number", "映射上限"),
    ("orient", "str", "horizontal / vertical"),
    ("pos_left", "str/%", "组件位置"),
    ("range_color", "list", "颜色渐变列表"),
]) + """

#### `ItemStyleOpts` / `LineStyleOpts` / `TextStyleOpts` / `SplitLineOpts`

**`ItemStyleOpts`：** `color`、`border_color`、`border_width`、`opacity`、`border_type`。  
**`LineStyleOpts`：** `color`、`width`、`type_`（solid/dashed/dotted）、`opacity`、`curve`（桑基边弯曲度）。  
**`TextStyleOpts`：** `color`、`font_size`、`font_style`、`font_weight`、`font_family`。  
**`SplitLineOpts`：** `is_show`、`linestyle_opts`（分割线线型）。

#### `EffectOpts`（涟漪特效散点）

""" + param_table([
    ("effect_type", "str", "特效类型，如 `ripple`"),
    ("scale", "float", "波纹缩放比例"),
    ("period", "int", "动画周期"),
    ("brush_type", "str", "stroke / fill"),
]) + """

#### `MarkPointOpts` / `MarkLineOpts` / `MarkAreaOpts`

用于标注最大值、最小值、平均线或区间：`data=[opts.MarkPointItem(type_=\"max\")]` 等，具体数据项见官方文档；教材表 9-4 仅列类名，用法与 `LabelOpts` 类似传入 `set_series_opts`。

---

### 9.2.4 渲染图表

| 方法 | 说明 | 主要参数 |
|------|------|----------|
| `render(path='render.html', template_name='simple_chart.html', env=None, **kwargs)` | 输出 HTML 文件 | 见下表 |
| `render_notebook()` | Jupyter 内嵌显示 | 无参数；需在 Notebook 环境 |
| `render_embed()` | 返回可嵌入片段 | 无参数；返回 `str`，供 Django/Flask 模板 |

**`render()` 参数说明（教材 9.2.4）：**

""" + param_table([
    ("path", "str", "输出文件路径，默认 `render.html`"),
    ("template_name", "str", "Jinja2 模板名，默认 `simple_chart.html`"),
    ("env", "Environment", "自定义 Jinja2 环境；Django 整合时配合 `CurrentConfig`"),
    ("**kwargs", "dict", "传给模板的额外变量"),
]) + """

**调用示例：**

""" + highlighted_snippet(
    """chart = Bar().add_xaxis(...).add_yaxis(...)
chart.render("my_chart.html")           # 独立 HTML 页
# chart.render_notebook()               # Jupyter 内嵌
# fragment = chart.render_embed()       # Web 模板片段""",
    legend=True,
) + """

---

## 9.3 绘制常用图表

### 9.3.1 折线图 `Line`

#### `Line.add_xaxis(xaxis_data, *, is_scale=False, is_inverse=False, ...)`

""" + param_table([
    ("xaxis_data", "list", "X 轴数据（类目或数值）"),
    ("is_scale", "bool", "是否脱离 0 值比例缩放"),
    ("is_inverse", "bool", "是否反向坐标轴"),
    ("boundary_gap", "bool", "类目轴两端留白"),
    ("min_", "number", "最小值"),
    ("max_", "number", "最大值"),
    ("split_number", "int", "分割段数"),
    ("axislabel_opts", "`LabelOpts`", "刻度标签"),
]) + """

#### `Line.add_yaxis(series_name, y_axis, *, ...)`

教材列出的关键参数：

""" + param_table([
    ("series_name", "str", "系列名"),
    ("y_axis", "list", "数据"),
    ("is_connect_nones", "bool", "是否连接空值"),
    ("color", "str", "标注文字颜色"),
    ("is_symbol_show", "bool", "是否显示标记，默认 True"),
    ("symbol", "str", "`circle`/`rect`/`triangle`/`diamond`/`pin`/`arrow`/`none`"),
    ("symbol_size", "int 或 [w,h]", "标记大小"),
    ("is_smooth", "bool", "是否平滑曲线"),
    ("label_opts", "`LabelOpts`", "点标签"),
    ("linestyle_opts", "`LineStyleOpts`", "线样式"),
]) + """

#### 图 9-3

""" + img("fig_9_03_line", "图 9-3 折线图示例", "fig_9_03_line.html") + """

教材数据：商家 A `[102,132,105,52,90,111,95]`，商家 B `[86,108,128,66,136,122,105]`，`symbol` 分别为 diamond / triangle。
""" + prog("fig_9_03_line") + """

---

### 9.3.2 饼图 / 圆环图 `Pie`

#### `Pie.add(series_name, data_pair, *, ...)`

""" + param_table([
    ("series_name", "str", "系列名"),
    ("data_pair", "list[tuple]", "`[(名称, 值), ...]`"),
    ("color", "str", "系列色"),
    ("color_by", "str", "按 `data` / `series` 取色"),
    ("is_legend_hover_link", "bool", "图例悬停是否联动高亮"),
    ("selected_mode", "bool/str", "选中模式"),
    ("selected_offset", "int", "选中扇区外移距离，默认 10"),
    ("radius", "None / str / [内,外]", "半径；内外半径均>0 为圆环"),
    ("center", "list", "圆心 `[x,y]`，像素或百分比"),
    ("rosetype", "str", "南丁格尔玫瑰图 `radius`/`area`"),
    ("is_clockwise", "bool", "是否顺时针"),
    ("start_angle", "number", "起始角度，默认 90"),
    ("label_opts", "`LabelOpts`", "扇区标签"),
]) + """

#### 图 9-4、9-5

""" + img("fig_9_04_pie", "图 9-4 饼图", "fig_9_04_pie.html") + """
教材数据：小米 150、华为 200、荣耀 100、魅族 60、vivo 145、OPPO 160。
""" + prog("fig_9_04_pie") + """

""" + img("fig_9_05_donut", "图 9-5 圆环图", "fig_9_05_donut.html") + """
`radius=[\"90px\", \"160px\"]` 得到圆环。
""" + prog("fig_9_05_donut") + """

---

### 9.3.3 散点图 `Scatter` / 涟漪 `EffectScatter`

**`Scatter.add_xaxis(xaxis_data, ...)`** 与折线相同，教材用 `np.arange(1, 21).tolist()`。

**`Scatter.add_yaxis(series_name, y_axis, *, ...)`**：与折线类似，无 `is_smooth`；教材示例 X 为 `1–20`，Y 为 `randint(10,40,20)`。全局常同时设置：

""" + highlighted_snippet(
    """.set_global_opts(
    title_opts=opts.TitleOpts(title="散点图示例"),
    xaxis_opts=opts.AxisOpts(name="x 轴", name_location="center", name_gap=30),
    yaxis_opts=opts.AxisOpts(name="y 轴", name_location="center", name_gap=30),
)""",
) + """

**`EffectScatter.add_yaxis`** 额外参数：

""" + param_table([
    ("effect_opts", "`EffectOpts`", "涟漪动画样式"),
    ("symbol", "str", "如 `pin`"),
    ("symbol_size", "int", "标记大小"),
]) + """

""" + img("fig_9_06_scatter", "图 9-6 散点图", "fig_9_06_scatter.html") + """
""" + prog("fig_9_06_scatter") + """

""" + embed_link("fig_9_07_effect_scatter.html", "图 9-7 涟漪特效散点") + """
""" + prog("fig_9_07_effect_scatter") + """

---

### 9.3.4 三维柱形图 `Bar3D`

#### `Bar3D.add(series_name, data, *, ...)`

""" + param_table([
    ("series_name", "str", "系列名"),
    ("data", "list", "每项 `[x索引, y索引, z值]`；教材将原 `[i,j,v]` 转为 `[j,i,v]`"),
    ("shading", "str", "`color` / `lambert` / `realistic` 光照"),
    ("xaxis3d_opts", "`Axis3DOpts`", "3D 的 X 轴"),
    ("yaxis3d_opts", "`Axis3DOpts`", "3D 的 Y 轴"),
    ("zaxis3d_opts", "`Axis3DOpts`", "3D 的 Z 轴"),
    ("grid3d_opts", "`Grid3DOpts`", "3D 网格"),
    ("label_opts", "`LabelOpts`", "柱顶标签"),
]) + """

""" + embed_link("fig_9_08_bar3d.html", "图 9-8 三维柱形图") + """
`VisualMapOpts(max_=30)` 控制映射上限。
""" + prog("fig_9_08_bar3d") + """

---

### 9.3.5 桑基图 `Sankey`

#### `Sankey.add(series_name, nodes, links, *, ...)`

""" + param_table([
    ("series_name", "str", "系列名"),
    ("nodes", "list[dict]", "节点列表，每项 `{\"name\": \"...\"}`"),
    ("links", "list[dict]", "`source` / `target` / `value` 流量"),
    ("linestyle_opt", "`LineStyleOpts`", "边样式；教材 `opacity=0.2, curve=0.5, color=\"source\"`"),
    ("label_opts", "`LabelOpts`", "节点标签；教材 `position=\"right\"`"),
]) + """

""" + embed_link("fig_9_09_sankey.html", "图 9-9 桑基图") + """
""" + prog("fig_9_09_sankey") + """

---

## 9.4 绘制组合图表

组合类型：**并行多图 Grid**、**顺序多图 Page**、**选项卡 Tab**、**时间线 Timeline**。

### 9.4.1 `Grid.add(chart, grid_opts, *, grid_index=0, is_control_axis_index=False)`

""" + param_table([
    ("chart", "Chart 子类实例", "要放入的图表"),
    ("grid_opts", "`GridOpts`", "该图在画布中的位置与大小"),
    ("grid_index", "int", "直角坐标系索引，默认 0"),
    ("is_control_axis_index", "bool", "是否手动控制轴索引"),
]) + """

**`GridOpts` 常用参数：**

""" + param_table([
    ("pos_left", "str/%", "左边距"),
    ("pos_right", "str/%", "右边距"),
    ("pos_top", "str/%", "上边距"),
    ("pos_bottom", "str/%", "下边距"),
    ("width", "str/%", "宽度"),
    ("height", "str/%", "高度"),
]) + """

教材示例：`pos_bottom=\"60%\"` 放下方图，`pos_top=\"60%\"` 放上方图。

""" + embed_link("fig_9_10_grid.html", "图 9-10 Grid 组合图") + """
""" + prog("fig_9_10_grid") + """

---

### 9.4.2 `Page(page_title, js_host, interval, layout, ...)`

**构造参数：**

""" + param_table([
    ("page_title", "str", "HTML 页标题，默认 Awesome-pyecharts"),
    ("js_host", "str", "JS 资源主机，空为默认"),
    ("interval", "int", "图表间距（像素），默认 1"),
    ("layout", "`PageLayoutOpts`", "页面布局"),
]) + """

**`Page.add(*charts)`**：按顺序传入多个图表对象。

""" + embed_link("fig_9_11_page.html", "图 9-11/12 Page 顺序多图") + """
""" + prog("fig_9_11_page") + """

---

### 9.4.3 `Tab` 选项卡多图

**`Tab()` 构造**：创建空选项卡容器。

**`Tab.add(chart, tab_name)`**

| 参数 | 说明 |
|------|------|
| `chart` | 图表对象（Bar、Line 等） |
| `tab_name` | 选项卡上显示的名称，如 `\"柱形图\"` |

渲染：`tab.render_notebook()` 或 `tab.render("tab.html")`。

""" + embed_link("fig_9_13_tab.html", "图 9-13/14 Tab 选项卡") + """
""" + prog("fig_9_13_tab") + """

---

### 9.4.4 `Timeline` 时间线轮播

#### `Timeline.add(chart, time_point)`

| 参数 | 说明 |
|------|------|
| `chart` | 某一时刻的图表 |
| `time_point` | 时间轴上显示的文字，如 `\"2023年\"` |

#### `Timeline.add_schema(...)`

""" + param_table([
    ("orient", "str", "`horizontal` / `vertical`"),
    ("symbol", "str", "时间点形状，默认 circle"),
    ("symbol_size", "int", "点大小"),
    ("play_interval", "int", "自动播放间隔（ms）"),
    ("is_auto_play", "bool", "是否自动播放"),
    ("is_loop_play", "bool", "是否循环"),
    ("is_rewind_play", "bool", "是否反向播放"),
    ("is_timeline_show", "bool", "是否显示时间轴"),
    ("pos_bottom", "str", "时间轴位置"),
]) + """

""" + embed_link("fig_9_15_timeline.html", "图 9-15 Timeline 时间线") + """
""" + prog("fig_9_15_timeline") + """

---

## 9.5 定制图表主题（表 9-5）

默认 `ThemeType.WHITE`。在 `InitOpts(theme=ThemeType.xxx)` 中设置。

| 主题 | 说明 |
|------|------|
| LIGHT | 浅色 |
| DARK | 深色 |
| WHITE | 默认白底 |
| CHALK | 粉笔质感 |
| ESSOS | 暖色 |
| INFOGRAPHIC | 信息图风格 |
| MACARONS | 马卡龙色 |
| PURPLE_PASSION | 紫色 |
| ROMA | 古典中性色 |
| ROMANTIC | 浪漫柔和 |
| SHINE | 高饱和闪亮 |
| VINTAGE | 复古柔和 |

""" + img("fig_9_16_theme_roma", "图 9-16 ROMA 主题", "fig_9_16_theme_roma.html") + """
""" + prog("fig_9_16_theme_roma") + """

---

## 9.6 整合 Web 框架（Django）

教材步骤摘要：

1. `django-admin startproject pyecharts_django_demo`  
2. `python manage.py startapp demo`，并在 `INSTALLED_APPS` 注册 `demo`  
3. `demo/urls.py`：`url(r'^$', views.index)`  
4. 主 `urls.py`：`url(r'^demo/', include('demo.urls'))`  
5. 复制 `pyecharts.render.templates` 下 `macro`、`simple_chart.html` 到 `demo/templates`  
6. `views.py` 中设置 `CurrentConfig.GLOBAL_ENV`（Jinja2 `FileSystemLoader`），构造图表后 `return HttpResponse(c.render_embed())`  
7. `python manage.py runserver`，访问 `http://127.0.0.1:8000/demo/`

**`render_embed()`**：返回嵌入现有模板的 HTML/JS 片段，而非完整页面。

**`CurrentConfig.GLOBAL_ENV`（教材 views 片段）**：用 Jinja2 `FileSystemLoader` 指向 `demo/templates`，使 pyecharts 能找到 `macro` 与 `simple_chart.html`。

**视图核心（教材图 9-17）：**

""" + highlighted_snippet(
    """from django.http import HttpResponse
from pyecharts import options as opts
from pyecharts.charts import Bar

def index(request):
    c = (
        Bar()
        .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
        .add_yaxis("商家B", [15, 25, 16, 55, 48, 8])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="柱形图示例", subtitle="我是副标题"),
            yaxis_opts=opts.AxisOpts(name="销售额(万元)", name_location="center", name_gap=30),
        )
    )
    return HttpResponse(c.render_embed())""",
    legend=True,
) + """

""" + embed_link("fig_9_17_django_embed.html", "图 9-17 Django render_embed 示例") + """
""" + prog("fig_9_17_django_embed", "— 本地模拟 render_embed") + """

---

## 9.7 实战演练：虎扑社区分析

目标：① 各板块发帖数；② 全站与 NBA 板块 24 小时发帖量。下列为**示例数据**演示流程，可替换真实 CSV。

""" + img("hupu_section_bar", "各板块发帖柱形图", "hupu_section_bar.html") + """
""" + prog("hupu_section_bar") + """

""" + img("hupu_hourly_line", "24 小时发帖折线", "hupu_hourly_line.html") + """
""" + prog("hupu_hourly_line") + """

---

## 课后习题（全文作答）

### 第一大题

1. pyecharts 基于 ECharts，图表在浏览器端渲染。——**对**  
2. `render_notebook()` 可在任意 `.py` 脚本代替 `render()`。——**错**  
3. Grid 与 Page 都可多图，Grid 同一画布分区，Page 垂直分页。——**对**  
4. 主题只能通过修改 JS 文件实现。——**错**，`InitOpts(theme=...)`  
5. 桑基图 `value` 决定边宽。——**对**

### 第二大题

1. `pip install pyecharts==2.0.4`  
2. `Bar`  
3. `title_opts`  
4. `Grid`  
5. `Timeline`  
6. `render_embed()`

### 第四大题（编程实践 · 对应本章各图）

教材通常要求用 pyecharts **复现图 9-2～图 9-15 及 9-7 虎扑分析** 等。本站已提供与课本数据一致的完整脚本，可按图号对照修改：

| 要求 | 脚本 |
|------|------|
| 柱形图（四步法） | `fig_9_02_bar.py` |
| 折线图双系列 | `fig_9_03_line.py` |
| 饼图 / 圆环图 | `fig_9_04_pie.py`、`fig_9_05_donut.py` |
| 散点 / 涟漪散点 | `fig_9_06_scatter.py`、`fig_9_07_effect_scatter.py` |
| 3D 柱形 / 桑基 | `fig_9_08_bar3d.py`、`fig_9_09_sankey.py` |
| Grid / Page / Tab / Timeline | `fig_9_10_grid.py` … `fig_9_15_timeline.py` |
| 主题 ROMA | `fig_9_16_theme_roma.py` |
| Django 嵌入 | `fig_9_17_django_embed.py` |
| 虎扑实战 | `hupu_section_bar.py`、`hupu_hourly_line.py` |

一键生成 HTML/PNG：`python Blog\\数据可视化-第九章\\code\\run_all.py`。

### 第三大题（简答）

**1. pyecharts 相对 Matplotlib 的两点优势与一点局限**  
优势：① 默认生成交互图（缩放、提示、图例切换）适合 Web 与报告展示；② 组合图（Grid/Page/Tab/Timeline）与主题、地图等封装完善，上手快。局限：依赖浏览器渲染环境，批量导出印刷级矢量图或复杂非 Web 排版不如 Matplotlib 直接。

**2. `set_global_opts` 与 `set_series_opts` 的区别，各举一例**  
`set_global_opts` 作用于整图，如 `title_opts=opts.TitleOpts(title="柱形图示例")`、`yaxis_opts=opts.AxisOpts(name="销售额(万元)")`。`set_series_opts` 作用于某一数据系列，如 `label_opts=opts.LabelOpts(position="top")` 只给柱顶加标签。

**3. Faker 数据集的作用**  
提供服装、水果、省份等**现成类目与随机数值**，不必每次手写长列表即可调试图表 API 与配置项。

**4. Web 项目为何常用 `render_embed()`**  
Django/Flask 模板往往已有页头页脚布局；`render_embed()` 只返回图表所需的 div+脚本片段，可插入模板指定位置，而 `render()` 生成的是完整 HTML 页面。

### 第五大题（Matplotlib 动画）

要求：默认样式正弦曲线；左端红点；沿曲线运动；显示坐标；**100 帧**、间隔 **100ms**。

""" + img("ex05_sine_frame", "第五大题示意帧") + """
[GIF](/static/blog/dataviz-ch09/ex05_sine_animation.gif)

""" + prog("ex05_sine_animation", "— 100 帧、间隔 100ms") + """

---

## 程序清单

| 图号 | 脚本 |
|------|------|
| 9-2 | `fig_9_02_bar.py` |
| 9-3 | `fig_9_03_line.py` |
| 9-4 | `fig_9_04_pie.py` |
| 9-5 | `fig_9_05_donut.py` |
| 9-6 | `fig_9_06_scatter.py` |
| 9-7 | `fig_9_07_effect_scatter.py` |
| 9-8 | `fig_9_08_bar3d.py` |
| 9-9 | `fig_9_09_sankey.py` |
| 9-10 | `fig_9_10_grid.py` |
| 9-11/12 | `fig_9_11_page.py` |
| 9-13/14 | `fig_9_13_tab.py` |
| 9-15 | `fig_9_15_timeline.py` |
| 9-16 | `fig_9_16_theme_roma.py` |
| 9-17 | `fig_9_17_django_embed.py` |
| 9.7 | `hupu_section_bar.py`、`hupu_hourly_line.py` |
| 习题5 | `ex05_sine_animation.py` |

**一键生成全部 HTML / 静态图：**

""" + prog("run_all", "— 批量执行各图脚本") + """

```powershell
python Blog\\数据可视化-第九章\\code\\run_all.py
```
"""

OUT.write_text(BODY, encoding="utf-8")
print("wrote", OUT)
