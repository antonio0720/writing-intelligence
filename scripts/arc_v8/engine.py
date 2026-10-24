"""Writing Intelligence — v8 Arc/Ending Read-Only Projection Evaluator.

Stdlib-only, deterministically evaluates authored narrative annotations against
an explicitly supplied canonical-graph projection. It is NOT a canonical store,
proof of literary quality, or integration with scripts/wi.py.
"""
from __future__ import annotations
import hashlib
import json
import re
from collections import Counter, defaultdict, deque
from datetime import datetime
from typing import Any, Dict, List, Optional

PROJECTION_SCHEMA = 'wi.arc.projection/v1'
REPORT_SCHEMA = 'wi.arc.report/v1'
CHARACTER_KINDS = {'protagonist', 'ensemble', 'supporting', 'antagonist'}
ARC_FAMILIES = {'positive_change', 'flat', 'corruption', 'fall', 'disillusionment', 'open', 'custom'}
KINDS = {'want', 'need', 'belief', 'ghost', 'arc_turn', 'choice', 'impact', 'relationship', 'cost', 'ending'}
BASES = {'author_asserted', 'reviewer_inferred', 'reader_reported', 'unverified', 'consistent_with_canon'}
WANTS = {'attained', 'thwarted', 'renounced', 'sacrificed', 'partial', 'unresolved', 'disputed', 'n_a'}
NEEDS = {'fulfilled', 'unfulfilled', 'rejected', 'partial', 'unresolved', 'disputed', 'n_a'}
QUADRANTS = {(True, True): 'sweet', (False, True): 'semi_sweet', (True, False): 'bittersweet', (False, False): 'bitter'}
SCOPES = {'working_draft', 'novel_final', 'series'}
SHA_RE = re.compile(r'^sha256:[0-9a-f]{64}$')
ISO_RE = re.compile(r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)$')


def digest(obj):
    """Digest input bytes as canonical JSON for audit identity, NOT v6 state_digest."""
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')
    return 'sha256:' + hashlib.sha256(b'wi8-arc-projection-v1\x00' + raw).hexdigest()


def finding(code, severity, location, message, requirement, evidence=None):
    return {'code': code, 'severity': severity, 'location': location, 'requirement': requirement,
            'message': message, 'evidence': sorted(set(evidence or []))}


def iso_parse(value):
    if not isinstance(value, str) or not ISO_RE.fullmatch(value):
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None


def _nonempty(s):
    return isinstance(s, str) and bool(s.strip())


def validate(doc):
    """Executable portable structural validator; mirrors the supplied JSON schema.

    No 'valid' here can certify the canonical graph, its actors, or the truth of interpretations.
    """
    fs = []
    def error(code, where, msg, rule='N113'):
        fs.append(finding(code, 'error', where, msg, rule))
    if not isinstance(doc, dict):
        return [finding('ARC_SCHEMA_ROOT', 'error', '$', 'Projection must be an object', 'N113')]
    if doc.get('schema') != PROJECTION_SCHEMA:
        error('ARC_SCHEMA_VERSION', '$.schema', 'Expected ' + PROJECTION_SCHEMA)
    source = doc.get('source')
    if not isinstance(source, dict):
        error('ARC_SOURCE_MISSING', '$.source', 'Source graph metadata is required', 'N111')
        source = {}
    if not SHA_RE.fullmatch(str(source.get('graph_root', ''))):
        error('ARC_GRAPH_ROOT', '$.source.graph_root', 'Graph root must be a declared sha256 digest', 'N111')
    if source.get('repo') != 'antonio0720/writing-intelligence':
        error('ARC_SOURCE_REPO', '$.source.repo', 'Source repository identity mismatch', 'N111')
    if source.get('origin') == 'canonical_export' and not _nonempty(source.get('readback_ref')):
        error('ARC_READBACK_MISSING', '$.source.readback_ref', 'Canonical export must declare independent core readback location; not verified by this tool', 'N114')
    if not _nonempty(source.get('branch')):
        error('ARC_BRANCH', '$.source.branch', 'Branch identity is required', 'N112')
    if source.get('origin') not in ('fixture', 'canonical_export'):
        error('ARC_ORIGIN', '$.source.origin', 'Origin is fixture or canonical_export, never inferred', 'N114')
    if not iso_parse(source.get('extracted_at')):
        error('ARC_EXTRACTION_TIME', '$.source.extracted_at', 'Valid timezone-aware ISO timestamp required', 'N112')
    if doc.get('scope') not in SCOPES:
        error('ARC_SCOPE', '$.scope', 'Scope must be working_draft, novel_final, or series')
    for key in ('characters','events','assertions'):
        if not isinstance(doc.get(key), list):
            error('ARC_LIST_REQUIRED', '$.'+key, 'Expected array for ' + key)
    chars = doc.get('characters') if isinstance(doc.get('characters'), list) else []
    events = doc.get('events') if isinstance(doc.get('events'), list) else []
    assertions = doc.get('assertions') if isinstance(doc.get('assertions'), list) else []
    ids = set()
    char_ids = set()
    event_ids = set()
    a_ids = set()
    event_orders = {}
    for i, c in enumerate(chars):
        where = '$.characters[%d]' % i
        if not isinstance(c, dict):
            error('ARC_CHAR_SHAPE', where, 'Character must be an object'); continue
        ident = c.get('id')
        if not _nonempty(ident) or ident in ids:
            error('ARC_DUPLICATE_ID', where+'.id', 'Missing or duplicated global node ID')
        else: ids.add(ident); char_ids.add(ident)
        if not _nonempty(c.get('name')): error('ARC_CHAR_NAME', where, 'Name required')
        if c.get('role') not in CHARACTER_KINDS: error('ARC_CHAR_ROLE', where, 'Unknown role')
        if c.get('arc_family') not in ARC_FAMILIES: error('ARC_FAMILY', where, 'Unknown arc family', 'N086')
    for i, ev in enumerate(events):
        where = '$.events[%d]' % i
        if not isinstance(ev, dict): error('ARC_EVENT_SHAPE', where, 'Event must be an object'); continue
        ident = ev.get('id')
        if not _nonempty(ident) or ident in ids: error('ARC_DUPLICATE_ID', where+'.id', 'Missing or duplicated global node ID')
        else: ids.add(ident); event_ids.add(ident)
        if type(ev.get('order')) is not int or ev.get('order') < 0: error('ARC_EVENT_ORDER', where, 'Event order must be a nonnegative integer', 'N112')
        else:
            if ev['order'] in event_orders: error('ARC_EVENT_ORDER_DUPLICATE', where, 'Two events have the same world-order index', 'N112')
            event_orders[ev['order']] = ident
        if not iso_parse(ev.get('known_at')): error('ARC_EVENT_KNOWLEDGE_TIME', where, 'Knowledge time required', 'N112')
        if not _nonempty(ev.get('scene_ref')): error('ARC_EVENT_SCENE', where, 'Source canon scene reference required', 'N113')
        if not isinstance(ev.get('causes', []), list): error('ARC_EVENT_CAUSES', where, 'Causes must be an array', 'N099')
    a_by_id = {}
    a_versions = set()
    for i, a in enumerate(assertions):
        where = '$.assertions[%d]' % i
        if not isinstance(a, dict): error('ARC_ASSERTION_SHAPE', where, 'Assertion must be an object'); continue
        ident = a.get('id')
        if not _nonempty(ident) or ident in ids: error('ARC_DUPLICATE_ID', where+'.id', 'Missing or duplicated global node ID')
        else: ids.add(ident); a_ids.add(ident); a_by_id[ident] = a
        if not _nonempty(a.get('logical_id')): error('ARC_LOGICAL_ID', where, 'Stable logical identity required', 'N112')
        if type(a.get('revision')) is not int or a.get('revision') < 1: error('ARC_REVISION', where, 'Revision >=1 required', 'N063')
        if a.get('kind') not in KINDS: error('ARC_KIND', where, 'Unknown semantic assertion kind', 'N111')
        if a.get('character_ref') not in char_ids: error('ARC_CHARACTER_REF', where, 'Unknown character', 'N069')
        version_key=(a.get('logical_id'),a.get('revision'))
        if version_key in a_versions: error('ARC_DUPLICATE_REVISION', where, 'Same logical state revision declared twice', 'N063')
        a_versions.add(version_key)
        if a.get('valid_from') not in event_ids: error('ARC_VALID_FROM', where, 'Unknown world-start event', 'N112')
        if a.get('valid_until') is not None and a.get('valid_until') not in event_ids:
            error('ARC_VALID_UNTIL', where, 'Unknown world-end event', 'N112')
        if not iso_parse(a.get('known_at')): error('ARC_KNOWLEDGE_TIME', where, 'Timezone-aware knowledge time required', 'N112')
        if not isinstance(a.get('payload'), dict): error('ARC_PAYLOAD', where, 'Typed payload required', 'N111')
        provenance = a.get('provenance')
        if not isinstance(provenance, dict) or provenance.get('basis') not in BASES:
            error('ARC_PROVENANCE', where, 'Recognized basis required', 'N068')
        elif not _nonempty(provenance.get('actor_id')): error('ARC_PROVENANCE_ACTOR', where, 'Claim interpreter ID required', 'N068')
        if not isinstance(a.get('evidence_refs'), list): error('ARC_EVIDENCE_REFS', where, 'Evidence references array required', 'N114')
        if not isinstance(a.get('derived_from', []), list): error('ARC_DERIVED_REFS', where, 'Derived-from array required', 'N111')
        payload=a.get('payload') if isinstance(a.get('payload'),dict) else {}
        if a.get('kind') in {'want','need','belief','ghost'} and not _nonempty(payload.get('proposition')):
            error('ARC_PROPOSITION', where, 'Proposition required for semantic assertion', 'N061')
        if a.get('kind') == 'ending':
            p=payload
            if p.get('want_outcome') not in WANTS: error('ARC_WANT_OUTCOME', where, 'Unknown want outcome', 'N065')
            if p.get('need_outcome') not in NEEDS: error('ARC_NEED_OUTCOME', where, 'Unknown need outcome', 'N065')
            for key in ('want_ref','need_ref'):
                if not _nonempty(p.get(key)): error('ARC_ENDING_FOCUS', where+'.payload.'+key, 'Focus explicit to avoid universal assumptions', 'N069')
            if p.get('closure') not in {'closed','open','deliberately_ambiguous'}:
                error('ARC_ENDING_CLOSURE', where, 'Explicit closure needed', 'N070')
    for i, ev in enumerate(events):
        if not isinstance(ev, dict): continue
        for dependency in ev.get('causes', []) if isinstance(ev.get('causes'), list) else []:
            if dependency not in event_ids: error('ARC_EVENT_CAUSE_DANGLING', '$.events[%d].causes'%i, 'Unknown causal event', 'N099')
    for i, a in enumerate(assertions):
        if not isinstance(a, dict): continue
        where = '$.assertions[%d]' % i
        for key in ('evidence_refs','derived_from'):
            for x in a.get(key, []) if isinstance(a.get(key),list) else []:
                if x not in ids: error('ARC_REF_DANGLING', where+'.'+key, 'Unknown local reference: '+str(x), 'N113')
                if x == a.get('id'): error('ARC_SELF_DEPENDENCY', where+'.'+key, 'Self-dependency prohibited', 'N113')
        start = next((e.get('order') for e in events if isinstance(e,dict) and e.get('id') == a.get('valid_from')), None)
        end = next((e.get('order') for e in events if isinstance(e,dict) and e.get('id') == a.get('valid_until')), None)
        if isinstance(start,int) and isinstance(end,int) and start >= end:
            error('ARC_TIME_INTERVAL', where, 'valid_until must follow valid_from (half-open)', 'N112')
        old = a_by_id.get(a.get('supersedes'))
        if a.get('supersedes') is not None:
            if not old: error('ARC_SUPERSEDES_UNKNOWN', where, 'Unknown prior revision', 'N063')
            elif old.get('logical_id') != a.get('logical_id') or old.get('kind') != a.get('kind') or old.get('character_ref') != a.get('character_ref'):
                error('ARC_SUPERSEDES_IDENTITY', where, 'History revision changes logical identity, kind or owner', 'N063')
            elif isinstance(old.get('revision'),int) and isinstance(a.get('revision'),int) and a['revision'] != old['revision']+1:
                error('ARC_REVISION_GAP', where, 'Revision must advance exactly one step', 'N063')
            elif iso_parse(old.get('known_at')) and iso_parse(a.get('known_at')) and iso_parse(old['known_at']) >= iso_parse(a['known_at']):
                error('ARC_REVISION_KNOWLEDGE_ORDER', where, 'New revision known before/equal to prior revision', 'N112')
        elif a.get('revision') != 1: error('ARC_MISSING_SUPERSEDES', where, 'Non-initial revision lacks predecessor', 'N063')
        if a.get('kind') == 'ending':
            p=a.get('payload') if isinstance(a.get('payload'),dict) else {}
            for key, expected in (('want_ref','want'),('need_ref','need')):
                ref=a_by_id.get(p.get(key))
                if ref is None: error('ARC_FOCUS_DANGLING', where+'.payload.'+key, 'Ending focus missing', 'N069')
                elif ref.get('kind') != expected or ref.get('character_ref') != a.get('character_ref'):
                    error('ARC_FOCUS_WRONG_OWNER', where+'.payload.'+key, 'Ending focus kind or character mismatch', 'N069')
            if p.get('choice_ref') is not None:
                choice=a_by_id.get(p.get('choice_ref'))
                if not choice or choice.get('kind') != 'choice' or choice.get('character_ref') != a.get('character_ref'):
                    error('ARC_CHOICE_REF', where, 'Final choice reference must point at same character choice', 'N109')
    # Cycle checks are identity-sensitive; avoiding recursion makes long manuscripts safe.
    dep = defaultdict(list)
    for e in events:
        if isinstance(e,dict):
            for prior in e.get('causes',[]) if isinstance(e.get('causes'),list) else []:
                dep[e.get('id')].append(prior)
    for a in assertions:
        if isinstance(a,dict):
            dep[a.get('id')].extend(x for x in a.get('derived_from',[]) if isinstance(a.get('derived_from'),list))
    state={}
    def detect_cycle(start):
        stack=[(start,False)]
        while stack:
            node,done=stack.pop()
            if done: state[node]=2; continue
            if state.get(node)==2: continue
            if state.get(node)==1: return True
            state[node]=1; stack.append((node,True))
            for nxt in dep.get(node,[]):
                if state.get(nxt)==1: return True
                if state.get(nxt)!=2: stack.append((nxt,False))
        return False
    for ident in dep:
        if state.get(ident) != 2 and detect_cycle(ident):
            error('ARC_CAUSAL_CYCLE', '$.events+assertions', 'Cycle in declared dependencies', 'N099'); break
    return sorted(fs,key=lambda f:(f['location'],f['code']))


def classify(ending, need_provenance_basis='author_asserted', ending_basis='author_asserted'):
    """Transparent 2x2 projection. Authors' interpretations remain authors' interpretations."""
    want = ending.get('want_outcome')
    need = ending.get('need_outcome')
    reasons=[]
    if need_provenance_basis != 'author_asserted' or ending_basis != 'author_asserted':
        reasons.append('Need and ending are not both author-asserted; reviewer/reader inference is not canon')
    if ending.get('closure') != 'closed':
        reasons.append('Ending is open or deliberately ambiguous')
    if want not in {'attained','thwarted','renounced','sacrificed'}:
        reasons.append('Want is not an unambiguous terminal binary result')
    if need not in {'fulfilled','unfulfilled','rejected'}:
        reasons.append('Need is not an unambiguous terminal binary result')
    if reasons:
        return {'quadrant':'not_classifiable','reasons': reasons,'epistemic_status':'not_determined'}
    key=(want=='attained', need=='fulfilled')
    return {'quadrant':QUADRANTS[key], 'reasons':[],
            'epistemic_status':'derived_from_author_asserted_interpretation',
            'want_binary':key[0], 'need_binary':key[1]}


def as_of(doc, event_id, known_at):
    """Projection of asserted state as of world event AND knowledge time."""
    errors=validate(doc)
    if errors: return {'status':'invalid','findings':errors}
    order = {e['id']:e['order'] for e in doc['events']}
    if event_id not in order: return {'status':'invalid','findings':[finding('ARC_UNKNOWN_EVENT','error','event_id','Unknown world event','N112')]}
    time = iso_parse(known_at)
    if not time: return {'status':'invalid','findings':[finding('ARC_ASOF_TIME','error','known_at','Invalid knowledge time','N112')]}
    eligible=defaultdict(list)
    for a in doc['assertions']:
        if order[a['valid_from']]<=order[event_id] and (a.get('valid_until') is None or order[event_id]<order[a['valid_until']]) and iso_parse(a['known_at'])<=time:
            eligible[a['logical_id']].append(a)
    projected={}
    for key,vals in sorted(eligible.items()):
        chosen=max(vals,key=lambda x:(iso_parse(x['known_at']),x['revision']))
        projected[key]={'state_id':chosen['id'],'revision':chosen['revision'],'kind':chosen['kind'],
                        'character_ref':chosen['character_ref'],'payload':chosen['payload'],
                        'provenance':chosen['provenance']}
    return {'status':'projected','event_id':event_id,'known_at':known_at, 'states': projected}


def impact(doc, changed_ids):
    """Read-only dependency frontier, not the canonical v6 invalidation engine."""
    errors=validate(doc)
    if errors: return {'status':'invalid','findings':errors}
    ids={x['id'] for x in doc['assertions']}|{x['id'] for x in doc['events']}
    unknown=sorted(set(changed_ids)-ids)
    if unknown:return {'status':'invalid','unknown_ids':unknown}
    reverse=defaultdict(set)
    for a in doc['assertions']:
        for ref in a.get('derived_from',[])+a['evidence_refs']:
            reverse[ref].add(a['id'])
    for e in doc['events']:
        for ref in e.get('causes',[]): reverse[ref].add(e['id'])
    found=set(changed_ids); q=deque(sorted(found)); waves=[]
    while q:
        item=q.popleft()
        new=sorted(reverse.get(item,set())-found)
        found.update(new); q.extend(new)
        if new: waves.append({'from':item,'directly_affected':new})
    return {'status':'projection_only','changed':sorted(set(changed_ids)),
            'downstream_may_be_stale':sorted(found-set(changed_ids)),
            'dependency_walk':waves,
            'warning':'Re-run canonical wi impact/obligations: this projection cannot invalidate real graph state.'}


def evaluate(doc):
    """Deterministic structural evaluation with separate interpretive review signals."""
    invalid=validate(doc)
    src = doc.get('source') if isinstance(doc,dict) and isinstance(doc.get('source'),dict) else {}
    report={'schema':REPORT_SCHEMA,'source_digest':digest(doc),'source_graph_root':src.get('graph_root'),
            'origin':src.get('origin'),
            'status':'invalid' if invalid else 'evaluated', 'findings':invalid,
            'characters':[], 'coverage':{}, 'limits':[
                'A source_root supplied in JSON is an assertion until independently matched to canonical core readback.',
                'All wants, needs, beliefs, arcs and endings are authored interpretations, not machine-proven psychology.',
                'Mechanical conformance is not evidence of emotional impact or reader satisfaction.',
                'This tool neither modifies canon nor implements canonical authority and commitment.'
            ]}
    if invalid: return report
    fs=[]
    by_id={a['id']:a for a in doc['assertions']}
    char_data=[]
    for char in doc['characters']:
        owned=[a for a in doc['assertions'] if a['character_ref']==char['id']]
        endings=[a for a in owned if a['kind']=='ending']
        snapshots=[]
        for a in endings:
            p=a['payload']; need=by_id[p['need_ref']]
            outcome=classify(p,need['provenance']['basis'],a['provenance']['basis'])
            snapshots.append({'assertion_id':a['id'],'arc_family':char['arc_family'],
                              'want_ref':p['want_ref'],'need_ref':p['need_ref'], 'projection':outcome,
                              'reader_valence':p.get('reader_valence'),
                              'closure':p['closure']})
            if p['closure']=='closed' and not a['evidence_refs']:
                fs.append(finding('ARC_ENDING_UNWITNESSED','review',a['id'],
                    'Closed ending has no witnessed canonical event', 'N109'))
            if p['closure']=='closed' and p.get('need_outcome')=='fulfilled' and p.get('choice_ref') is None:
                fs.append(finding('ARC_CLAIMED_CHANGE_NO_CHOICE','review',a['id'],
                    'Need fulfillment is declared without an identified behavioral choice', 'N078'))
            if outcome['quadrant']=='not_classifiable':
                fs.append(finding('ARC_ENDING_NONBINARY','info',a['id'],
                    '; '.join(outcome['reasons']), 'N064'))
            if p.get('reader_valence') is not None:
                fs.append(finding('ARC_READER_VALENCE_ASSERTED','review',a['id'],
                    'Narrator/author projection may not stand in for independent reader reports', 'N110'))
        if char['role'] in ('protagonist','ensemble') and doc['scope']=='novel_final' and not endings:
            fs.append(finding('ARC_PROTAGONIST_ENDING_MISSING','review',char['id'],
                'No ending projection supplied for central character', 'N069'))
        for a in owned:
            if a['kind']=='arc_turn' and not a['evidence_refs']:
                fs.append(finding('ARC_TURN_UNWITNESSED','review',a['id'],
                    'Claimed turn lacks scene/event witness', 'N099'))
            if a['kind']=='need' and a['provenance']['basis']=='unverified':
                fs.append(finding('ARC_NEED_UNVERIFIED','review',a['id'],
                    'Internal need is unverified interpretation, not an established character property', 'N068'))
            if a['kind']=='choice' and not a['evidence_refs']:
                fs.append(finding('ARC_CHOICE_UNWITNESSED','review',a['id'],
                    'No witnessed decision supplied', 'N079'))
            if a['kind']=='ghost' and a['payload'].get('universal_trauma_cause') is True:
                fs.append(finding('ARC_UNIVERSAL_TRAUMA_ASSUMPTION','review',a['id'],
                    'Trauma is not mandatory or a universal causal explanation', 'N071'))
        char_data.append({'character_ref':char['id'],'arc_family':char['arc_family'],
                          'endings':snapshots,
                          'wants':[a['id'] for a in owned if a['kind']=='want'],
                          'needs':[a['id'] for a in owned if a['kind']=='need'],
                          'turns':[a['id'] for a in owned if a['kind']=='arc_turn']})
    report['characters']=char_data
    report['findings']=sorted(fs,key=lambda f:(f['location'],f['code']))
    report['coverage']={
      'characters':len(doc['characters']), 'events':len(doc['events']),
      'assertions':len(doc['assertions']), 'ending_projections':sum(len(x['endings']) for x in char_data),
      'automated_validity':'structure_and_declared_dependency_only',
      'human_review':'not_performed_by_this_tool',
      'reader_study':'not_performed_by_this_tool'}
    return report


def gate(doc, reader_reviews=None, stage='mechanical'):
    r=evaluate(doc)
    if r['status']=='invalid': return {'verdict':'BLOCK','stage':stage,'reason':'Invalid typed projection','report':r}
    if stage not in ('mechanical','editorial','publication'): raise ValueError('stage must be mechanical, editorial or publication')
    if stage=='mechanical':
        return {'verdict':'PASS_MECHANICAL_ONLY','stage':stage,
                'reason':'Only local typed invariants were checked, no canon readback', 'report':r}
    reasons=[]
    if any(f['severity']=='review' for f in r['findings']): reasons.append('Unresolved interpretive findings')
    if doc.get('scope')=='novel_final' and any(x['arc_family']!='open' and not x['endings'] for x in r['characters'] if x['character_ref']):
        reasons.append('Incomplete ending coverage')
    if stage=='publication':
        if not reader_reviews or not isinstance(reader_reviews,dict) or reader_reviews.get('schema')!='wi.arc.reader_review/v1':
            reasons.append('No independent human reader evidence supplied')
        else:
            if reader_reviews.get('source_digest')!=r['source_digest']:
                reasons.append('Reader study source digest stale or mismatched')
            if len({x.get('reader_id') for x in reader_reviews.get('responses',[]) if isinstance(x,dict) and x.get('blind') is True})<2:
                reasons.append('Fewer than two distinct blinded reader reports')
    if stage=='editorial': reasons.append('Literary judgment is not executable; obtain qualified editorial acceptance')
    if stage=='publication': reasons.append('Publication authorization, canon audit, typesetting and rights checks run outside this module')
    return {'verdict':'HOLD','stage':stage,'reason':'; '.join(reasons), 'report':r}


def state_diff(doc, start_event, end_event, known_at, character_ref=None):
    """Deterministic opening/closing state diff, not a claim of character transformation."""
    left=as_of(doc,start_event,known_at)
    right=as_of(doc,end_event,known_at)
    if left['status'] != 'projected' or right['status'] != 'projected':
        return {'status':'invalid','finding':'Unable to project both states', 'left':left, 'right':right}
    lhs={k:v for k,v in left['states'].items() if character_ref is None or v['character_ref']==character_ref}
    rhs={k:v for k,v in right['states'].items() if character_ref is None or v['character_ref']==character_ref}
    if character_ref is not None and character_ref not in {c['id'] for c in doc['characters']}:
        return {'status':'invalid','finding':'Unknown character'}
    changes=[]
    for key in sorted(set(lhs)|set(rhs)):
        before=lhs.get(key);after=rhs.get(key)
        if before != after:
            changes.append({'logical_id':key,'change':('introduced' if before is None else 'ceased' if after is None else 'state_changed'),
                            'before':before,'after':after})
    return {'status':'projection_only','start_event':start_event,'end_event':end_event,
            'known_at':known_at,'character_ref':character_ref,'changes':changes,
            'caution':'These differences are author-declared states; psychological transformation and causal adequacy require review.'}
