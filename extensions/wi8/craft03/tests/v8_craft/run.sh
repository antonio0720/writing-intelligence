#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 -m unittest discover -s tests/v8_craft -p 'test_*.py' -v
python3 scripts/check_craft03_package.py
