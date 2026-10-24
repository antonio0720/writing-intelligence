#!/usr/bin/env python3
"""Optional external JSON Schema 2020-12 cross-file validator (requires jsonschema).
Does not add a dependency to the production analyzer."""
import json,sys
from pathlib import Path
try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError as exc:
    print('SCHEMA TOOL NOT INSTALLED: pip install jsonschema referencing',file=sys.stderr)
    sys.exit(3)
ROOT=Path(__file__).resolve().parent.parent
folder=ROOT/'schemas/v8'
store={}
for p in sorted(folder.glob('*.json')):
    d=json.loads(p.read_text());Draft202012Validator.check_schema(d)
    store[d['$id']]=d
reg=Registry()
for url,d in store.items():reg=reg.with_resource(url,Resource.from_contents(d))
main=store['https://writing-intelligence.dev/schemas/v8/craft_projection.schema.json']
validator=Draft202012Validator(main,registry=reg,format_checker=Draft202012Validator.FORMAT_CHECKER)
for p in sorted((ROOT/'tests/v8_craft/fixtures').glob('*.json')):
    sample=json.loads(p.read_text());errors=list(validator.iter_errors(sample))
    if errors:
        for e in errors[:4]:print('FAIL',p.name,':',e.message,file=sys.stderr)
        sys.exit(2)
print('PASS: 8 Draft 2020-12 schemas and',len(list((ROOT/'tests/v8_craft/fixtures').glob('*.json'))),'fixtures')
