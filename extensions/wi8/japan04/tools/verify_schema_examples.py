#!/usr/bin/env python3
"""Optional external jsonschema validation; runtime itself has no pip deps."""
import json
import sys
from pathlib import Path
try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit('jsonschema optional package missing; Python runtime remains stdlib only')
ROOT=Path(__file__).resolve().parents[1]
files=sorted((ROOT/'schemas').glob('*.schema.json'))
for s in files:Draft202012Validator.check_schema(json.loads(s.read_text()))
schema=json.loads((ROOT/'schemas/projection_japan.schema.json').read_text())
project=json.loads((ROOT/'fixtures/sample_project.json').read_text())
Draft202012Validator(schema).validate(project)
from sys import path
sys.path.insert(0,str(ROOT/'src'))
from japan_story_os.analysis import analyze
report=analyze(project)
Draft202012Validator(json.loads((ROOT/'schemas/report_japan.schema.json').read_text())).validate(report)
print(json.dumps({'status':'PASS','schemas':len(files),'projection_valid':True,'report_valid':True},indent=2))
