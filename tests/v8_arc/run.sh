#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/v8_arc -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 scripts/wi-arc.py validate --input tests/v8_arc/fixtures/four_quadrants.json >/dev/null
if PYTHONDONTWRITEBYTECODE=1 python3 scripts/wi-arc.py validate --input tests/v8_arc/fixtures/dangling.json >/dev/null; then
  echo 'FAIL: dangling negative control was accepted' >&2; exit 1
fi
if PYTHONDONTWRITEBYTECODE=1 python3 scripts/wi-arc.py gate --input tests/v8_arc/fixtures/four_quadrants.json --stage publication >/dev/null; then
  echo 'FAIL: publication falsely certified' >&2; exit 1
fi
echo 'PASS: positive control, negative control, and publication hold'
