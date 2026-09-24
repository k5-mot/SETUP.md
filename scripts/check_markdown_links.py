#!/usr/bin/env python3
"""Markdown内のLocal Link Targetが存在することを検証する。"""

from __future__ import annotations

import argparse
import logging
import re
import subprocess
import time
from pathlib import Path
from urllib.parse import unquote, urlsplit

LOGGER = logging.getLogger(__name__)
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)]+)\)")


def _git_markdown_files(root: Path) -> list[Path]:
    process = subprocess.run(
        [
            "git",
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            "*.md",
        ],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return [root / name for name in process.stdout.decode().split("\0") if name]


def _local_target(raw_target: str) -> str | None:
    target = raw_target.strip().strip("<>")
    if not target or target.startswith("#"):
        return None
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    return unquote(parsed.path)


def _broken_links(root: Path, files: list[Path]) -> list[str]:
    broken: list[str] = []
    for source in files:
        text = source.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            target = _local_target(match.group("target"))
            if target is None:
                continue
            resolved = (source.parent / target).resolve()
            if resolved.exists():
                continue
            line = text.count("\n", 0, match.start()) + 1
            broken.append(f"{source.relative_to(root)}:{line}: {target}")
    return broken


def main() -> int:
    """指定MarkdownまたはGit管理候補のLocal Linkを検証する。"""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()

    started = time.perf_counter()
    root = arguments.root.resolve()
    files = (
        [(root / path).resolve() for path in arguments.files]
        if arguments.files
        else _git_markdown_files(root)
    )
    broken = _broken_links(root, files)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    for finding in broken:
        LOGGER.error(finding)
    LOGGER.info(
        "markdown links files=%d broken=%d elapsed_seconds=%.3f",
        len(files),
        len(broken),
        time.perf_counter() - started,
    )
    return 1 if broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
