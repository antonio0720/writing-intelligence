#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 -m unittest discover -s tests/v8 -p 'test_*.py' -v
python3 scripts/wi-fiction.py validate --input tests/v8/fixtures/valid_draft.json >/dev/null
set +e
python3 scripts/wi-fiction.py gate --input tests/v8/fixtures/forbidden_power.json >/dev/null
code=$?
set -e
if [ "$code" -ne 2 ]; then echo "NEGATIVE CONTROL FAILED: forbidden power exit=$code"; exit 1; fi
set +e
python3 scripts/wi-fiction.py gate --input tests/v8/fixtures/valid_draft.json --mode publication >/dev/null
code=$?
set -e
if [ "$code" -ne 3 ]; then echo "NEGATIVE CONTROL FAILED: publication without readers exit=$code"; exit 1; fi
echo 'PASS: unit tests and negative controls'
