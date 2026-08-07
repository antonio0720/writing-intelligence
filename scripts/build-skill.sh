#!/usr/bin/env bash
#
# build-skill.sh — package Writing Intelligence as an installable .skill bundle.
#
# Produces:
#   dist/writing-intelligence.skill          the uploadable bundle (zip)
#   dist/writing-intelligence.skill.sha256   checksum for release verification
#   writing-intelligence.skill               copy at repo root, for direct download
#
# The build is reproducible: file order is sorted and every mtime is normalized,
# so the same tree produces the same bytes and the published checksum means
# something. Run it from anywhere; it locates the repo itself.
#
# Usage:
#   bash scripts/build-skill.sh              build, verify, write dist/ and root copy
#   bash scripts/build-skill.sh --no-root    build without updating the root copy
#   bash scripts/build-skill.sh --check      build to a temp dir and verify only
#
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

NAME="writing-intelligence"
UPDATE_ROOT=1
CHECK_ONLY=0
for arg in "$@"; do
  case "$arg" in
    --no-root) UPDATE_ROOT=0 ;;
    --check)   CHECK_ONLY=1; UPDATE_ROOT=0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

# What ships inside the bundle.
#
# Two constraints shape this list, and the second one is a hard wall:
#
#   1. The REST service, CI config and repo scaffolding are not useful inside a
#      chat surface and more than double the download.
#   2. **A skill bundle may contain at most 200 files.** Exceed it and the
#      upload is rejected outright — the bundle does not degrade, it simply
#      will not load, which makes every install instruction in this repository
#      false. MAX_FILES below enforces it at build time so that can never ship.
#
# So the payload is the operating set: the skill, the doctrine it cites, the
# schemas, the agents, the verifier, and the fixtures that prove the verifier
# works. Benchmarks, certification rubrics, release notes, worked examples and
# the regression corpora are repository material — they stay in the repo, where
# they are one `git clone` away, and nothing in the shipped set links to them.
PAYLOAD=(
  SKILL.md
  README.md
  CHANGELOG.md
  CHEATSHEET.md
  USER_GUIDE.md
  ROADMAP.md
  CONTRIBUTING.md
  LICENSE
  agents
  docs
  governance
  references
  schemas
  scripts/wi.py
  tests/v4
  tests/v5
)

# The upload limit. Not a style preference — a bundle over this does not load.
MAX_FILES=200
WARN_FILES=185

# --------------------------------------------------------------------------
# Preflight. A bundle that ships a broken verifier is worse than no bundle,
# because it looks installed.
# --------------------------------------------------------------------------
echo "==> Preflight"

for p in "${PAYLOAD[@]}"; do
  [ -e "$p" ] || { echo "FAIL missing payload path: $p" >&2; exit 1; }
done
echo "    payload paths present"

head -1 SKILL.md | grep -qx -- '---' \
  || { echo "FAIL SKILL.md has no YAML frontmatter; the skill loader reads it" >&2; exit 1; }
grep -qE '^name: +' SKILL.md \
  || { echo "FAIL SKILL.md frontmatter has no name:" >&2; exit 1; }
grep -qE '^description: +' SKILL.md \
  || { echo "FAIL SKILL.md frontmatter has no description:" >&2; exit 1; }
echo "    SKILL.md frontmatter intact"

V4_DOCS=$(ls references/v4/*.md 2>/dev/null | wc -l | tr -d ' ')
[ "$V4_DOCS" -ge 8 ] \
  || { echo "FAIL expected >=8 v4 reference docs, found $V4_DOCS" >&2; exit 1; }
echo "    v4 reference docs: $V4_DOCS"

# v4 doctrine is not deleted by v5; it is the compatibility layer beneath it.
# Both must be present or the skill degrades into naming laws it cannot cite.
V5_DOCS=$(ls references/v5/*.md 2>/dev/null | wc -l | tr -d ' ')
[ "$V5_DOCS" -ge 20 ] \
  || { echo "FAIL expected >=20 v5 reference docs, found $V5_DOCS" >&2; exit 1; }
echo "    v5 reference docs: $V5_DOCS"

V5_SCHEMAS=$(ls schemas/v5/*.json 2>/dev/null | wc -l | tr -d ' ')
[ "$V5_SCHEMAS" -ge 14 ] \
  || { echo "FAIL expected >=14 v5 schemas, found $V5_SCHEMAS" >&2; exit 1; }
echo "    v5 schemas: $V5_SCHEMAS"

# The version in the CLI, the skill and the changelog must be one number.
CLI_V=$(python3 scripts/wi.py --version 2>/dev/null | awk '{print $2}')
grep -q "^\*\*Version:\*\* $CLI_V" SKILL.md \
  || { echo "FAIL SKILL.md does not declare version $CLI_V" >&2; exit 1; }
grep -q "## \[$CLI_V\]" CHANGELOG.md \
  || { echo "FAIL CHANGELOG.md has no entry for $CLI_V" >&2; exit 1; }
echo "    version consistent: $CLI_V"

if command -v python3 >/dev/null 2>&1; then
  for SUITE in tests/v4/test_wi.sh tests/v5/test_wi5.sh; do
    if RESULT=$(bash "$SUITE" 2>&1); then
      echo "$RESULT" | sed 's/^/    /'
    else
      echo "$RESULT" | sed 's/^/    /'
      echo "FAIL $SUITE did not pass; refusing to build a bundle" >&2
      echo "     shipping a broken verifier is worse than shipping none — it looks installed" >&2
      exit 1
    fi
  done
else
  echo "    WARN python3 not found; verifier regressions not run" >&2
fi

# --------------------------------------------------------------------------
# Stage
# --------------------------------------------------------------------------
echo "==> Staging"

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT
ROOT="$STAGE/$NAME"
mkdir -p "$ROOT"

for p in "${PAYLOAD[@]}"; do
  if [ -d "$p" ]; then
    # -L resolves symlinks into real files; a bundle must be self-contained.
    mkdir -p "$ROOT/$(dirname "$p")"
    cp -RL "$p" "$ROOT/$(dirname "$p")/"
  else
    mkdir -p "$ROOT/$(dirname "$p")"
    cp -L "$p" "$ROOT/$p"
  fi
done

# Strip anything that should never ship.
find "$ROOT" \( -name '__pycache__' -o -name '.DS_Store' -o -name '*.pyc' \
              -o -name '*.original-*' -o -name '*.claims.json' \) \
     -exec rm -rf {} + 2>/dev/null || true

FILES=$(find "$ROOT" -type f | wc -l | tr -d ' ')
echo "    staged $FILES files (limit $MAX_FILES)"

# A bundle that exceeds the limit is not a degraded bundle. It is a bundle
# nobody can install, shipped from a repository whose README says they can.
# Fail here, loudly, with the arithmetic already done.
if [ "$FILES" -gt "$MAX_FILES" ]; then
  echo "FAIL bundle has $FILES files; the skill upload limit is $MAX_FILES" >&2
  echo "     over by $(( FILES - MAX_FILES )). Largest directories:" >&2
  ( cd "$ROOT" && find . -type f | sed 's|^\./||; s|/[^/]*$||' \
      | sort | uniq -c | sort -rn | head -12 | sed 's/^/       /' ) >&2
  echo "     Drop a directory from PAYLOAD, or split it. Do not raise MAX_FILES:" >&2
  echo "     the limit is imposed by the installer, not by this script." >&2
  exit 1
fi
if [ "$FILES" -gt "$WARN_FILES" ]; then
  echo "    WARN only $(( MAX_FILES - FILES )) file(s) of headroom remain" >&2
fi

# Normalize mtimes so the archive is byte-reproducible.
find "$ROOT" -exec touch -t 200001010000.00 {} + 2>/dev/null || true

# --------------------------------------------------------------------------
# Archive
# --------------------------------------------------------------------------
echo "==> Archiving"

OUT_DIR="$REPO/dist"
[ "$CHECK_ONLY" -eq 1 ] && OUT_DIR="$STAGE/out"
mkdir -p "$OUT_DIR"
BUNDLE="$OUT_DIR/$NAME.skill"
rm -f "$BUNDLE"

# -X drops extra file attributes (uid/gid/timestamps) that vary per machine.
( cd "$STAGE" && find "$NAME" -print | sort | zip -qX9 "$BUNDLE" -@ )

SIZE=$(wc -c < "$BUNDLE" | tr -d ' ')
echo "    $BUNDLE ($SIZE bytes)"

# --------------------------------------------------------------------------
# Verify the artifact, not the intention
# --------------------------------------------------------------------------
echo "==> Verifying bundle"

VERIFY="$(mktemp -d)"
trap 'rm -rf "$STAGE" "$VERIFY"' EXIT
unzip -qq "$BUNDLE" -d "$VERIFY"

[ -f "$VERIFY/$NAME/SKILL.md" ]             || { echo "FAIL bundle has no SKILL.md" >&2; exit 1; }
[ -f "$VERIFY/$NAME/scripts/wi.py" ]        || { echo "FAIL bundle has no scripts/wi.py" >&2; exit 1; }
[ -d "$VERIFY/$NAME/references/v4" ]        || { echo "FAIL bundle has no references/v4" >&2; exit 1; }
[ -d "$VERIFY/$NAME/references/v5" ]        || { echo "FAIL bundle has no references/v5" >&2; exit 1; }
[ -d "$VERIFY/$NAME/schemas/v5" ]           || { echo "FAIL bundle has no schemas/v5" >&2; exit 1; }
[ ! -d "$VERIFY/$NAME/services" ]           || { echo "FAIL bundle contains services/" >&2; exit 1; }
[ ! -d "$VERIFY/$NAME/.git" ]               || { echo "FAIL bundle contains .git" >&2; exit 1; }

# The verifier must work when extracted, not only in the repo.
if command -v python3 >/dev/null 2>&1; then
  ( cd "$VERIFY/$NAME" && python3 scripts/wi.py --version >/dev/null ) \
    || { echo "FAIL wi.py does not run from the extracted bundle" >&2; exit 1; }
  for SUITE in tests/v4/test_wi.sh tests/v5/test_wi5.sh; do
    if RESULT=$( cd "$VERIFY/$NAME" && bash "$SUITE" 2>&1 ); then
      echo "$RESULT" | sed 's/^/    /'
    else
      echo "$RESULT" | sed 's/^/    /'
      echo "FAIL $SUITE fails inside the extracted bundle" >&2
      exit 1
    fi
  done
fi

echo "    bundle verified"

if [ "$CHECK_ONLY" -eq 1 ]; then
  echo "==> --check: no artifacts written"
  exit 0
fi

# --------------------------------------------------------------------------
# Checksum and publish
# --------------------------------------------------------------------------
echo "==> Checksum"

if command -v shasum >/dev/null 2>&1; then
  ( cd "$OUT_DIR" && shasum -a 256 "$NAME.skill" > "$NAME.skill.sha256" )
elif command -v sha256sum >/dev/null 2>&1; then
  ( cd "$OUT_DIR" && sha256sum "$NAME.skill" > "$NAME.skill.sha256" )
else
  echo "    WARN no shasum/sha256sum; checksum not written" >&2
fi
[ -f "$OUT_DIR/$NAME.skill.sha256" ] && cat "$OUT_DIR/$NAME.skill.sha256" | sed 's/^/    /'

if [ "$UPDATE_ROOT" -eq 1 ]; then
  cp "$BUNDLE" "$REPO/$NAME.skill"
  echo "    updated $REPO/$NAME.skill"
fi

echo
echo "Built $NAME.skill — $FILES files, $SIZE bytes."
echo "Upload path: Claude → Settings → Capabilities → Skills → Upload skill"
