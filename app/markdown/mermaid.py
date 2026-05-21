"""Turn fenced ```mermaid blocks into renderable Mermaid markup."""

from __future__ import annotations

import html
import re

_MERMAID_FENCE_RE = re.compile(
    r"<pre><code class=\"language-mermaid\">(.*?)</code></pre>",
    re.DOTALL | re.IGNORECASE,
)


def apply_mermaid_blocks(markup: str) -> tuple[str, bool]:
    """Replace markdown fenced mermaid with <pre class=\"mermaid\">; return (html, has_mermaid)."""

    def repl(match: re.Match[str]) -> str:
        body = html.unescape(match.group(1).strip())
        return f'<pre class="mermaid">{html.escape(body)}</pre>'

    converted, count = _MERMAID_FENCE_RE.subn(repl, markup)
    return converted, count > 0
