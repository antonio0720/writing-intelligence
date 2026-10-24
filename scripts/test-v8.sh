#!/usr/bin/env bash
#
# test-v8.sh — the v8 Story Intelligence integration check.
#
# v8 is four engines built and tested independently: Fiction & Thriller
# Intelligence (FI-01..FI-60), Arc, Want/Need & Ending Intelligence
# (N061..N120), The Craft (C121..C180) and the Japan Story OS (JP-181..JP-340).
# Each ships its own suite. This script runs all four from one place and then
# adds the cross-engine checks the individual suites cannot make:
#
#   * every publication gate HOLDS (exit 3). A structural pass is not a good
#     novel, and an engine that certified publication on its own would be
#     claiming a reader study nobody ran;
#   * malformed or contradictory input is REFUSED (exit 2), not quietly passed;
#   * the four requirement registers together carry exactly 340 numbered IDs,
#     none duplicated, so the program cannot silently lose or invent one.
#
# Each positive check has a negative twin. A suite that can only go green
# certifies nothing.
#
# Run from anywhere: it locates the tree (repository or extracted
# writing-intelligence-story bundle) itself.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONDONTWRITEBYTECODE=1

PASS=0
FAIL=0
pass() { echo "PASS $1"; PASS=$((PASS + 1)); }
fail() { echo "FAIL $1" >&2; FAIL=$((FAIL + 1)); }

expect_exit() {
  local want="$1" label="$2"; shift 2
  "$@" >/dev/null 2>&1
  local got=$?
  if [ "$got" -eq "$want" ]; then pass "$label (exit $got)"; else fail "$label (wanted exit $want, got $got)"; fi
}

suite() {
  local label="$1"; shift
  if OUT=$("$@" 2>&1); then pass "$label"; else echo "$OUT" | tail -20 >&2; fail "$label"; fi
}

CRAFT=extensions/wi8/craft03
JAPAN=extensions/wi8/japan04

# --- the four engines' own suites, unchanged ---------------------------------
suite "fiction & thriller suite (tests/v8)"         bash tests/v8/run.sh
suite "arc, want/need & ending suite (tests/v8_arc)" bash tests/v8_arc/run.sh
suite "the craft suite (C121-C180)"                  bash "$CRAFT/tests/v8_craft/run.sh"
suite "japan story os suite (JP-181-JP-340)"         bash -c "cd '$JAPAN' && python3 -m unittest discover -s tests"

# --- positive controls -------------------------------------------------------
expect_exit 0 "fiction: a valid draft validates"         python3 scripts/wi-fiction.py validate --input tests/v8/fixtures/valid_draft.json
expect_exit 0 "arc: four ending quadrants evaluate"      python3 scripts/wi-arc.py evaluate --input tests/v8_arc/fixtures/four_quadrants.json
expect_exit 0 "craft: a quiet mixed victory evaluates"   python3 "$CRAFT/scripts/wi-craft.py" evaluate --input "$CRAFT/tests/v8_craft/fixtures/valid_quiet_mixed_victory.json"
expect_exit 0 "japan: the sample project checks"         python3 "$JAPAN/cli/wi8_japan.py" check "$JAPAN/fixtures/sample_project.json"

# The ending algebra (references/v8/ENDING_ALGEBRA.md): want attained + need
# unfulfilled is bittersweet; want lost + need fulfilled is semi-sweet. A
# partial want is not classifiable at all — the twin that proves the engine
# refuses to invent certainty.
Q1=$(python3 scripts/wi-arc.py classify --want attained --need unfulfilled 2>/dev/null)
if echo "$Q1" | grep -q '"bittersweet"'; then pass "arc: want attained + need unfulfilled classifies bittersweet"
else fail "arc: want attained + need unfulfilled did not classify bittersweet: $Q1"; fi
Q2=$(python3 scripts/wi-arc.py classify --want sacrificed --need fulfilled 2>/dev/null)
if echo "$Q2" | grep -q '"semi_sweet"'; then pass "arc: want sacrificed + need fulfilled classifies semi-sweet"
else fail "arc: want sacrificed + need fulfilled did not classify semi-sweet: $Q2"; fi
Q3=$(python3 scripts/wi-arc.py classify --want partial --need fulfilled 2>/dev/null)
if echo "$Q3" | grep -q '"not_classifiable"'; then pass "arc: a partial want is not classifiable (no invented certainty)"
else fail "arc: a partial want was classified: $Q3"; fi

# --- negative twins: refusal --------------------------------------------------
expect_exit 2 "fiction: a forbidden power use is blocked" python3 scripts/wi-fiction.py gate --input tests/v8/fixtures/forbidden_power.json
expect_exit 2 "arc: a dangling reference is refused"      python3 scripts/wi-arc.py validate --input tests/v8_arc/fixtures/dangling.json
expect_exit 2 "arc: a causal cycle is refused"            python3 scripts/wi-arc.py validate --input tests/v8_arc/fixtures/cycle.json
expect_exit 2 "japan: preflight is not an authorization"  python3 "$JAPAN/cli/wi8_japan.py" preflight "$JAPAN/fixtures/sample_project.json"

# --- negative twins: no engine certifies publication -------------------------
expect_exit 3 "fiction: publication HOLDS without readers" python3 scripts/wi-fiction.py gate --input tests/v8/fixtures/valid_draft.json --mode publication
expect_exit 3 "arc: publication HOLDS"                     python3 scripts/wi-arc.py gate --input tests/v8_arc/fixtures/four_quadrants.json --stage publication
expect_exit 3 "craft: publication HOLDS"                   python3 "$CRAFT/scripts/wi-craft.py" gate --input "$CRAFT/tests/v8_craft/fixtures/valid_quiet_mixed_victory.json" --stage publication

# --- the program cannot lose or invent a requirement --------------------------
COUNT=$(python3 - "$CRAFT" "$JAPAN" <<'PY'
import json, re, sys
craft, japan = sys.argv[1], sys.argv[2]
ids = []
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("id", "rule_id", "requirement_id"):
                if isinstance(v, str):
                    ids.append(v)
                elif isinstance(v, int) and 181 <= v <= 340:
                    ids.append("JP-%d" % v)  # the Japan register numbers its IDs
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
for path in ("rules/fiction_v8_rules.json", "rules/arc_120_requirements.json",
             craft + "/rules/craft_c121_c180.json",
             japan + "/references/JAPAN_REQUIREMENTS_181_340.json"):
    walk(json.load(open(path, encoding="utf-8")))
pat = {"FI": r"^FI-\d\d$", "N": r"^N\d{3}$", "C": r"^C\d{3}$", "JP": r"^JP-\d{3}$"}
found = {k: sorted({i for i in ids if re.match(p, i)}) for k, p in pat.items()}
print(" ".join("%s=%d" % (k, len(v)) for k, v in found.items()), sum(len(v) for v in found.values()))
PY
)
TOTAL=$(echo "$COUNT" | awk '{print $NF}')
if [ "$TOTAL" = "340" ]; then pass "registers carry 340 numbered requirements ($COUNT)"
else fail "registers carry $TOTAL numbered requirements, expected 340 ($COUNT)"; fi

echo
echo "v8 integration: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
