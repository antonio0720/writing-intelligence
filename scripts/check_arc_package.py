#!/usr/bin/env python3
"""Verify complete separately packaged v8 arc artifact, stdlib only."""
from pathlib import Path
import hashlib
import json
import re
import sys
ROOT=Path(__file__).resolve().parent.parent

def main():
    errors=[]
    catalog=json.loads((ROOT/'rules/arc_120_requirements.json').read_text(encoding='utf-8'))
    actual=[x['id'] for x in catalog['requirements']]
    expected=['B%03d'%i for i in range(1,61)]+['N%03d'%i for i in range(61,121)]
    if actual!=expected:errors.append('Require exact B001-B060 + N061-N120 order and identity')
    if catalog['count']!=120 or catalog['new_count']!=60 or catalog['carried_forward_count']!=60:
        errors.append('Requirement counts inconsistent')
    for item in catalog['requirements']:
        if item['id'].startswith('B') and item['implementation']!='existing_separate_zip_not_imported':
            errors.append('Prior ZIP B rule ownership incorrectly claimed: '+item['id'])
        if item['implementation'] not in ('existing_separate_zip_not_imported','partially_executable','specified_not_certified'):
            errors.append('Unknown maturity/status '+item['id'])
    m=json.loads((ROOT/'plans/v8-arc.proposal.json').read_text())
    if len(m['waves'])!=12 or any(x['status']!='planned' for x in m['waves']):errors.append('An upstream wave falsely presented as shipped')
    baseline=json.loads((ROOT/'provenance/ARC_BASELINE.json').read_text())
    if m['baseline']!=baseline['head_commit_sha']:errors.append('Baseline SHA mismatch')
    for schema in (ROOT/'schemas/v8').glob('arc_*.schema.json'):
        obj=json.loads(schema.read_text())
        if obj.get('$schema')!='https://json-schema.org/draft/2020-12/schema':errors.append('Unexpected schema draft '+schema.name)
    sums=ROOT/'ARC_SHA256SUMS.txt'
    if not sums.is_file():errors.append('Missing ARC_SHA256SUMS.txt')
    else:
        listed=set()
        for line in sums.read_text().splitlines():
            m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
            if not m:errors.append('Invalid checksum line');continue
            expected_hash,path=m.groups()
            if path in listed:errors.append('Repeated checksum entry '+path)
            listed.add(path)
            p=ROOT/path
            try:
                p.resolve().relative_to(ROOT.resolve())
                escaped = False
            except ValueError:
                escaped = True
            if p.is_symlink() or not p.is_file() or escaped:
                errors.append('Missing or escaped file '+path);continue
            if hashlib.sha256(p.read_bytes()).hexdigest()!=expected_hash:errors.append('Checksum mismatch '+path)
        actual_files={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='ARC_SHA256SUMS.txt'}
        if listed!=actual_files:
            errors.append('File-set mismatch: missing '+str(sorted(actual_files-listed))+' extra '+str(sorted(listed-actual_files)))
    if errors:
        for e in errors:print('FAIL',e,file=sys.stderr)
        return 2
    print('PASS: 120 indexed requirements, two-ZIP boundary, 12 planned waves, baseline, schemas and %d SHA256 files'%len(listed))
    return 0
if __name__=='__main__':sys.exit(main())
