"""thread-splitter-lite：把长文拆成带编号、带钩子的社媒帖子串。

按段落聚合，使每条帖子不超过 max_len 字符；超长段落再硬切。
首帖加一个钩子开头，每条帖子带 "n/total" 尾注。
"""

from __future__ import annotations

import re

DEFAULT_HOOK = "下面是一条帖子串，全文分 {total} 条讲完 👇"


def _split_paragraphs(text: str) -> list[str]:
    """把文本切成段落：先按空行，再按单换行。"""
    paras: list[str] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        block = block.strip()
        if not block:
            continue
        for line in block.splitlines():
            line = line.strip()
            if line:
                paras.append(line)
    return paras


def _hard_split(seg: str, max_len: int) -> list[str]:
    """把超长段落硬切成不超过 max_len 的片段。"""
    if len(seg) <= max_len:
        return [seg]
    parts = []
    cur = ""
    sentences = re.split(r"(?<=[。！？!?；;])", seg)
    for s in sentences:
        if not s:
            continue
        if len(cur) + len(s) <= max_len:
            cur += s
        else:
            if cur:
                parts.append(cur)
            while len(s) > max_len:
                parts.append(s[:max_len])
                s = s[max_len:]
            cur = s
    if cur:
        parts.append(cur)
    return parts


def split_thread(text: str, max_len: int = 300,
                 hook: str | None = None) -> list[str]:
    """把长文拆成帖子串。

    max_len：每条帖子正文（不含尾注）目标上限。
    hook：首帖钩子模板，{total} 会被替换为总条数；传空串则不加钩子。
    """
    paras = _split_paragraphs(text)
    units: list[str] = []
    for p in paras:
        units.extend(_hard_split(p, max_len))

    if not units:
        return []

    footer_guess = " (1/1)"
    budget = max_len - len(footer_guess)

    chunks: list[str] = []
    cur = ""
    for u in units:
        if not cur:
            cur = u
        elif len(cur) + 1 + len(u) <= budget:
            cur += "\n" + u
        else:
            chunks.append(cur)
            cur = u
    if cur:
        chunks.append(cur)

    total = len(chunks)

    use_hook = hook if hook is not None else DEFAULT_HOOK
    if use_hook:
        hook_text = use_hook.format(total=total) + "\n"
        if len(hook_text) + len(chunks[0]) > budget:
            chunks.insert(0, "")
            total = len(chunks)
            hook_text = use_hook.format(total=total) + "\n"
        chunks[0] = hook_text + chunks[0]

    out = []
    for i, c in enumerate(chunks, 1):
        out.append(f"{c.rstrip()} ({i}/{total})")
    return out


def render_thread(posts: list[str]) -> str:
    """把帖子串渲染成带分隔线的纯文本。"""
    return ("\n\n— 👇 —\n\n").join(posts)
