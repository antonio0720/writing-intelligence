#!/usr/bin/env bash
#
# test-v9.sh — the v9 regression, runnable from the repository and
# from the extracted writing-intelligence-authorship bundle.
#
# Owner: Antonio T. Smith Jr. Stdlib only. Exits non-zero on any failure.
#
# The meaning-led doctrine scan reads the craft library, which ships in a
# different bundle. Where that library is absent the scan is skipped by name,
# never counted as a pass: a scan of nothing proves nothing.
set -u
cd "$(dirname "${BASH_SOURCE[0]}")/.."
fails=0
run() {
  local label="$1"; shift
  if out=$("$@" 2>&1) && echo "$out" | grep -Eq '^Ran [1-9][0-9]* test'; then
    echo "PASS $label ($(echo "$out" | grep -E '^Ran ' | tail -1))"
  else
    echo "$out" | tail -20
    echo "FAIL $label"
    fails=$((fails + 1))
  fi
}
run "authorship checker" python3 -m unittest discover -s tests/v9 -p 'test_authorship*.py'
run "schema parity" python3 -m unittest discover -s tests/v9 -p 'test_schema_parity.py'
run "skill frontmatter limits" python3 -m unittest discover -s tests/v9 -p 'test_skill_frontmatter.py'
run "wi authorship subcommand" python3 -m unittest discover -s tests/v9 -p 'test_wi_subcommand.py'
run "no shipped voice corpus" python3 -m unittest discover -s tests/v9 -p 'test_no_shipped_voice_corpus.py'
run "platform refusal without POSIX file safety" python3 -m unittest discover -s tests/v9 -p 'test_platform_refusal.py'
run "reference kernel" python3 -m unittest discover -s prototypes/wi9/tests -p 'test_*.py'
if [ -d references/anti_patterns ]; then
  run "meaning-led doctrine" python3 -m unittest discover -s tests/v9 -p 'test_doctrine_meaning_led.py'
else
  echo "SKIP meaning-led doctrine — the craft library is not in this artifact; it runs in the repository"
fi
if [ "$fails" -ne 0 ]; then
  echo "v9 regression: $fails failed"
  exit 1
fi
echo "v9 regression complete"
