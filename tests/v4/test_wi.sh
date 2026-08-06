#!/usr/bin/env bash
#
# Regression suite for scripts/wi.py.
#
# The fixture is adversarial on purpose. narrative.md contains:
#   - an inflated figure      (12,400 households; the source says 11,800)
#   - a reshaped quotation    (not verbatim in any source)
#   - a fabricated citation   (Whitfield and Barnes 2021 — resolves to nothing)
#   - an author assertion     (our own operating history; not an external fact)
# and sources/needs_assessment.txt carries a prompt injection plus zero-width
# characters.
#
# Expected verdict: BLOCK.
#
# Exits non-zero if any check fails. A test that always exits 0 is not a test.

set -u
cd "$(dirname "$0")"

WI="../../scripts/wi.py"
LEDGER="$(mktemp -t wi-test.XXXXXX.json 2>/dev/null || echo /tmp/wi-test.$$.json)"
trap 'rm -f "$LEDGER"' EXIT

fails=0
pass() { echo "PASS $1"; }
fail() { echo "FAIL $1"; fails=$((fails + 1)); }

# 1. Law F — the injection in the supplied source is detected and quarantined.
if python3 "$WI" scan-sources sources/ 2>/dev/null | grep -q "QUARANTINE"; then
  pass "injection detected"
else
  fail "injection detected — scan-sources did not quarantine the poisoned source"
fi

# 2. The pipeline runs end to end.
if ! python3 "$WI" extract-claims narrative.md --out "$LEDGER" >/dev/null 2>&1; then
  fail "extract-claims — pipeline aborted"
elif ! python3 "$WI" verify "$LEDGER" sources/ >/dev/null 2>&1; then
  fail "verify — pipeline aborted"
else
  # 3. Law D/E — a fabricated citation must block, not merely hold.
  python3 "$WI" gate "$LEDGER" --mode strict --exit-code >/dev/null 2>&1
  code=$?
  if [ "$code" -eq 2 ]; then
    pass "gate BLOCK"
  else
    fail "gate BLOCK — expected exit 2 (BLOCK), got $code"
  fi

  # 4. The statuses that matter are all reachable on one document.
  if python3 - "$LEDGER" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
got = {c["status"] for c in d["claims"]}
need = {"unsafe", "conflicted", "author_asserted"}
sys.exit(0 if need <= got else 1)
PY
  then
    pass "statuses"
  else
    fail "statuses — expected unsafe, conflicted and author_asserted to all appear"
  fi
fi

if [ "$fails" -ne 0 ]; then
  echo
  echo "$fails check(s) failed. The deterministic tier is not doing its job;"
  echo "do not trust its verdicts until this passes."
  exit 1
fi
exit 0
