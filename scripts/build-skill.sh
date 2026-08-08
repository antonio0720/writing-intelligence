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
  # NOTICE and PATENTS.md ship with LICENSE, not instead of it. LICENSE is a
  # copyright grant and is silent on trademarks and patents; a bundle carrying
  # it alone tells a recipient the terms are MIT and nothing else, which is
  # true and incomplete in the two places a recipient would want it complete.
  NOTICE
  PATENTS.md
  agents
  docs
  governance
  plans
  references/v4
  references/v5
  references/v6
  schemas
  scripts/wi.py
  tests/v4
  tests/v5
  tests/v6
)

# The second bundle: the craft library.
#
# At v5 the single bundle was 182 files against a 200-file ceiling — eighteen
# files of headroom for a system that grows by adding doctrine. v6 adds 24
# reference documents, 20 schemas and a regression suite, which is 45 files on
# its own. There is no arrangement of one bundle that fits.
#
# So the library splits from the runtime. This is not a downgrade dressed as
# an architecture decision; it is the only shape that leaves both halves able
# to grow, and it is what `references/v6/PACKAGE_SYSTEM.md` argues for on
# independent grounds: the skill bundle is not the product payload.
CRAFT_NAME="writing-intelligence-craft"
CRAFT_SKILL=packs/craft/SKILL.md
CRAFT_PAYLOAD=(
  LICENSE
  references/academic
  references/anti_patterns
  references/compiler
  references/diagnostics
  references/genre_packs
  references/positive_patterns
  references/voiceprints
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

# The frontmatter is what the loader reads, and every field in it has a hard
# limit on the other side. A bundle that violates one is not degraded — it is
# rejected, which turns every install instruction in this repository into a
# false claim. Check the arithmetic here, where it is cheap.
python3 - <<'FRONTMATTER' || exit 1
import re, sys

MAX_NAME, MAX_DESC = 64, 1024
src = open("SKILL.md", encoding="utf-8").read()

if not src.startswith("---\n"):
    sys.exit("FAIL SKILL.md has no YAML frontmatter; the skill loader reads it")
end = src.find("\n---", 4)
if end < 0:
    sys.exit("FAIL SKILL.md frontmatter is not terminated")
fm = src[4:end]

fields, bad = {}, []
for key in ("name", "description"):
    m = re.search(r"^%s:[ \t]+(.*)$" % key, fm, re.M)
    if not m:
        sys.exit("FAIL SKILL.md frontmatter has no %s:" % key)
    fields[key] = m.group(1).strip().strip('"\'')

if len(fields["name"]) > MAX_NAME:
    bad.append("name is %d characters; the limit is %d"
               % (len(fields["name"]), MAX_NAME))
if not re.match(r"^[a-z0-9][a-z0-9-]*$", fields["name"]):
    bad.append("name %r must be lowercase letters, digits and hyphens"
               % fields["name"])

n = len(fields["description"])
if n > MAX_DESC:
    bad.append("description is %d characters, over by %d; the limit is %d"
               % (n, n - MAX_DESC, MAX_DESC))
elif n > MAX_DESC - 40:
    print("    WARN description has only %d character(s) of headroom"
          % (MAX_DESC - n), file=sys.stderr)

# A colon followed by a space inside an unquoted plain scalar is ambiguous
# YAML. It parses in some loaders and not others, which is the worst kind of
# bug: it works here and fails on the surface the user actually installs to.
if ": " in fields["description"]:
    bad.append("description contains ': ' — quote it or rewrite the clause; "
               "unquoted plain scalars must not contain a colon-space")

if bad:
    for b in bad:
        print("FAIL " + b, file=sys.stderr)
    sys.exit(1)

print("    SKILL.md frontmatter intact "
      "(name %d/%d, description %d/%d characters)"
      % (len(fields["name"]), MAX_NAME, n, MAX_DESC))
FRONTMATTER

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

# v6 doctrine and schemas are the release. A bundle that ships the v6 command
# surface without the documents that govern it would be a skill naming laws it
# cannot cite, which is the failure this project exists to catch.
V6_DOCS=$(ls references/v6/*.md 2>/dev/null | wc -l | tr -d ' ')
[ "$V6_DOCS" -ge 23 ] \
  || { echo "FAIL expected >=23 v6 reference docs, found $V6_DOCS" >&2; exit 1; }
echo "    v6 reference docs: $V6_DOCS"

V6_SCHEMAS=$(ls schemas/v6/*.json 2>/dev/null | wc -l | tr -d ' ')
[ "$V6_SCHEMAS" -ge 20 ] \
  || { echo "FAIL expected >=20 v6 schemas, found $V6_SCHEMAS" >&2; exit 1; }
echo "    v6 schemas: $V6_SCHEMAS"

[ -f "$CRAFT_SKILL" ] \
  || { echo "FAIL missing craft bundle skill: $CRAFT_SKILL" >&2; exit 1; }

# The version in the CLI, the skill and the changelog must be one number.
CLI_V=$(python3 scripts/wi.py --version 2>/dev/null | awk '{print $2}')
grep -q "^\*\*Version:\*\* $CLI_V" SKILL.md \
  || { echo "FAIL SKILL.md does not declare version $CLI_V" >&2; exit 1; }
grep -q "## \[$CLI_V\]" CHANGELOG.md \
  || { echo "FAIL CHANGELOG.md has no entry for $CLI_V" >&2; exit 1; }
echo "    version consistent: $CLI_V"

if command -v python3 >/dev/null 2>&1; then
  for SUITE in tests/v4/test_wi.sh tests/v5/test_wi5.sh tests/v6/test_wi6.sh; do
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
[ -d "$VERIFY/$NAME/references/v6" ]        || { echo "FAIL bundle has no references/v6" >&2; exit 1; }
[ -d "$VERIFY/$NAME/schemas/v5" ]           || { echo "FAIL bundle has no schemas/v5" >&2; exit 1; }
[ -d "$VERIFY/$NAME/schemas/v6" ]           || { echo "FAIL bundle has no schemas/v6" >&2; exit 1; }
[ ! -d "$VERIFY/$NAME/services" ]           || { echo "FAIL bundle contains services/" >&2; exit 1; }
[ ! -d "$VERIFY/$NAME/.git" ]               || { echo "FAIL bundle contains .git" >&2; exit 1; }

# The verifier must work when extracted, not only in the repo.
if command -v python3 >/dev/null 2>&1; then
  ( cd "$VERIFY/$NAME" && python3 scripts/wi.py --version >/dev/null ) \
    || { echo "FAIL wi.py does not run from the extracted bundle" >&2; exit 1; }
  for SUITE in tests/v4/test_wi.sh tests/v5/test_wi5.sh tests/v6/test_wi6.sh; do
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

# --------------------------------------------------------------------------
# The craft library bundle.
#
# Built and verified with the same rigour as the runtime, because the failure
# mode is identical: an over-ceiling bundle does not load, and a repository
# that tells people to install two skills has to be right about both.
# --------------------------------------------------------------------------
echo "==> Craft bundle"

CSTAGE="$(mktemp -d)"
CROOT="$CSTAGE/$CRAFT_NAME"
mkdir -p "$CROOT"
cp -L "$CRAFT_SKILL" "$CROOT/SKILL.md"
for p in "${CRAFT_PAYLOAD[@]}"; do
  [ -e "$p" ] || { echo "FAIL missing craft payload path: $p" >&2; exit 1; }
  mkdir -p "$CROOT/$(dirname "$p")"
  if [ -d "$p" ]; then cp -RL "$p" "$CROOT/$(dirname "$p")/"; else cp -L "$p" "$CROOT/$p"; fi
done
find "$CROOT" \( -name '__pycache__' -o -name '.DS_Store' -o -name '*.pyc' \) \
     -exec rm -rf {} + 2>/dev/null || true

CFILES=$(find "$CROOT" -type f | wc -l | tr -d ' ')
echo "    staged $CFILES files (limit $MAX_FILES)"
if [ "$CFILES" -gt "$MAX_FILES" ]; then
  echo "FAIL craft bundle has $CFILES files; the skill upload limit is $MAX_FILES" >&2
  exit 1
fi

# Same frontmatter arithmetic as the runtime skill. Both are uploaded, so both
# are rejected on the same rules.
CRAFT_SKILL_PATH="$CROOT/SKILL.md" python3 - <<'CRAFTFM' || exit 1
import os, re, sys
MAX_NAME, MAX_DESC = 64, 1024
src = open(os.environ["CRAFT_SKILL_PATH"], encoding="utf-8").read()
if not src.startswith("---\n"):
    sys.exit("FAIL craft SKILL.md has no YAML frontmatter")
fm = src[4:src.find("\n---", 4)]
bad = []
for key, limit in (("name", MAX_NAME), ("description", MAX_DESC)):
    m = re.search(r"^%s:[ \t]+(.*)$" % key, fm, re.M)
    if not m:
        sys.exit("FAIL craft SKILL.md frontmatter has no %s:" % key)
    v = m.group(1).strip().strip('"\'')
    if len(v) > limit:
        bad.append("%s is %d characters, over by %d; the limit is %d"
                   % (key, len(v), len(v) - limit, limit))
    if key == "description" and ": " in v:
        bad.append("description contains ': ' — unquoted plain scalars must not")
    if key == "name" and not re.match(r"^[a-z0-9][a-z0-9-]*$", v):
        bad.append("name %r must be lowercase letters, digits and hyphens" % v)
if bad:
    for b in bad:
        print("FAIL " + b, file=sys.stderr)
    sys.exit(1)
print("    craft SKILL.md frontmatter intact")
CRAFTFM

find "$CROOT" -exec touch -t 200001010000.00 {} + 2>/dev/null || true
CRAFT_BUNDLE="$OUT_DIR/$CRAFT_NAME.skill"
rm -f "$CRAFT_BUNDLE"
( cd "$CSTAGE" && find "$CRAFT_NAME" -print | sort | zip -qX9 "$CRAFT_BUNDLE" -@ )
CSIZE=$(wc -c < "$CRAFT_BUNDLE" | tr -d ' ')
echo "    $CRAFT_BUNDLE ($CSIZE bytes)"

CVERIFY="$(mktemp -d)"
unzip -qq "$CRAFT_BUNDLE" -d "$CVERIFY"
[ -f "$CVERIFY/$CRAFT_NAME/SKILL.md" ] \
  || { echo "FAIL craft bundle has no SKILL.md" >&2; exit 1; }
[ -d "$CVERIFY/$CRAFT_NAME/references/genre_packs" ] \
  || { echo "FAIL craft bundle has no genre packs" >&2; exit 1; }
[ ! -d "$CVERIFY/$CRAFT_NAME/scripts" ] \
  || { echo "FAIL craft bundle contains scripts/ — the verifier belongs to the runtime" >&2; exit 1; }
rm -rf "$CSTAGE" "$CVERIFY"
echo "    craft bundle verified"

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

if command -v shasum >/dev/null 2>&1; then
  ( cd "$OUT_DIR" && shasum -a 256 "$CRAFT_NAME.skill" > "$CRAFT_NAME.skill.sha256" )
elif command -v sha256sum >/dev/null 2>&1; then
  ( cd "$OUT_DIR" && sha256sum "$CRAFT_NAME.skill" > "$CRAFT_NAME.skill.sha256" )
fi
[ -f "$OUT_DIR/$CRAFT_NAME.skill.sha256" ] \
  && cat "$OUT_DIR/$CRAFT_NAME.skill.sha256" | sed 's/^/    /'

if [ "$UPDATE_ROOT" -eq 1 ]; then
  cp "$BUNDLE" "$REPO/$NAME.skill"
  cp "$CRAFT_BUNDLE" "$REPO/$CRAFT_NAME.skill"
  echo "    updated $REPO/$NAME.skill"
  echo "    updated $REPO/$CRAFT_NAME.skill"
fi

echo
echo "Built $NAME.skill        — $FILES files, $SIZE bytes."
echo "Built $CRAFT_NAME.skill — $CFILES files, $CSIZE bytes."
echo
echo "Install both. They are two halves of one system."
echo "Upload path: Claude → Settings → Capabilities → Skills → Upload skill"
