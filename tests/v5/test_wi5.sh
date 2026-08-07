#!/usr/bin/env bash
#
# test_wi5.sh — regression suite for the v5 proof-carrying core.
#
# Every assertion here has a negative twin. A suite that can only pass tells
# you nothing: if the implementation were disabled, most naive tests would
# still print PASS because nothing would object. So this file checks both that
# the good case is accepted AND that the tampered, stale and contradicted cases
# are rejected, for the correct reason.
#
# stdlib Python only. No network. Runs in a temp directory and cleans up.
#
# Usage: bash tests/v5/test_wi5.sh
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
WI="python3 $REPO/scripts/wi.py"

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT
cp -R "$HERE/world/." "$WORK/"
cd "$WORK"

FAILED=0
ok()   { echo "PASS $1"; }
bad()  { echo "FAIL $1"; [ -n "${2:-}" ] && echo "     $2"; FAILED=1; }
check(){ if [ "$2" = "$3" ]; then ok "$1"; else bad "$1" "expected [$3], got [$2]"; fi; }

# --------------------------------------------------------------------------
# 1. Workspace, ingestion, content addressing
# --------------------------------------------------------------------------
$WI init --title "Delta" --mode strict >/dev/null 2>&1
[ -f .wi/workspace.db ] && ok "workspace created" || bad "workspace created"

$WI ingest sources/ > ingest.txt 2>&1
grep -q "2 readable" ingest.txt && ok "sources ingested" || bad "sources ingested" "$(cat ingest.txt)"

# The same bytes must always produce the same digest, or nothing downstream
# means anything.
D1=$($WI ingest sources/outcomes_report.txt 2>/dev/null | grep outcomes | awk '{print $2}')
D2=$($WI ingest sources/outcomes_report.txt 2>/dev/null | grep outcomes | awk '{print $2}')
check "source digest is stable" "$D1" "$D2"

# --------------------------------------------------------------------------
# 2. Atomization — a compound sentence becomes independent claims
# --------------------------------------------------------------------------
$WI atomize drafts/report.md > atom.txt 2>&1
LEDGER=$(ls .wi/graph/ledger-*.json | head -1)
[ -f "$LEDGER" ] && ok "claim ledger written" || bad "claim ledger written"
SPLIT=$(grep -c "came from splitting" atom.txt)
check "compound sentence split into atoms" "$SPLIT" "1"

# --------------------------------------------------------------------------
# 3. Anchoring — every claim points at an inspectable span
# --------------------------------------------------------------------------
$WI anchor "$LEDGER" sources/ > anchor.txt 2>&1
grep -q "evidence anchor(s) bound" anchor.txt && ok "evidence anchors bound" \
  || bad "evidence anchors bound" "$(cat anchor.txt)"
# Law C: the report must name what it did NOT do.
grep -q "paraphrase entailment" anchor.txt && ok "unrun checks are named" \
  || bad "unrun checks are named"

# --------------------------------------------------------------------------
# 4. The clean draft releases at strict
# --------------------------------------------------------------------------
$WI gate "$LEDGER" --mode strict --exit-code >/dev/null 2>&1
check "clean draft releases at strict" "$?" "0"

# --------------------------------------------------------------------------
# 5. Semantic diff — the edit that changes meaning is named, not just shown
# --------------------------------------------------------------------------
$WI diff drafts/report.md drafts/report-v2.md --semantic > diff.txt 2>&1
grep -q "certainty_strengthened" diff.txt && ok "may -> reduces classified" \
  || bad "may -> reduces classified" "$(cat diff.txt)"
grep -q "quantity_changed" diff.txt && ok "11,800 -> 12,400 classified" \
  || bad "11,800 -> 12,400 classified"
grep -q "does not carry forward" diff.txt && ok "proof impact reported" \
  || bad "proof impact reported"
# The negative twin: an unchanged sentence must NOT be reported as a change.
UNCHANGED=$(grep -c "^PROOF   unaffected" diff.txt)
[ "$UNCHANGED" -ge 3 ] && ok "unchanged sentences left alone" \
  || bad "unchanged sentences left alone" "only $UNCHANGED reported unaffected"

# --------------------------------------------------------------------------
# 6. Writing tests
# --------------------------------------------------------------------------
$WI test > test.txt 2>&1
grep -q "every_sourced_claim_has_support" test.txt && ok "writing tests run" \
  || bad "writing tests run" "$(cat test.txt)"
grep -q "of .* required claim atoms" test.txt && ok "coverage reports a denominator" \
  || bad "coverage reports a denominator"

# --------------------------------------------------------------------------
# 7. Proof-carrying release: build, verify, and reject a tampered copy
# --------------------------------------------------------------------------
$WI bundle out/delta.wiab --artifact drafts/report.md --mode strict >/dev/null 2>&1
[ -f out/delta.wiab ] && ok "release bundle built" || bad "release bundle built"

# Reproducible: the published checksum is meaningless otherwise.
$WI bundle out/delta-2.wiab --artifact drafts/report.md --mode strict >/dev/null 2>&1
A=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open('out/delta.wiab','rb').read()).hexdigest())")
B=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open('out/delta-2.wiab','rb').read()).hexdigest())")
check "bundle build is reproducible" "$A" "$B"

$WI verify-release out/delta.wiab >/dev/null 2>&1
check "intact bundle verifies offline" "$?" "0"

# The negative twin. Swap the figure inside the sealed artifact and nothing
# else. A verifier that cannot catch this is decoration.
python3 - <<'PY'
import zipfile
src = zipfile.ZipFile("out/delta.wiab")
with zipfile.ZipFile("out/tampered.wiab", "w") as out:
    for info in src.infolist():
        data = src.read(info.filename)
        if info.filename.startswith("artifact/"):
            data = data.replace(b"11,800", b"12,400")
        out.writestr(info, data)
src.close()
PY
$WI verify-release out/tampered.wiab > tamper.txt 2>&1
check "tampered bundle is rejected" "$?" "2"
grep -q "FAIL  release.artifact_digest" tamper.txt \
  && ok "tamper rejected for the right reason" \
  || bad "tamper rejected for the right reason" "$(cat tamper.txt)"

# --------------------------------------------------------------------------
# 8. Staleness — the whole point of v5
# --------------------------------------------------------------------------
sed -i.bak 's/11,800 households/11,240 households/' sources/outcomes_report.txt
rm -f sources/outcomes_report.txt.bak
$WI impact sources/outcomes_report.txt --apply > impact.txt 2>&1

grep -q "1  claim atom" impact.txt && ok "exactly one claim atom invalidated" \
  || bad "exactly one claim atom invalidated" "$(cat impact.txt)"
grep -qE "4  evidence anchor\(s\) provably outside" impact.txt \
  && ok "unaffected anchors reported as unaffected" \
  || bad "unaffected anchors reported as unaffected" "$(cat impact.txt)"
grep -q "Cheapest safe repair" impact.txt && ok "repair path named" \
  || bad "repair path named"

$WI gate "$LEDGER" --mode strict --exit-code >/dev/null 2>&1
check "stale source holds the gate" "$?" "1"

# --------------------------------------------------------------------------
# 8b. The concept registry catches drift — and its negative twin
# --------------------------------------------------------------------------
$WI test --tests wi.tests.yaml > ctest.txt 2>&1
grep -q "PASS  households_figure_does_not_drift" ctest.txt \
  && ok "concept registry accepts the governing figure" \
  || bad "concept registry accepts the governing figure" "$(cat ctest.txt)"
grep -q "SKIP" ctest.txt || true

# Point the same test at the drafted-wrong file. It must fail, because the
# forbidden alias 12,400 is there. A registry that cannot fail is decoration.
sed 's|drafts/report.md|drafts/report-v2.md|' wi.tests.yaml > wi.tests.drift.yaml
$WI test --tests wi.tests.drift.yaml > drift.txt 2>&1
check "concept drift is caught" "$?" "1"
grep -q "forbidden alias" drift.txt && ok "drift names the forbidden alias" \
  || bad "drift names the forbidden alias" "$(cat drift.txt)"

# --------------------------------------------------------------------------
# 8c. Lockfile and bundle profiles
# --------------------------------------------------------------------------
[ -f wi.lock ] && ok "wi.lock written" || bad "wi.lock written"
python3 -c "import json;d=json.load(open('wi.lock'));assert d['core']['version'];assert d['sources']" \
  && ok "wi.lock pins core and sources" || bad "wi.lock pins core and sources"

$WI bundle out/redacted.wiab --artifact drafts/report.md --profile redacted \
  --mode strict --allow-block >/dev/null 2>&1
python3 -c "
import zipfile,sys
n=zipfile.ZipFile('out/redacted.wiab').namelist()
sys.exit(0 if 'evidence/excerpts.jsonl' in n and not any(x.startswith('sources/blobs/') for x in n) else 1)"
check "redacted bundle ships excerpts, not sources" "$?" "0"

$WI bundle out/full.wiab --artifact drafts/report.md --profile full \
  --mode strict --allow-block >/dev/null 2>&1
python3 -c "
import zipfile,sys
n=zipfile.ZipFile('out/full.wiab').namelist()
sys.exit(0 if any(x.startswith('sources/blobs/') for x in n) else 1)"
check "full bundle ships source bytes" "$?" "0"

# --------------------------------------------------------------------------
# 9. Capability honesty (Law C as protocol)
# --------------------------------------------------------------------------
$WI doctor > doctor.txt 2>&1
grep -q "never reported as done" doctor.txt && ok "doctor states what is unavailable" \
  || bad "doctor states what is unavailable"
grep -q "pdf_region" doctor.txt && ok "unimplemented anchors declared missing" \
  || bad "unimplemented anchors declared missing"

echo
if [ "$FAILED" -ne 0 ]; then
  echo "v5 regression FAILED"
  exit 1
fi
echo "v5 regression complete"
