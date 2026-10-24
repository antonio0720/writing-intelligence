"""Context-dependent Japan craft checks: no global cultural linter or made-up timetables."""
from __future__ import annotations
from datetime import date
from .contracts import ContractError,require

ERA_BOUNDARIES = ((date(2019,5,1),'Reiwa',2018), (date(1989,1,8),'Heisei',1988),
                  (date(1926,12,25),'Shōwa',1925), (date(1912,7,30),'Taishō',1911),
                  (date(1873,1,1),'Meiji',1867))

def era_from_gregorian(y,m,d):
    """Named Japanese era for Gregorian dates >= 1873; don't fabricate old lunisolar conversion."""
    when=date(y,m,d)
    if when<date(1873,1,1):raise ContractError('pre-1873 calendrical conversion requires specialized source')
    for boundary,era,offset in ERA_BOUNDARIES:
        if when>=boundary:return {'era':era,'year_of_era':y-offset,'gregorian':when.isoformat(),
                                  'calendar_assumption':'Gregorian','verified_current_event':False}
    raise AssertionError('unreachable')

def cultural_applicability(claim_scope, scene_scope):
    """Conservative three-valued applicability: match, mismatch or unknown.

    These are asserted textual scope checks, never verification of the claim itself.
    An Okinawan source isn't automatically a Kyoto custom even when both are
    inside Japan; both can be meaningful where their scoped facts are evidenced.
    """
    keys=('region','prefecture','municipality','site_id','institution','tradition','era','community')
    if not isinstance(claim_scope,dict) or not isinstance(scene_scope,dict):raise ContractError('scope objects required')
    matched=[];missing=[];mismatched=[]
    for k in keys:
        if k in claim_scope:
            if k not in scene_scope:missing.append(k)
            elif claim_scope[k] not in (scene_scope[k],'all') and scene_scope[k] !='all':mismatched.append(k)
            else:matched.append(k)
    status = 'mismatch' if mismatched else ('unknown' if missing or not matched else 'scope_match_only')
    return {'status':status,'matched_dimensions':matched,'mismatched_dimensions':mismatched,'unknown_dimensions':missing,
            'culturally_correct':None,'source_verified':False}

def tradition_hint(site_kind, proposed_rule):
    """Detect a small class of asserted site ontology mixups, not universal etiquette."""
    if site_kind not in ('buddhist_temple','shinto_shrine','other','unknown','invented'):
        raise ContractError('unknown kind; do not infer religion from name')
    if proposed_rule=='torii_required' and site_kind=='buddhist_temple':
        return {'status':'REVIEW','reason':'Torii cannot be universally mandated for Buddhist temples','severity':'likely_mismatch'}
    return {'status':'CONTEXT_REQUIRED','reason':'Site-custodian and period-specific evidence required','severity':'unknown'}

def honorific_transition(previous, current, intended_effect=None):
    """Shifts are interpretable character actions, not fixed cultural violations."""
    return {'changed':previous!=current,'author_intention':intended_effect,
            'status':'author_intent_recorded' if previous!=current and intended_effect else 'contextual_review',
            'forbidden':False,'authenticity_proven':False}

def grade_transition(school_year_start,age,grade=None):
    """Context-only: no global April enforcement for every institution."""
    require(school_year_start in range(1,13),'school start month must be 1..12')
    require(type(age) is int and age>=0,'age must be nonnegative')
    return {'start_month':school_year_start,'age':age,'grade':grade,
            'institution_specific':True,'national_universal_claim':False}

def scene_travel(start,end,adjacency,exception=None):
    """Declare reachability only from provided adjacency; no invented ETA."""
    require(isinstance(start,str) and isinstance(end,str),'place IDs required')
    require(isinstance(adjacency,dict),'map adjacency dictionary required')
    if exception:
        return {'plausible':'author_declared_magic','exception_ref':exception,'estimated_minutes':None}
    if start==end:return {'plausible':'same_place','estimated_minutes':0}
    if end in adjacency.get(start,[]):return {'plausible':'declared_adjacent','estimated_minutes':None}
    return {'plausible':'needs_route_evidence','estimated_minutes':None}

def simulate_power_ledger(events, opening_resources):
    if not isinstance(events,list) or not isinstance(opening_resources,dict):raise ContractError('inputs invalid')
    resources=dict(opening_resources);entries=[]
    for k,v in resources.items():
        require(type(v) is int and v>=0,'initial resources nonnegative ints')
    for event in events:
        name=event.get('resource');change=event.get('delta')
        if name not in resources or type(change) is not int:raise ContractError('unrecognized pool or invalid delta')
        before=resources[name];after=before+change
        if after<0:return {'status':'BLOCK_OVERSPENT','at_event':event.get('id'),'resource':name,
                            'remaining_before':before,'attempted_change':change,'entries':entries}
        resources[name]=after
        entries.append({'id':event.get('id'),'resource':name,'before':before,'delta':change,'after':after})
    return {'status':'CONSISTENT_WITH_DECLARED_RESOURCES','ending_resources':resources,'entries':entries,
            'actual_fictional_canon_verified':False}
