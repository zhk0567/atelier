"""9.7 实战：各板块发帖量柱形图（示例数据）。"""

from pyecharts import options as opts
from pyecharts.charts import Bar

from _paths import HTML_DIR, ensure_dirs

SECTIONS = ["篮球", "足球", "汽车", "NBA", "影视", "数码", "步行街", "国际足球"]
POST_COUNTS = [1280, 860, 540, 990, 430, 380, 720, 310]


def main() -> None:
    ensure_dirs()
    bar = (
        Bar(init_opts=opts.InitOpts(width="720px", height="400px"))
        .add_xaxis(SECTIONS)
        .add_yaxis("发帖数", POST_COUNTS)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="虎扑社区各板块发帖量（示例）"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
            yaxis_opts=opts.AxisOpts(name="帖子数"),
            datazoom_opts=[opts.DataZoomOpts()],
        )
        .set_series_opts(label_opts=opts.LabelOpts(position="top"))
    )
    bar.render(str(HTML_DIR / "hupu_section_bar.html"))


if __name__ == "__main__":
    main()
