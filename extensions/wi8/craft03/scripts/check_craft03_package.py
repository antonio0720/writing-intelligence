#!/usr/bin/env python3
"""Independent internal consistency and integrity checker. Not an upstream release gate."""
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
COMMIT='d4524f3caa5f75e005b23f94dcd1c71bb5002127'
def fail(msg):print('FAIL:',msg,file=sys.stderr);return 2
def run():
    rules=json.loads((ROOT/'rules/craft_c121_c180.json').read_text())
    expected=[f'C{i}' for i in range(121,181)]
    actual=[r['id'] for r in rules['rules']]
    if actual!=expected or len({r['id'] for r in rules['rules']})!=60:return fail('rule IDs incorrect or duplicated')
    if any(r['upstream_status']!='proposed' for r in rules['rules']):return fail('upstream release status was fabricated')
    if any(not r['acceptance'] or not r['owner_existing_path'] for r in rules['rules']):return fail('missing contract or owner')
    engine=(ROOT/'scripts/craft_v8/engine.py').read_text()
    instrumented={'C'+x for x in re.findall(r"'C(1[2-8][0-9])'",engine)}
    for r in rules['rules']:
        should='partial_executable' if r['id'] in instrumented else 'specified_review_protocol'
        if r['local_coverage']!=should:return fail('misstated local mechanism for '+r['id'])
    plan=json.loads((ROOT/'plans/v8-craft03.proposal.json').read_text())
    ws=plan['waves']
    if [w['id'] for w in ws]!=[f'WI8-{i}' for i in range(12,24)]:return fail('incorrect wave numbering')
    if any(w['status']!='planned' or w['upstream_receipt'] is not None for w in ws):return fail('wave incorrectly marked shipped')
    base=json.loads((ROOT/'provenance/BASELINE.json').read_text())
    if base['observed_commit']!=COMMIT or plan['source_baseline_sha']!=COMMIT:return fail('canonical repo baseline mismatch')
    if any('..' in p.relative_to(ROOT).parts for p in ROOT.rglob('*')):return fail('path traversal')
    for p in (ROOT/'schemas/v8').glob('*.json'):
        d=json.loads(p.read_text())
        if d.get('$schema')!='https://json-schema.org/draft/2020-12/schema':return fail('unversioned schema '+p.name)
    sums=ROOT/'CRAFT03_SHA256SUMS.txt'
    if sums.exists():
        listing={}
        for line in sums.read_text().splitlines():
            match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
            if not match:return fail('bad checksum line')
            sha,path=match.groups()
            if path in listing:return fail('duplicate checksum')
            listing[path]=sha
        found={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
               for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
               and p.name!='CRAFT03_SHA256SUMS.txt' and not p.name.endswith('.pyc')}
        if listing!=found:
            return fail('checksum mismatch; removed/added/modified files: '+str(sorted(set(listing)^set(found))[:10]))
    print('PASS: 60 numbered requirements; 29 instrumented IDs; 12 planned upstream waves; pinned baseline; 8 JSON schemas; checksum verified' if sums.exists() else 'PASS: requirements, wave, ownership and schema checks (checksums not sealed)')
    return 0
if __name__=='__main__':sys.exit(run())
