"""Deterministic validation of scoped research and adopted fictional rules.

Findings do not claim Japanese cultural truth; external accuracy requires
source inspection by qualified humans. Severity is bounded to evidence.
"""
from __future__ import annotations
from .contracts import validate_project, ContractError, digest


def finding(code, subject, category, severity, explanation, requirements, provenance='mechanically_checked'):
    return {'code':code,'subject':subject,'category':category,'severity':severity,'explanation':explanation,
            'requirements':requirements,'assurance':provenance}


def analyze(project:dict) -> dict:
    validate_project(project)
    findings=[]
    claims=project['claims']; sources={s['id']:s for s in project['sources']}
    for c in claims:
        if c['realm']=='external_fact':
            if not c.get('source_refs'):
                findings.append(finding('JP_SOURCE_REQUIRED',c['id'],'research','review','Factual assertion has no source; no authenticity conclusion possible',[191,194,197,198,334]))
            if c.get('source_status') in ('NEEDS_SOURCE','STALE','SOURCE_CONFLICT'):
                findings.append(finding('JP_SOURCE_UNRESOLVED',c['id'],'research','review','Current source status is unresolved; do not use as verified publication fact',[193,196,200,205,218]))
            for ref in c.get('source_refs',[]):
                src=sources[ref]
                if src['rights'] in ('restricted','permission_required'):
                    findings.append(finding('JP_RIGHTS_REVIEW',c['id'],'rights','hold','Reference may not be republished without permission',[321,323,324,330]))
            if c.get('scope',{}).get('region')=='all_japan' and not c.get('universal_basis_refs'):
                findings.append(finding('JP_UNIVERSAL_SCOPE_UNSUPPORTED',c['id'],'research','review','Nationwide generalization lacks explicit scoped substantiation',[194,196,224,242,255]))
        if c['realm']=='fictional_canon' and c.get('source_status') == 'INVENTED' and c.get('canon_state')=='proposed':
            findings.append(finding('JP_SEED_UNADOPTED',c['id'],'authorship','info','This fictional invention is proposed, not canon',[186,191,195]))
    # Same subject may have multiple legitimate geographically distinct variants.
    groups={}
    for v in project['variants']: groups.setdefault(v['subject'],[]).append(v)
    for subject,versions in groups.items():
        if len(versions)>1:
            findings.append(finding('JP_VARIANTS_PRESERVED',subject,'folklore','info','Multiple attributed versions preserved; no automatic winning interpretation',[192,249,251,252,258]))
    # No global expectation of supernatural techniques: optional and per-world.
    for w in project['worlds']:
        if w.get('powers') and w['powers'].get('kind')=='ki_threads':
            abilities=w['powers'].get('abilities',[]); ids=set()
            for a in abilities:
                if a['id'] in ids: raise ContractError('duplicate technique within world')
                ids.add(a['id'])
                if a.get('decisive',False) and not (a.get('causal_setup_refs') or a.get('intentional_mystery_exception')):
                    findings.append(finding('JP_DEUS_EX_CAUSAL_GAP',a['id'],'fictional_canon','review','Decisive power lacks established setup or declared mystery exception',[272,280]))
                if a.get('spends',0) and a['spends']<0:
                    raise ContractError('ability spends cannot be negative')
    # Programmatic semantic fallibility boundaries.
    for n in project['names']:
        if n.get('kanji') and not n.get('reading'):
            findings.append(finding('JP_READING_UNKNOWN',n['id'],'language','review','Kanji has no author-selected/attested pronunciation; do not fabricate a reading',[221,223,334]))
        if n.get('reading') and n.get('reading_status')=='verified' and not n.get('source_refs'):
            findings.append(finding('JP_READING_UNSUPPORTED',n['id'],'language','review','Reading labeled verified without any source',[221,223]))
    for p in project['places']:
        if p.get('kind')=='real' and p.get('travel_claim') and not p.get('travel_source_ref'):
            findings.append(finding('JP_TIMETABLE_NEEDS_CURRENT_SOURCE',p['id'],'geography','review','Transit or time claim needs date-specific source',[201,205,210,300]))
        if p.get('kind')=='invented' and not p.get('world_id'):
            findings.append(finding('JP_FANTASY_PLACE_NEEDS_WORLD',p['id'],'fictional_canon','review','Invented place must bind to a declared fictional world',[209,298]))
    for e in project['events']:
        if e.get('kind')=='festival' and (not e.get('year') or not e.get('place_id') or not e.get('organizer_source_ref')):
            findings.append(finding('JP_FESTIVAL_SCOPE_MISSING',e['id'],'time','review','Festival date requires year, place and organizer source',[218,193,200]))
        if e.get('historical') and e.get('real') and e.get('alternate_history') and not e.get('divergence_ref'):
            findings.append(finding('JP_UNDECLARED_ALTERNATE_HISTORY',e['id'],'time','review','Fictional historical departure must be annotated',[195,211,212,298]))
    for t in project['techniques']:
        if t.get('uses') and not t.get('world_id'):
            findings.append(finding('JP_TECHNIQUE_UNBOUND',t['id'],'fictional_canon','review','A technique is valid only within its own declared series',[271,272,279]))
        if t.get('resource_before') is not None and t.get('resource_spent') is not None:
            a,b=t['resource_before'],t['resource_spent']
            if type(a) not in (int,float) or type(b) not in (int,float) or a<0 or b<0: raise ContractError('invalid resource counters')
            if b>a and not t.get('replenishment_ref'):
                findings.append(finding('JP_RESOURCE_OVERSPENT',t['id'],'fictional_canon','defect','Power resource spent exceeds declared available amount',[279,290]))
    for item in project['adaptations']:
        if item.get('proposes_canon_change') and not item.get('author_decision_id'):
            findings.append(finding('JP_ADAPTATION_NOT_CANON',item['id'],'authorship','hold','Derivative adaptation cannot silently alter source novel canon',[304,306,309,310]))
    for s in project['seeds']:
        if s.get('adopted') and not s.get('author_decision_id'):
            findings.append(finding('JP_SEED_ADOPTION_FORBIDDEN',s['id'],'authorship','hold','Seed cannot enter canon without explicit author decision',[181,186,317]))
    # Safety does not depend on a cultural authenticity scalar.
    findings.sort(key=lambda x:(x['code'],x['subject']))
    return {'format':'wi8-japan04/report-1','source_projection_digest':digest(project),'status':'diagnostic_only','findings':findings,
            'reported_categories':['mechanical_consistency','research_provenance','author_intention','rights','publication_authority'],
            'explicitly_not_verified':['aesthetic_quality','cultural_authenticity','native_language_fluency','reader_response','external_publication_readiness']}
