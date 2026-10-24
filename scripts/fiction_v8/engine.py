"""Evidence-bounded fiction audits. Offline, deterministic, no model dependencies.

Only an explicit canon or structural contradiction is a machine DEFECT.
Heuristics are SIGNAL, omission is UNASSESSED, artistic judgment is REVIEWED.
Never represent a typed annotation as proof of reader experience.
"""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

RULES_PATH = Path(__file__).resolve().parents[2] / 'rules' / 'fiction_v8_rules.json'
PROFILES_PATH = Path(__file__).resolve().parents[2] / 'policies' / 'fiction_profiles.json'


def stable_json(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')


def digest(obj):
    return 'sha256:' + hashlib.sha256(stable_json(obj)).hexdigest()


def load_json(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def catalog():
    data = load_json(RULES_PATH)
    expected = [f'FI-{i:02d}' for i in range(1, 61)]
    if data.get('schema') != 'wi.fiction.rule-catalog/v1' or [r['id'] for r in data.get('rules', [])] != expected:
        raise ValueError('invalid rule catalog: exactly 60 ordered, distinct rule IDs required')
    return data


def validate(data):
    """Mandatory cross-record invariants. This does not pretend to implement full JSON Schema."""
    errors = []
    if not isinstance(data, dict) or data.get('schema') != 'wi.fiction.manuscript/v1':
        return ['schema must be wi.fiction.manuscript/v1']
    if not isinstance(data.get('work'), dict) or not data['work'].get('id') or not data['work'].get('title'):
        errors.append('work.id and work.title required')
    for field in ('scenes', 'characters', 'relationships', 'mysteries', 'motifs', 'world_rules', 'events', 'emotional_events', 'act_states', 'plants', 'interventions', 'assessments', 'waivers'):
        if field in data and not isinstance(data[field], list):
            errors.append(field + ' must be an array')
    if errors:
        return errors
    ids = {}
    for key in ('scenes', 'characters', 'relationships', 'mysteries', 'motifs', 'world_rules', 'events', 'emotional_events', 'plants', 'interventions'):
        vals = data.get(key, [])
        by = set()
        for i, obj in enumerate(vals):
            if not isinstance(obj, dict) or not isinstance(obj.get('id'), str) or not obj['id']:
                errors.append(f'{key}[{i}] needs nonempty id'); continue
            if obj['id'] in by: errors.append(f'{key}: duplicate id {obj["id"]}')
            by.add(obj['id'])
        ids[key] = by
    scenes = data.get('scenes', [])
    scene_orders = []
    for s in scenes:
        if not isinstance(s, dict) or not s.get('id'):continue
        if not isinstance(s.get('order'), int) or isinstance(s.get('order'), bool) or s['order'] < 1:
            errors.append(f'scene {s["id"]}: order must be positive integer')
        else: scene_orders.append(s['order'])
        for field in ('major_suspense', 'recovery'):
            if field in s and not isinstance(s[field], bool): errors.append(f'scene {s["id"]}: {field} must be boolean')
        if 'tension' in s and (type(s['tension']) is not int or not 0<=s['tension']<=5): errors.append(f'scene {s["id"]}: tension must be integer 0..5')
        if 'power_uses' in s:
            for u in s['power_uses']:
                if u.get('rule_id') not in ids['world_rules']:errors.append(f'scene {s["id"]}: unknown world rule {u.get("rule_id")}')
    if len(scene_orders) != len(set(scene_orders)):errors.append('scene.order values must be unique')
    lookup = {s['id']:s['order'] for s in scenes if isinstance(s, dict) and s.get('id') in ids['scenes'] and isinstance(s.get('order'), int)}
    for key, keys in [('mysteries', ('raised_scene','resolution_scene')), ('plants', ('scene_id','payoff_scene')), ('interventions', ('scene_id',)), ('events',('scene_id',)), ('emotional_events',('scene_id',))]:
        for o in data.get(key, []):
            for f in keys:
                if o.get(f) is not None and o.get(f) not in ids['scenes']:errors.append(f'{key} {o["id"]}: {f} points to unknown scene')
        if key=='plants':
            for p in data.get(key,[]):
                if p.get('payoff_scene') and p.get('scene_id') in lookup and p['payoff_scene'] in lookup and lookup[p['payoff_scene']] < lookup[p['scene_id']]:
                    errors.append(f'plant {p["id"]}: payoff precedes plant in reading order (use explicit nonlinear payoff semantics if intended)')
    for ev in data.get('emotional_events',[]):
        for sid in ev.get('residue_scene_ids',[]):
            if sid not in ids['scenes']:errors.append(f'emotional event {ev["id"]}: residue points to unknown scene {sid}')
    for c in data.get('characters', []):
        for k in ('key_choice_scene_ids','appears_in'):
            for scene_id in c.get(k, []):
                if scene_id not in ids['scenes']:errors.append(f'character {c["id"]}: {k} unknown {scene_id}')
    for rel in data.get('relationships', []):
        for actor in rel.get('actors', []):
            if actor not in ids['characters']:errors.append(f'relationship {rel["id"]}: unknown actor {actor}')
        for state in rel.get('states', []):
            if state.get('scene_id') not in ids['scenes']:errors.append(f'relationship {rel["id"]}: state unknown scene')
    for rule in data.get('world_rules', []):
        for scene_id in rule.get('demonstrated_in',[]):
            if scene_id not in ids['scenes']:errors.append(f'world rule {rule["id"]}: demonstration unknown scene')
    valid_rules = {f'FI-{i:02d}' for i in range(1,61)}
    for a in data.get('assessments', []):
        if a.get('rule_id') not in valid_rules:errors.append(f'assessment: unknown rule {a.get("rule_id")}')
        if a.get('verdict') not in ('pass','concern','fail','not_applicable'):errors.append('assessment verdict must be pass/concern/fail/not_applicable')
        if a.get('reviewer_type') not in ('human','model'):errors.append('assessment reviewer_type must be human or model')
        if not a.get('reviewer') or not a.get('evidence_refs') or not a.get('rationale'):
            errors.append('assessment needs reviewer, evidence_refs, rationale')
    for w in data.get('waivers', []):
        if w.get('rule_id') not in valid_rules or not w.get('rationale') or not w.get('actor') or not w.get('evidence_refs'):
            errors.append('waiver requires known rule_id, actor, rationale, evidence_refs')
        if w.get('scope') != data.get('work',{}).get('id'):errors.append('waiver scope must bind exact work.id')
    return sorted(set(errors))


def finding(rule_id, status, reason, anchors=None, method='typed', severity='review'):
    return {'rule_id':rule_id,'status':status,'severity':severity,'method':method,'reason':reason,'anchors':sorted(set(str(x) for x in (anchors or [])))}


def text_signals(txt, options=None):
    """Conservative evidence-producing signals. Never infer metaphor meaning from a regex."""
    options = options or {}
    out=[]
    words = list(re.finditer(r"\b[\w’'-]+\b",txt, flags=re.UNICODE))
    if not words: return out
    sentence_parts = [p.strip() for p in re.split(r'(?<=[.!?])\s+',txt) if p.strip()]
    wcount=len(words)
    figuratives=list(re.finditer(r'\b(?:as if|like (?:a|an|the)|as (?:cold|hot|sharp|still) as)\b',txt,re.I))
    density=1000*len(figuratives)/wcount
    if wcount>=120 and density>options.get('figuration_signals_per_1000',22):
        out.append(finding('FI-01','SIGNAL',f'{len(figuratives)} possible comparison markers in {wcount} words ({density:.1f}/1k); false positives possible',[f'char:{m.start()}' for m in figuratives[:12]],method='heuristic'))
    # Repeat n-grams with meaningful non-stopword prefix, report locations not a pass/fail count.
    toks=[m.group(0).lower() for m in words]
    hits={}
    for n in (3,4,5):
        seq={}
        for i in range(len(toks)-n+1):
            k=' '.join(toks[i:i+n])
            if all(w in {'the','and','of','in','to','a','as','if','it','was'} for w in k.split()):continue
            seq.setdefault(k,[]).append(i)
        for k,pos in seq.items():
            if len(pos)>=options.get('repeated_ngram_min',4) and len({p//75 for p in pos})>=2:
                hits[k]=pos
    if hits:
        patterns=sorted(hits.items(),key=lambda kv:(-len(kv[1]),kv[0]))[:8]
        out.append(finding('FI-03','SIGNAL','Manuscript-wide repeated sequences (possible motif or accident): '+', '.join(f'{k} ×{len(v)}' for k,v in patterns),[f'word:{v[0]}' for _,v in patterns],method='heuristic'))
    lengths=[len(re.findall(r'\b\w+\b', s)) for s in sentence_parts]
    if len(lengths)>=8:
        longest=0;current=0;previous=None
        for n in lengths:
            b='short' if n<=6 else 'long' if n>=22 else 'medium'
            current=current+1 if b==previous else 1
            longest=max(longest,current);previous=b
        if longest>=options.get('cadence_streak',8):
            out.append(finding('FI-08','SIGNAL',f'{longest} successive sentences in the same coarse length band; rhythm may be intentional',method='heuristic'))
    pats=[r'\bthis (?:was|is) the (?:moment|part|story)\b',r'\bthe reader (?:would|will|should) (?:never|always|now)\b',r'\bthis (?:changed|changes) everything\b']
    intrusion=[m for p in pats for m in re.finditer(p,txt,re.I)]
    if intrusion:
        out.append(finding('FI-09','SIGNAL','Potential unearned narration about its own effects',[f'char:{m.start()}' for m in intrusion],method='heuristic'))
    raw=list(re.finditer(r'(?:\\(?:frac|alpha|beta|begin\{|end\{|text\{|sum|times)\b|\uFFFD|\[\s*(?:INSERT|TODO|TBD)\s+[^\]]+\])',txt,re.I))
    if raw:
        out.append(finding('FI-55','SIGNAL','Potential raw math, encoding damage or placeholder requiring export inspection',[f'char:{m.start()}' for m in raw],method='heuristic'))
    return out


def typed_findings(data):
    out=[]
    scene=sorted(data.get('scenes',[]),key=lambda s:s.get('order',0))
    coverage=data.get('coverage',{})
    def add(n,reason,anchors,status='SIGNAL',severity='review'):
        out.append(finding(f'FI-{n:02d}',status,reason,anchors,'typed',severity))
    for m in data.get('motifs',[]):
        uses=m.get('uses',[])
        if len(uses)>=3 and len({u.get('meaning') for u in uses})==1 and not all(u.get('intentional') for u in uses):
            add(4,'Motif repetition has unchanged annotated meaning; author may defend artistic recurrence',[m['id']]+[u.get('scene_id','') for u in uses])
    for s in scene:
        if s.get('major_suspense') and not any(s.get(k) for k in ('new_danger','new_info','lost_options','consequences','state_deltas')):
            add(13,'Major suspense beat declares no consequential state delta; verify annotations and scene',[s['id']])
    for i in range(len(scene)-2):
        a=scene[i:i+3]
        if all(s.get('tension') is not None for s in a) and len({s.get('tension') for s in a})==1 and all(not s.get('state_deltas') for s in a):
            add(14,'Three adjacent scenes have same annotated tension and no declared turn',[s['id'] for s in a])
    for t in data.get('threats',[]):
        if t.get('major') and not t.get('proven_consequence_scene') and coverage.get('threats'):
            add(15,'Major threat has no documented concrete consequence',[t.get('id','threat')])
    for m in data.get('mysteries',[]):
        if m.get('importance')=='major' and not m.get('resolution_scene') and not m.get('deferred_reason') and coverage.get('mysteries'):
            add(19,'Major mystery has neither resolution nor defensible series deferral',[m['id'],m.get('raised_scene','')])
    for i in range(len(scene)-3):
        window=scene[i:i+4]
        if all(s.get('pressures') for s in window) and len(set.intersection(*(set(s['pressures']) for s in window)))>=1 and len(set.union(*(set(s['pressures']) for s in window)))==1:
            add(22,'Four scenes declare a single repeated pressure class',[s['id'] for s in window])
    if len(scene)>=5 and all(s.get('tension') is not None and s['tension']>=4 for s in scene) and not any(s.get('recovery') for s in scene):
        add(23,'No recovery segment across at least five high-tension annotated scenes',[s['id'] for s in scene])
    if coverage.get('characters'):
        for c in data.get('characters',[]):
            missing=[x for x in ('private_desire','history','contradiction') if not c.get(x)]
            if missing:add(25,'Character registry lacks independent human dimensions: '+', '.join(missing),[c['id']],'DATA_GAP')
            if not c.get('desire_conflict'):add(26,'No registered desire versus duty or loyalty conflict',[c['id']],'DATA_GAP')
    for rel in data.get('relationships',[]):
        states=rel.get('states',[])
        for i in range(1,len(states)):
            a,b=states[i-1],states[i]
            if a.get('trust')!=b.get('trust') and not b.get('cause'):
                add(29,'Trust changes without documented causal event',[rel['id'],b.get('scene_id','')],'DATA_GAP')
    if coverage.get('emotional_events'):
        for ev in data.get('emotional_events',[]):
            if ev.get('major') and not ev.get('residue_scene_ids') and not ev.get('intentional_absence'):
                add(30,'Major emotional event has no documented residue in later scenes',[ev.get('id','event'),ev.get('scene_id','')])
    act_states=data.get('act_states',[])
    if len(act_states)>=3 and coverage.get('act_states'):
        signatures=[(x.get('objective'),tuple(x.get('available_options',[])),tuple(x.get('known_facts',[])),x.get('stakes'),x.get('relationship_state')) for x in act_states]
        if len(set(signatures))==1:
            add(45,'Three or more acts preserve identical objective, options, information, stakes and relationships',[str(x.get('act')) for x in act_states])
    for tr in data.get('turning_points',[]):
        if tr.get('major') and not tr.get('character_choice_scene'):
            add(32,'Major turning point lacks linked character decision',[tr.get('id','turn')])
    rules={r['id']:r for r in data.get('world_rules',[])}
    for r in rules.values():
        if coverage.get('world_rules') and not (r.get('permits') or r.get('forbids')):
            add(35,'World rule specifies no ability boundaries',[r['id']],'DATA_GAP')
        if coverage.get('world_rules') and not r.get('demonstrated_in'):
            add(42,'World rule is not linked to an event demonstrating its consequence',[r['id']])
    for s in scene:
        for use in s.get('power_uses',[]):
            rule=rules.get(use.get('rule_id'))
            if rule and use.get('action') in rule.get('forbids',[]):
                add(36,'Canon-forbidden power use without recorded authorized retcon',[s['id'],rule['id']],'DEFECT','block')
            elif rule and use.get('action') not in rule.get('permits',[]):
                add(35,'Power operation neither explicitly permitted nor forbidden; knowledge gap, not automatic permission',[s['id'],rule['id']],'DATA_GAP')
    for event in data.get('interventions',[]):
        if event.get('requires_cost') and event.get('cost_paid') is False and not event.get('explicit_deferral'):
            add(37,'Intervention spends an explicit required cost without payment or deferral',[event['id'],event.get('scene_id','')],'DEFECT','block')
        elif event.get('requires_cost') and 'cost_paid' not in event and not event.get('explicit_deferral'):
            add(37,'Cost-bearing intervention has no payment/deferral annotation',[event['id'],event.get('scene_id','')],'DATA_GAP')
    for event in data.get('events',[]):
        if event.get('record_time') and event.get('story_time') and event['record_time']<event['story_time'] and not event.get('anticipatory_record'):
            add(40,'Record date precedes event date; verify prophecy, fraud, time travel, or clerical error',[event['id'],event.get('scene_id','')])
    by_act={}
    for s in scene:by_act.setdefault(str(s.get('act','')),[]).append(s)
    if len(by_act)>=2:
        acts=list(by_act.items())
        for i in range(1,len(acts)):
            prev=acts[i-1][1][-1];curr=acts[i][1][0]
            if prev.get('state_signature') and prev.get('state_signature')==curr.get('state_signature') and not curr.get('state_deltas'):
                add(46,'Act transition has no documented alteration of options, knowledge, or objective',[prev['id'],curr['id']])
    promises=data.get('work',{}).get('opening_promises',[])
    delivered=set(data.get('work',{}).get('delivered_promises',[]))
    if promises and coverage.get('ending'):
        for promise in promises:
            if promise not in delivered:add(48,'Opening promise not linked to delivered consequence',[str(promise)])
    for plant in data.get('plants',[]):
        if plant.get('payoff_scene') and not plant.get('consequence'):
            add(49,'Reappearance is recorded but consequential payoff has not been documented',[plant['id'],plant['payoff_scene']])
    if coverage.get('ending') and not data.get('work',{}).get('central_resolution'):
        add(51,'Book lacks documented standalone resolution of central conflict',[data.get('work',{}).get('id','work')])
    for f in ('title','edition','publisher','copyright'):
        if data.get('publication',{}).get('release_target') in ('print','ebook') and not data.get('publication',{}).get(f):
            add(56,'Required publication metadata absent: '+f,[f],'DEFECT','block')
    return out


def audit(data, text=None, options=None):
    errors=validate(data)
    rule_set=catalog()
    if text is not None:
        expected='sha256:'+hashlib.sha256(text.encode('utf-8')).hexdigest()
        for scene in data.get('scenes',[]):
            a=scene.get('anchor')
            if a:
                if a.get('source_digest')!=expected:
                    errors.append('scene '+scene['id']+': stale or wrong source_digest')
                start,end=a.get('start'),a.get('end')
                if not isinstance(start,int) or not isinstance(end,int) or start<0 or start>=end or end>len(text):
                    errors.append('scene '+scene['id']+': invalid text anchor offsets')
    raw=[] if errors else typed_findings(data)
    if text is not None:
        raw+=text_signals(text,options)
    assessments={}
    for a in data.get('assessments',[]):
        assessments.setdefault(a.get('rule_id'),[]).append(a)
    active_waivers={w['rule_id']:w for w in data.get('waivers',[]) if w.get('rule_id') and w.get('actor') and w.get('rationale')}
    by_rule={}
    for f in raw:by_rule.setdefault(f['rule_id'],[]).append(f)
    results=[]
    for r in rule_set['rules']:
        rid=r['id'];events=by_rule.get(rid,[]);judgments=assessments.get(rid,[])
        if rid in active_waivers:
            status='WAIVED' if not any(x['status']=='DEFECT' for x in events) else 'DEFECT'
        elif any(x['status']=='DEFECT' for x in events):status='DEFECT'
        elif any(x.get('verdict')=='fail' for x in judgments):status='EDITORIAL_FAIL'
        elif any(x['status']=='DATA_GAP' for x in events):status='DATA_GAP'
        elif any(x['status']=='SIGNAL' for x in events):status='SIGNAL'
        elif any(x.get('verdict')=='concern' for x in judgments):status='EDITORIAL_CONCERN'
        elif any(x.get('reviewer_type')=='human' and x.get('verdict')=='pass' for x in judgments):status='REVIEWED_PASS'
        elif any(x.get('verdict')=='not_applicable' and x.get('reviewer_type')=='human' for x in judgments):status='NOT_APPLICABLE'
        else:status='UNASSESSED'
        results.append({'id':rid,'title':r['title'],'status':status,'method':r['evaluation_method'],'events':events,'assessments':judgments,'waiver':active_waivers.get(rid)})
    report={'schema':'wi.fiction.audit/v1','work_id':data.get('work',{}).get('id'),'input_digest':digest(data),'catalog_digest':digest(rule_set),'text_digest':('sha256:'+hashlib.sha256(text.encode('utf-8')).hexdigest() if text is not None else None),'schema_errors':errors,'summary':dict(sorted(Counter(r['status'] for r in results).items())),'results':results,'assertion':'Machine findings establish only the supplied structural data and observed text patterns. No automated score proves artistic quality or reader experience.'}
    return report


def release_gate(data, report, study=None, mode='draft'):
    profiles=load_json(PROFILES_PATH)['profiles']
    if mode not in profiles:raise ValueError('unknown gate mode '+mode)
    p=profiles[mode];issues=[]
    if report['schema_errors']:
        issues.append({'type':'DEFECT','reason':'Invalid typed manuscript evidence','details':report['schema_errors']})
    for r in report['results']:
        if r['status']=='DEFECT':issues.append({'type':'DEFECT','reason':r['id']+' structural failure'})
        if r['status']=='EDITORIAL_FAIL':issues.append({'type':'HOLD','reason':r['id']+' documented editorial failure'})
    if mode in ('editorial','publication'):
        for rid in p['mandatory_review_rules']:
            item=next(x for x in report['results'] if x['id']==rid)
            if item['status'] not in ('REVIEWED_PASS','NOT_APPLICABLE'):
                issues.append({'type':'HOLD','reason':rid+' lacks resolved human editorial judgment; current '+item['status']})
    if mode=='publication':
        pub=data.get('publication',{})
        if pub.get('release_target') not in ('print','ebook'):
            issues.append({'type':'HOLD','reason':'Publication target print or ebook not declared'})
        for field in ('export_proof','pagination_review','metadata_review'):
            if not pub.get(field):issues.append({'type':'HOLD','reason':'No '+field+' evidence artifact'})
        if not isinstance(study,dict) or study.get('schema')!='wi.fiction.reader-study/v1':
            issues.append({'type':'HOLD','reason':'No reader-study contract supplied'})
        else:
            if study.get('work_id')!=data.get('work',{}).get('id'):issues.append({'type':'HOLD','reason':'Reader study belongs to another work'})
            if study.get('manuscript_digest')!=report.get('input_digest'):
                issues.append({'type':'HOLD','reason':'Reader study manuscript version does not match audit input'})
            if study.get('independent_readers',0)<p['min_independent_readers']:
                issues.append({'type':'HOLD','reason':'Independent reader sample below declared editorial policy'})
            if not study.get('methodology') or not study.get('findings') or not study.get('reconciliation'):
                issues.append({'type':'HOLD','reason':'Reader study missing method, findings or reconciliation'})
            if not study.get('consent_confirmed'):
                issues.append({'type':'HOLD','reason':'Reader study consent not attested'})
    verdict='BLOCK' if any(x['type']=='DEFECT' for x in issues) else 'HOLD' if issues else 'ELIGIBLE_FOR_HUMAN_DECISION'
    if mode=='draft' and verdict=='ELIGIBLE_FOR_HUMAN_DECISION':verdict='DRAFT_CHECKS_COMPLETE'
    return {'schema':'wi.fiction.gate/v1','mode':mode,'work_id':report.get('work_id'),'input_digest':report.get('input_digest'),'policy_digest':digest(load_json(PROFILES_PATH)),'verdict':verdict,'issues':issues,'note':'Eligibility is not publication or audience approval. A human with actual authority accepts release; the existing WI semantic runtime remains canonical.'}
