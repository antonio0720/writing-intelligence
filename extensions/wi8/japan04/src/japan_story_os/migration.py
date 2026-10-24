"""Non-destructive Japan v1 identifier migration and field compatibility plan."""
from __future__ import annotations
import hashlib
import json
import re
from .contracts import ContractError

PREFIXES={'CID::':'legacy.canon','CHAR::':'legacy.character','LOC::':'legacy.location','TECH::':'legacy.technique','NAME::':'legacy.name'}

def normalize_legacy_id(raw):
    if not isinstance(raw,str) or not raw.strip():raise ContractError('ID empty')
    kind=next((v for k,v in PREFIXES.items() if raw.startswith(k)),None)
    if not kind:raise ContractError('unknown legacy ID prefix')
    # Exact old spelling stays separately present. Digest is stable and does not merge case variants.
    return {'logical_alias':'jp04:'+hashlib.sha256(raw.encode('utf-8')).hexdigest()[:32],
            'legacy_id':raw,'legacy_family':kind}

def migrate_legacy(records, *, mode='preview'):
    if mode!='preview':raise ContractError('canonical migration not possible in standalone runtime')
    if not isinstance(records,list):raise ContractError('records array required')
    changed=[];aliases=set();sources=set()
    for rec in records:
        if not isinstance(rec,dict) or not isinstance(rec.get('cid'),str):raise ContractError('record must carry original cid')
        result=normalize_legacy_id(rec['cid']);alias=result['logical_alias']
        if alias in aliases or rec['cid'] in sources:raise ContractError('legacy ID collision; refuse')
        aliases.add(alias);sources.add(rec['cid'])
        changed.append({'alias':result,'original':dict(rec),'draft_projection':{k:v for k,v in rec.items() if k!='cid'}})
    return {'format':'wi8-japan04/migration-preview-1','status':'PREVIEW_ONLY_NOT_COMMITTED',
            'records':changed,'canonical_effects':0,'lossless_original_records':True}
