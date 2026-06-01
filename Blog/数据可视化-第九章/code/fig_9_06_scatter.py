"""图 9-6 散点图示例。"""

import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Scatter

from _paths import HTML_DIR, ensure_dirs


def main() -> None:
    ensure_dirs()
    x = list(range(1, 21))
    rng = np.random.default_rng(42)
    y = rng.integers(10, 41, size=20).tolist()
    scatter = (
        Scatter(init_opts=opts.InitOpts(width="600px", height="380px"))
        .add_xaxis(x)
        .add_yaxis("样本", y)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="散点图示例"),
            xaxis_opts=opts.AxisOpts(name="X"),
            yaxis_opts=opts.AxisOpts(name="Y"),
        )
    )
    scatter.render(str(HTML_DIR / "fig_9_06_scatter.html"))


if __name__ == "__main__":
    main()
