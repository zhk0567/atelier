"""9.7 实战：全站与 NBA 板块 24 小时发帖折线图（示例数据）。"""

from pyecharts import options as opts
from pyecharts.charts import Line

from _paths import HTML_DIR, ensure_dirs

HOURS = [f"{h:02d}:00" for h in range(24)]
ALL_SITE = [42, 28, 18, 12, 10, 15, 38, 62, 88, 95, 102, 110, 118, 125, 130, 128, 135, 148, 156, 142, 120, 98, 72, 55]
NBA = [18, 12, 8, 6, 5, 7, 16, 28, 40, 44, 48, 52, 55, 58, 60, 58, 62, 68, 72, 65, 52, 42, 30, 22]


def main() -> None:
    ensure_dirs()
    line = (
        Line(init_opts=opts.InitOpts(width="760px", height="400px"))
        .add_xaxis(HOURS)
        .add_yaxis("全站", ALL_SITE, is_smooth=True)
        .add_yaxis("NBA", NBA, is_smooth=True)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="虎扑 24 小时发帖量（示例）"),
            xaxis_opts=opts.AxisOpts(name="时刻"),
            yaxis_opts=opts.AxisOpts(name="帖子数"),
            legend_opts=opts.LegendOpts(pos_top="8%"),
        )
    )
    line.render(str(HTML_DIR / "hupu_hourly_line.html"))


if __name__ == "__main__":
    main()
