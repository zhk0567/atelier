"""Annotate pyecharts example code with per-line semantic highlights for the blog."""

from __future__ import annotations

import html
import re

_LINE_RULES: tuple[tuple[str, str], ...] = (
    (
        "pec-output",
        r"\.render\(|render_embed|FuncAnimation|anim\.save|HttpResponse\(",
    ),
    (
        "pec-config",
        r"\.set_global_opts|\.set_series_opts|add_schema|InitOpts|ThemeType|"
        r"grid_opts\s*=|Axis3DOpts|VisualMapOpts|EffectOpts|LineStyleOpts|"
        r"label_opts\s*=|linestyle_opt",
    ),
    (
        "pec-compose",
        r"Grid\(|Page\(|Tab\(|Timeline\(|grid\.add|page\.add|tab\.add|tl\.add|"
        r"for year in",
    ),
    (
        "pec-data",
        r"\.add_xaxis|\.add_yaxis|nodes\s*=|links\s*=|^data\s*=|=\s*\[|"
        r"SECTIONS|POST_|HOURS|ALL_SITE|\bNBA\b|CLOTHES|SALES_|PHONES|"
        r"days\s*=|groups\s*=|\braw\s*=|rng\.|np\.|print\(Faker|"
        r"clothes\s*=|sales_[ab]\s*=",
    ),
    (
        "pec-step",
        r"Bar\(|Line\(|Pie\(|Scatter|EffectScatter|Bar3D|Sankey\(|"
        r"return\s*\(|^\s*\.add\(",
    ),
)


def classify_line(line: str) -> str | None:
    s = line.strip()
    if not s:
        return None
    if s.startswith(("import ", "from ", "def ", "class ")):
        return None
    if s.startswith("#") and not s.startswith("# chart"):
        return "pec-note"
    for kind, pattern in _LINE_RULES:
        if re.search(pattern, s):
            return kind
    if s.startswith("."):
        return "pec-step"
    return "pec-muted"


def _code_inner(body: str) -> str:
    rows: list[str] = []
    for line in body.splitlines():
        esc = html.escape(line)
        kind = classify_line(line)
        if kind:
            rows.append(f'<span class="pec-line {kind}">{esc}</span>')
        else:
            rows.append(esc)
    return "\n".join(rows)


def highlighted_block(body: str, *, legend: bool = True) -> str:
    legend_html = ""
    if legend:
        legend_html = """<p class="pyecharts-code__legend">
<span class="pec-chip pec-data">数据</span>
<span class="pec-chip pec-step">建图链式</span>
<span class="pec-chip pec-config">配置项</span>
<span class="pec-chip pec-compose">组合布局</span>
<span class="pec-chip pec-output">渲染输出</span>
<span class="pec-chip pec-note">注释</span>
</p>
"""
    return (
        f'<div class="pyecharts-code">\n{legend_html}'
        f'<pre class="pyecharts-code__pre"><code>{_code_inner(body)}</code></pre>\n'
        f"</div>\n"
    )


def highlighted_snippet(source: str, *, legend: bool = False) -> str:
    return highlighted_block(source.strip(), legend=legend)
