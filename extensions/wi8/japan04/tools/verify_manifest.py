#!/usr/bin/env python3
"""Self-audit for the independent Japan proposal package, not upstream release."""
from pathlib import Path
import csv
import json
import sys

ROOT=Path(__file__).resolve().parents[1]

def verify():
    errors=[]
    reg=json.loads((ROOT/'references/JAPAN_REQUIREMENTS_181_340.json').read_text())
    ids=[r['id'] for r in reg.get('requirements',[])]
    if ids!=list(range(181,341)):errors.append('requirement IDs are not continuous JP-181..JP-340')
    if len(set(ids))!=160:errors.append('duplicate requirements')
    for r in reg.get('requirements',[]):
        if not all(k in r for k in ('id','id_code','category','title','requirement','acceptance','implementation_state')):
            errors.append('missing requirement fields: '+str(r.get('id')))
        if r.get('upstream_integrated') or r.get('acceptance_fully_verified'):
            errors.append('unearned accepted/upstream status: '+str(r.get('id')))
    waves=json.loads((ROOT/'plans/japan04_waves.json').read_text())
    if [w['id'] for w in waves.get('waves',[])]!=[f'WI8-{i:02d}' for i in range(24,44)]:errors.append('wave IDs invalid')
    for w in waves.get('waves',[]):
        if w['status']!='planned':errors.append('unearned shipped status '+w['id'])
        if not w.get('exit') or not w.get('negative_control'):errors.append('wave lacks falsifiable exit '+w['id'])
    if not (ROOT/'references/SOURCE_PIN.json').is_file():errors.append('missing source pin')
    if json.loads((ROOT/'fixtures/proposed_seed_catalog.json').read_text())['status']!='PROPOSED_NOT_ADOPTED':errors.append('unearned seed adoption')
    print(json.dumps({'status':'PASS' if not errors else 'FAIL','requirements':len(ids),'waves':len(waves.get('waves',[])),
                      'upstream_waves_shipped':0,'errors':errors},indent=2))
    return 0 if not errors else 1
if __name__=='__main__':raise SystemExit(verify())
