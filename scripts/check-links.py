#!/usr/bin/env python3
"""
check-links.py — verify every relative link in the Markdown actually resolves.

Documentation that points at a file which does not exist is the same failure this
project exists to catch, one level up: a confident claim nobody checked. A README
promising `docs/INSTALL.md` when there is no such file reads exactly like one
where the file is there.

Checks two things, both offline:

  1. Relative links and image targets.
  2. Absolute links that point back into THIS repository — the `blob/` and
     `raw.githubusercontent.com` forms. Those carry the same claim as a relative
     link and, until now, were skipped because they contained `://`.

     They exist for a reason: `release/RELEASE_NOTES_*.md` is consumed as a
     GitHub release body, where the file is not rendered from its own directory,
     so a relative `../docs/INSTALL.md` resolves to nothing. Absolute is the only
     form that is correct both in the repo and on the release page — so the
     checker has to be able to see it, or the most-read page in the project
     becomes the one page nothing verifies.

External URLs to anywhere else are not fetched — that would need the network and
would fail for reasons that have nothing to do with this repository.

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

# Absolute links that point back at this repository. Anything else on the
# internet is somebody else's to keep alive; these are ours.
_SELF_PREFIX = (
    r"https?://(?:"
    r"github\.com/antonio0720/writing-intelligence/(?:blob|tree|raw)/"
    r"|raw\.githubusercontent\.com/antonio0720/writing-intelligence/"
    r")"
)

SELF = re.compile(r"^" + _SELF_PREFIX + r"(?P<rest>.+)$")

# The same thing unanchored, for finding self-URLs in prose and in commands.
BARE_SELF_URL = re.compile(_SELF_PREFIX + r"[^\s)\"'`<>\]]+")


def is_external(target):
    return (
        "://" in target
        or target.startswith("#")
        or target.startswith("mailto:")
        or target.startswith("tel:")
    )


def self_link_path(target):
    """Repo-relative path a self-link claims, or None if it is not a self-link.

    The ref sits between the repo and the path and may itself contain slashes
    (`blob/claude/some-branch/README.md`), so where the ref ends is genuinely
    ambiguous from the URL alone. Every split point is tried and the first that
    resolves on disk wins. That is permissive in the harmless direction: a link
    to a file that does not exist under ANY split still fails, which is the
    defect worth catching, while a branch name with a slash does not produce a
    false alarm. A checker that cries wolf is one somebody switches off, and the
    real rule goes with it.
    """
    m = SELF.match(target)
    if not m:
        return None
    parts = m.group("rest").split("/")
    for i in range(1, len(parts)):
        candidate = "/".join(parts[i:])
        if candidate and (REPO / candidate).exists():
            return candidate
    # Nothing resolved. Report the most likely reading: one ref segment.
    return "/".join(parts[1:]) if len(parts) > 1 else None


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
    self_checked = 0
    files = 0

    for md in sorted(markdown_files()):
        files += 1
        raw = md.read_text(encoding="utf-8", errors="replace")

        # Self-URLs are checked in the RAW text, fences included. A fenced
        # `curl -LO https://raw.githubusercontent.com/.../writing-intelligence.skill`
        # is not an illustration — it is the install command for everyone who
        # is not a developer, and a typo in that path breaks the only download
        # path they have while the page still reads as correct.
        seen = set()
        for m in BARE_SELF_URL.finditer(raw):
            url = m.group(0).rstrip(".,;:")
            if url in seen:
                continue
            seen.add(url)
            claimed = self_link_path(url)
            if claimed is None:
                continue
            self_checked += 1
            if not (REPO / claimed.split("#", 1)[0]).exists():
                broken.append((md.relative_to(REPO), url))

        text = FENCE.sub("", raw)

        for m in LINK.finditer(text):
            target = m.group(1).strip()

            # Strip a title:  [x](path "Title")
            if " " in target and not target.startswith("<"):
                target = target.split(" ", 1)[0]
            target = target.strip("<>")

            if not target:
                continue

            # Self-URLs were already covered by the raw-text pass above.
            if is_external(target):
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
        print("checked %d relative and %d self link(s) across %d markdown file(s)"
              % (checked, self_checked, files))

    # A checker that inspected nothing reports success forever.
    if files == 0 or (checked + self_checked) == 0:
        print("FAIL: found no markdown or no relative links to check; "
              "the checker is not looking at anything", file=sys.stderr)
        return 1

    if broken:
        print("\n%d broken link(s):\n" % len(broken), file=sys.stderr)
        for src, target in broken:
            print("  %s  ->  %s" % (src, target), file=sys.stderr)
        return 1

    if not quiet:
        print("all links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
