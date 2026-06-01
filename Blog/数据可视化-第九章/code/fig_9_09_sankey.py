"""图 9-9 桑基图示例（教材数据）。"""

from pyecharts import options as opts
from pyecharts.charts import Sankey

from _paths import HTML_DIR, ensure_dirs


def main() -> None:
    ensure_dirs()
    nodes = [
        {"name": "消费者"},
        {"name": "老客户"},
        {"name": "新客户"},
        {"name": "运动鞋"},
        {"name": "衬衫"},
        {"name": "连衣裙"},
        {"name": "高跟鞋"},
    ]
    links = [
        {"source": "消费者", "target": "老客户", "value": 30},
        {"source": "消费者", "target": "新客户", "value": 20},
        {"source": "老客户", "target": "运动鞋", "value": 10},
        {"source": "老客户", "target": "衬衫", "value": 20},
        {"source": "新客户", "target": "连衣裙", "value": 10},
        {"source": "新客户", "target": "高跟鞋", "value": 10},
    ]
    chart = (
        Sankey(init_opts=opts.InitOpts(width="800px", height="450px"))
        .add(
            "",
            nodes,
            links,
            linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source"),
            label_opts=opts.LabelOpts(position="right"),
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="桑基图示例"))
    )
    chart.render(str(HTML_DIR / "fig_9_09_sankey.html"))


if __name__ == "__main__":
    main()
