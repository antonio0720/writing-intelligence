#!/usr/bin/env bash
#
# test_wi7.sh — the v7 regression suite.
#
# v7.0.0 ships governance, not a new domain capability, so this suite tests the
# two things v7.0.0 claims: the doctrine no longer instructs detector evasion,
# and the program manifest cannot be marked shipped without a receipt behind it.
# Every positive check has a negative twin that must go red: an evasion
# instruction planted back is caught, and a wave marked shipped on a missing,
# failed, incomplete or dependency-violating receipt is refused.
#
# Stdlib only. Runs from the repository and from an extracted bundle.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/../.."
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
fails=0
pass() { echo "PASS $1"; }
fail() { echo "FAIL $1"; fails=$((fails + 1)); }

# --- Doctrine: no instruction to evade detection or fake authorship ----------
cat > "$TMP/scan.py" <<'PY'
import sys
from pathlib import Path
FORBIDDEN = (
    "anti-detection specifics",
    "maximum undetectability",
    "no detector can flag",
    "could only come from attending the class",
    "imperfect transitions",
    "anti-detection rules",
    "anti-detection adversarial",
    "highest-leverage anti-detection",
    "perfect certainty is a tell",
)
roots = [Path(a) for a in sys.argv[1:]]
files = []
for r in roots:
    if r.is_file():
        files.append(r)
    elif r.is_dir():
        files.extend(sorted(r.rglob("*.md")))
if not files:
    print("scanned 0 files; a scan of nothing is not a pass")
    sys.exit(2)
hits = []
for f in files:
    low = f.read_text(encoding="utf-8", errors="replace").lower()
    for phrase in FORBIDDEN:
        if phrase in low:
            hits.append("%s: %s" % (f, phrase))
print("scanned %d file(s), %d forbidden instruction(s)" % (len(files), len(hits)))
for h in hits:
    print("  " + h)
sys.exit(1 if hits else 0)
PY
SCAN_ROOTS="SKILL.md references packs"
if python3 "$TMP/scan.py" $SCAN_ROOTS > "$TMP/scan.out"; then
  pass "doctrine carries no detector-evasion instruction ($(head -1 "$TMP/scan.out"))"
else
  cat "$TMP/scan.out"; fail "doctrine still instructs detector evasion"
fi

printf '## Anti-Detection Specifics\nImperfect transitions: one per paper.\n' > "$TMP/planted.md"
if python3 "$TMP/scan.py" "$TMP/planted.md" >/dev/null; then
  fail "a planted evasion instruction was not caught"
else
  pass "a planted evasion instruction is caught"
fi

# --- Program manifest: shipped means a receipt reads PASS --------------------
if python3 scripts/check-manifest.py > "$TMP/m.out" 2>&1; then
  pass "every plans/*.manifest.yaml validates"
else
  cat "$TMP/m.out"; fail "a manifest does not validate"
fi

grep -q "^receipts_required: true" plans/v7.manifest.yaml \
  && pass "the v7 manifest requires receipts" \
  || fail "the v7 manifest does not require receipts"

expect_refused() {  # $1 label, $2 manifest
  if python3 scripts/check-manifest.py "$2" > "$TMP/neg.out" 2>&1; then
    fail "$1 was accepted"
  else
    pass "$1 is refused"
  fi
}

sed 's#receipt: plans/receipts/WI7-02.json#receipt: plans/receipts/does-not-exist.json#' \
  plans/v7.manifest.yaml > "$TMP/missing.yaml"
expect_refused "a shipped wave whose receipt does not exist" "$TMP/missing.yaml"

python3 - "$TMP" <<'PY'
import json, sys
from pathlib import Path
tmp = Path(sys.argv[1])
base = json.loads(Path("plans/receipts/WI7-02.json").read_text())
failed = dict(base, status="FAIL")
(tmp / "failed.json").write_text(json.dumps(failed))
nocontrol = dict(base, negative_controls=[])
(tmp / "nocontrol.json").write_text(json.dumps(nocontrol))
noreadback = dict(base, independent_readback=None)
(tmp / "noreadback.json").write_text(json.dumps(noreadback))
other = dict(base, checkpoint="WI7-01")
(tmp / "other.json").write_text(json.dumps(other))
PY
for case in failed nocontrol noreadback other; do
  sed "s#receipt: plans/receipts/WI7-02.json#receipt: $TMP/$case.json#" \
    plans/v7.manifest.yaml > "$TMP/$case.yaml"
done
expect_refused "a shipped wave whose receipt reads FAIL" "$TMP/failed.yaml"
expect_refused "a receipt with no negative control" "$TMP/nocontrol.yaml"
expect_refused "a receipt with no independent readback" "$TMP/noreadback.yaml"
expect_refused "a receipt that belongs to another wave" "$TMP/other.yaml"

python3 - "$TMP" <<'PY'
import sys
from pathlib import Path
s = Path("plans/v7.manifest.yaml").read_text()
s = s.replace("  - id: WI7-04\n    name: Security and privacy foundation — tenant, matter, academic, deal and bid isolation\n    status: planned",
              "  - id: WI7-04\n    name: Security and privacy foundation — tenant, matter, academic, deal and bid isolation\n    status: shipped\n    receipt: plans/receipts/WI7-02.json", 1)
Path(sys.argv[1], "early.yaml").write_text(s)
PY
expect_refused "a wave shipped before its dependency" "$TMP/early.yaml"

# --- One version, one description inside the loader's limit -----------------
V=$(python3 scripts/wi.py --version | awk '{print $2}')
# The CLI, SKILL.md and the NEWEST program manifest must name one version.
# Since v8 the newest manifest is plans/v8.manifest.yaml; the v7 manifest keeps
# the core_version it shipped with (7.0.0), which may never exceed the CLI.
LATEST=$(ls plans/v*.manifest.yaml | sort -V | tail -1)
V7CORE=$(awk '/^core_version:/{print $2}' plans/v7.manifest.yaml)
grep -q "^\*\*Version:\*\* $V" SKILL.md && grep -q "^core_version: $V" "$LATEST" \
  && [ "$(printf '%s\n%s\n' "$V7CORE" "$V" | sort -V | tail -1)" = "$V" ] \
  && pass "CLI, SKILL.md and the newest manifest ($LATEST) agree on $V" \
  || fail "version disagreement ($V)"

python3 - <<'PY' && pass "SKILL.md description is inside the 1024-character limit" || fail "SKILL.md description exceeds 1024 characters"
import re, sys
src = open("SKILL.md", encoding="utf-8").read()
fm = src[4:src.find("\n---", 4)]
d = re.search(r"^description:[ \t]+(.*)$", fm, re.M).group(1).strip().strip("'\"")
sys.exit(0 if len(d) <= 1024 else 1)
PY

echo
if [ "$fails" -ne 0 ]; then echo "v7 regression FAILED ($fails)"; exit 1; fi
echo "v7 regression complete"
