#!/usr/bin/env python3
"""Regenerate content/ from the How to Rock Climb! LLM wiki.

Usage: python3 sync-wiki.py [path/to/wiki]

- Skips log.md (internal history, not reader-facing).
- Moves the page's `# Title` into frontmatter `title` (Quartz renders it).
- Copies `summary` to `description` (used for previews and link cards).
- Turns links to raw/ sources into plain text: the source PDF is not published.
"""
import re
import shutil
import sys
from pathlib import Path

DEFAULT_WIKI = Path.home() / "Documents/org-notes/llm-wiki/other/how-to-rock-climb/wiki"
SKIP = {"log.md"}

RAW_LINK = re.compile(r"\[([^\]]+)\]\(<?\.\./raw/[^)>]*>?\)")


def yaml_quote(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert(text: str, stem: str) -> str:
    fm, body = "", text
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4)
        fm, body = text[4:end], text[end + 5 :]

    body = body.lstrip("\n")
    title = None
    m = re.match(r"# (.+)\n", body)
    if m:
        title = m.group(1).strip()
        body = body[m.end() :].lstrip("\n")
    if stem == "index":
        title = "How to Rock Climb!"
        body = re.sub(r"\n## Meta\n.*?(?=\n## |\Z)", "\n", body, flags=re.S)

    body = RAW_LINK.sub(r"\1", body)

    extra = []
    if title:
        extra.append(f"title: {yaml_quote(title)}")
    sm = re.search(r"^summary: (\|-?\n(?:  .*\n?)+|.+)$", fm, re.M)
    if sm:
        val = sm.group(1)
        if val.startswith("|"):
            val = " ".join(l.strip() for l in val.splitlines()[1:])
        extra.append(f"description: {yaml_quote(val.strip())}")

    lines = extra + ([fm.rstrip("\n")] if fm else [])
    return "---\n" + "\n".join(lines) + "\n---\n\n" + body.rstrip() + "\n"


def main() -> None:
    wiki = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_WIKI
    content = Path(__file__).resolve().parent / "content"
    shutil.rmtree(content, ignore_errors=True)
    content.mkdir()
    n = 0
    for src in sorted(wiki.glob("*.md")):
        if src.name in SKIP:
            continue
        (content / src.name).write_text(convert(src.read_text(), src.stem))
        n += 1
    print(f"Wrote {n} pages to {content}")


if __name__ == "__main__":
    main()
