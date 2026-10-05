"""thread-splitter-lite 命令行入口。

用法示例：
    python3 cli.py --file long_article.txt
    python3 cli.py --text "第一段。第二段。" --max-len 120
"""

from __future__ import annotations

import argparse
import sys

from thread_splitter import render_thread, split_thread


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="thread-splitter-lite",
        description="把长文拆成带编号、带钩子的社媒帖子串",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="直接传入长文")
    src.add_argument("--file", help="从文本文件读取长文")
    p.add_argument("--max-len", type=int, default=300, help="每条帖子目标字符上限，默认 300")
    p.add_argument("--no-hook", action="store_true", help="不添加首帖钩子")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = args.text or ""

    hook = "" if args.no_hook else None
    posts = split_thread(text, max_len=args.max_len, hook=hook)
    print(render_thread(posts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
