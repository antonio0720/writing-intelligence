"""Typed, fail-closed contracts. Python standard library only.

A record is a *projection* of future Writing Intelligence semantic nodes, not a
stand-in for its canonical object store. Canonical revisions require upstream
v6 proposals, authority checks and commits; this toolkit cannot perform them.
"""
from __future__ import annotations
import hashlib
import json
import re
from typing import Any

class ContractError(ValueError):
    pass

REALMS = frozenset({'external_fact', 'fictional_canon', 'interpretation', 'research_note', 'simulation'})
STATES = frozenset({'proposed', 'author_adopted', 'archived', 'retconned'})
AUTHOR_MODES = frozenset({'ask','research','challenge','outline','edit','co-create','surprise','questions-only','experiment'})
RESEARCH_STATES = frozenset({'NEEDS_SOURCE','SOURCED_UNREVIEWED','SOURCE_CONFLICT','EXPERT_REVIEWED','STALE','INVENTED'})
ASSURANCE = frozenset({'mechanically_checked','author_asserted','reviewer_inferred','reader_reported','unverified','disputed'})
SOURCE_KINDS = frozenset({'primary','community_custodian','museum','scholarship','government','local_organizer','secondary','media','field_observation','unknown'})
PROTECTION = frozenset({'public','private','restricted'})
UNKNOWN = 'UNKNOWN'
ALLOWED_EDGES = frozenset({'source_inspires','source_documents_variant','author_adopts','fiction_diverges','reviewed_by','renders_as','depends_on','derived_from','set_in','contradicts','costs','consents_to','changes_relationship'})
SCRIPT = frozenset({'kanji','hiragana','katakana','latin','mixed'})


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def mapping(data: Any, name: str) -> dict:
    require(type(data) is dict, name + ' must be object')
    return data


def seq(data: Any, name: str) -> list:
    require(type(data) is list, name + ' must be array')
    return data


def nonempty(data: Any, name: str) -> str:
    require(type(data) is str and len(data.strip()) > 0, name + ' must be nonempty string')
    return data


def unique_ids(rows: list, name: str) -> None:
    ids = []
    for i, row in enumerate(rows):
        mapping(row, f'{name}[{i}]')
        ids.append(nonempty(row.get('id'), f'{name}[{i}].id'))
    require(len(ids) == len(set(ids)), name + ' has duplicate IDs')


def digest(data: Any) -> str:
    # Local transport digest, not the repo's canonical state digest.
    payload=json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')
    return 'sha256:'+hashlib.sha256(b'WI8-JP04-PROJECTION-ONLY\0'+payload).hexdigest()


def validate_claim(row: dict) -> None:
    mapping(row, 'claim')
    nonempty(row.get('id'), 'claim.id'); nonempty(row.get('statement'),'claim.statement')
    realm=row.get('realm'); require(realm in REALMS, 'claim realm invalid')
    if realm == 'external_fact':
        scope = mapping(row.get('scope'), 'external claim scope')
        require(any(scope.get(k) for k in ('region','place','community','institution','era')), 'external claims need nonempty scope')
        require(row.get('source_status') in RESEARCH_STATES - {'INVENTED'}, 'external claim source status required')
        require(type(row.get('source_refs')) is list, 'external claim source_refs must be array')
        if row.get('source_status') in {'EXPERT_REVIEWED'}:
            require(bool(row['source_refs']), 'source-reviewed claim must cite a source')
    if realm == 'fictional_canon':
        nonempty(row.get('world_id'), 'fictional claim.world_id')
        require(row.get('canon_state') in STATES, 'fictional claim canon_state invalid')
        require(row.get('source_status') not in {'EXPERT_REVIEWED'}, 'fictional canon is not external research verification')
        if row['canon_state'] == 'author_adopted':
            nonempty(row.get('author_decision_id'), 'adoption requires author decision')
    if realm == 'interpretation':
        require(row.get('assurance') in ASSURANCE, 'interpretation assurance required')
        require(row.get('assurance') != 'mechanically_checked', 'interpretation cannot be mechanically established as truth')


def validate_source(row: dict) -> None:
    mapping(row,'source'); nonempty(row.get('id'), 'source.id'); nonempty(row.get('title'),'source.title')
    require(row.get('kind') in SOURCE_KINDS,'source.kind invalid')
    require(row.get('status') in RESEARCH_STATES - {'INVENTED'},'source.status invalid')
    require(row.get('rights') in {'unknown','public_domain','licensed','permission_required','restricted'},'source.rights invalid')
    if row.get('status') == 'EXPERT_REVIEWED':
        nonempty(row.get('reviewer_ref'), 'expert reviewed source requires named reviewer reference')
    if row.get('protected'):
        require(row.get('rights') in {'restricted','permission_required'},'protected source must carry restrictive rights')


def validate_variant(row: dict, sources: dict) -> None:
    mapping(row,'variant'); nonempty(row.get('id'),'variant.id')
    nonempty(row.get('subject'),'variant.subject'); nonempty(row.get('account'),'variant.account')
    refs=seq(row.get('source_refs',[]),'variant.source_refs')
    for ref in refs:
        require(ref in sources,'variant unknown source: '+str(ref))
    require(row.get('status') in {'recorded','disputed','unverified','invented'},'variant.status invalid')
    require(type(row.get('scope',{})) is dict,'variant.scope must be object')
    if row['status'] == 'recorded':
        require(bool(refs),'recorded folklore variant needs source')


def validate_world(row: dict) -> None:
    mapping(row,'world'); nonempty(row.get('id'), 'world.id'); nonempty(row.get('title'),'world.title')
    require(row.get('genre_mode') in {'contemporary','historic','alternate_history','fantasy','near_future','invented','slice_of_life'},'world.genre_mode invalid')
    require(row.get('powers') is None or isinstance(row.get('powers'),dict),'world.powers must be object or null')
    if row.get('powers'):
        for ability in seq(row['powers'].get('abilities',[]),'world.powers.abilities'):
            nonempty(ability.get('id'),'ability.id')
            require(type(ability.get('costs',[])) is list,'ability.costs must be array')
            require(type(ability.get('limits',[])) is list,'ability.limits must be array')


def validate_project(data: dict) -> dict:
    mapping(data,'project')
    require(data.get('format')=='wi8-japan04/projection-1','incorrect or counterfeit project format')
    require(data.get('authority')=='noncanonical_projection','must not claim canonical authority')
    require(data.get('network_policy')=='offline','network must be offline')
    require(data.get('release_policy')=='preview_only','release policy must be preview_only')
    for field in ('sources','claims','variants','worlds','edges','names','places','events','characters','techniques','reviews','adaptations','seeds'):
        seq(data.get(field,[]),field)
        if field != 'edges': unique_ids(data.get(field,[]),field)
    sources={x['id']:x for x in data['sources']}
    worlds={x['id']:x for x in data['worlds']}
    for s in data['sources']:validate_source(s)
    for c in data['claims']:
        validate_claim(c)
        for ref in c.get('source_refs',[]):
            require(ref in sources,'claim points at nonexistent source')
        if c.get('realm')=='fictional_canon':require(c['world_id'] in worlds,'fiction references missing world')
    for v in data['variants']:validate_variant(v,sources)
    for w in data['worlds']:validate_world(w)
    ids=set().union(*(set(x['id'] for x in data[k]) for k in ('sources','claims','variants','worlds','names','places','events','characters','techniques','reviews','adaptations','seeds')))
    counts=sum(len(data[k]) for k in ('sources','claims','variants','worlds','names','places','events','characters','techniques','reviews','adaptations','seeds'))
    require(len(ids)==counts, 'duplicate ID across different entity families')
    for e in data['edges']:
        require(e.get('relation') in ALLOWED_EDGES, 'unknown semantic relation')
        require(e.get('from') in ids and e.get('to') in ids, 'dangling semantic edge')
        require(e.get('from') != e.get('to') or e.get('relation') in {'contradicts'}, 'meaningless self-edge')
    return data


def empty_project() -> dict:
    return {'format':'wi8-japan04/projection-1','authority':'noncanonical_projection','network_policy':'offline','release_policy':'preview_only',
            'sources':[],'claims':[],'variants':[],'worlds':[],'edges':[],'names':[],'places':[],'events':[],'characters':[],'techniques':[],
            'reviews':[],'adaptations':[],'seeds':[]}
