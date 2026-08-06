#!/usr/bin/env python3
"""
check-links.py — verify every relative link in the Markdown actually resolves.

Documentation that points at a file which does not exist is the same failure this
project exists to catch, one level up: a confident claim nobody checked. A README
promising `docs/INSTALL.md` when there is no such file reads exactly like one
where the file is there.

Checks relative links and image targets only. External URLs are not fetched —
that would need the network and would fail for reasons that have nothing to do
with this repository.

Stdlib only. Exit 1 if anything is broken.

Usage:
    python3 scripts/check-links.py
    python3 scripts/check-links.py --quiet
"""

import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

SKIP_DIRS = {".git", "node_modules", "dist", "__pycache__", ".venv"}

# [text](target) and ![alt](target), ignoring reference-style and inline code.
LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")

# Fenced code blocks — links inside them are examples, not claims.
FENCE = re.compile(r"```.*?```", re.S)


def is_external(target):
    return (
        "://" in target
        or target.startswith("#")
        or target.startswith("mailto:")
        or target.startswith("tel:")
    )


def markdown_files():
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".md"):
                yield Path(root) / f


def main(argv):
    quiet = "--quiet" in argv
    broken = []
    checked = 0
    files = 0

    for md in sorted(markdown_files()):
        files += 1
        text = md.read_text(encoding="utf-8", errors="replace")
        text = FENCE.sub("", text)

        for m in LINK.finditer(text):
            target = m.group(1).strip()

            # Strip a title:  [x](path "Title")
            if " " in target and not target.startswith("<"):
                target = target.split(" ", 1)[0]
            target = target.strip("<>")

            if not target or is_external(target):
                continue

            # Drop any anchor; we verify the file exists, not the heading.
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue

            checked += 1
            resolved = (md.parent / path_part).resolve()
            if not resolved.exists():
                broken.append((md.relative_to(REPO), target))

    if not quiet:
        print("checked %d relative link(s) across %d markdown file(s)" % (checked, files))

    # A checker that inspected nothing reports success forever.
    if files == 0 or checked == 0:
        print("FAIL: found no markdown or no relative links to check; "
              "the checker is not looking at anything", file=sys.stderr)
        return 1

    if broken:
        print("\n%d broken link(s):\n" % len(broken), file=sys.stderr)
        for src, target in broken:
            print("  %s  ->  %s" % (src, target), file=sys.stderr)
        return 1

    if not quiet:
        print("all relative links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
