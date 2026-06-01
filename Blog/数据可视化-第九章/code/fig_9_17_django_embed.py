"""图 9-17 Django 整合思路：生成与 render_embed() 等价的单页 HTML。"""

from pyecharts import options as opts
from pyecharts.charts import Bar

from _paths import HTML_DIR, ensure_dirs

CLOTHES = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
SALES_A = [5, 20, 36, 10, 75, 90]
SALES_B = [15, 25, 16, 55, 48, 8]


def main() -> None:
    ensure_dirs()
    bar = (
        Bar(init_opts=opts.InitOpts(width="640px", height="360px"))
        .add_xaxis(CLOTHES)
        .add_yaxis("商家A", SALES_A)
        .add_yaxis("商家B", SALES_B)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="柱形图示例", subtitle="我是副标题"),
            yaxis_opts=opts.AxisOpts(
                name="销售额(万元)",
                name_location="center",
                name_gap=30,
            ),
        )
    )
    embed = bar.render_embed()
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title>pyecharts Django 嵌入示例</title>
</head>
<body>
  <h1>模拟 HttpResponse(chart.render_embed())</h1>
  {embed}
</body>
</html>
"""
    out = HTML_DIR / "fig_9_17_django_embed.html"
    out.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
