"""Writing Intelligence v8 Craft 03: deterministic *read-only projection evaluator*.

Never stores or mutates canon. It accepts synthetic fixtures/draft annotations,
NOT an attested export from the canonical v6 graph. Upstream adapters must be
implemented and separately verified before this is promoted to the canonical
runtime. All literary judgments are review signals rather than machine proof.
Python 3.8+ stdlib. No I/O aside from callers passing parsed objects.
"""
import copy
import datetime as dt
import hashlib
import json

SCHEMA = 'wi8.craft.projection/v1'
ORIGINS = ('fixture', 'draft_projection')
STRATEGIES = ('character_entrance','antagonist_entrance','relationship','catalyst','in_medias_res',
 'flashback','flashforward','dream','puzzle','quiet_power','parallel_action','iconic_moment',
 'concealed_clue','custom','none')
SEVERITIES = ('error','review','hold')
KINDS = ('mechanical_consistency','causal_integrity','craft_diagnosis','human_evaluation','provenance')
DOMAIN_KEYS = ('events','scenes','opening','fights','spaces','opposition','suspense','goals',
               'outcomes','twists','references','adaptations','reader_reviews')


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)


def digest(obj):
    return 'sha256:' + hashlib.sha256(canonical(obj).encode('utf-8')).hexdigest()


def _time(value):
    if not isinstance(value,str):
        raise ValueError('time must be ISO-8601 string')
    try:
        x=dt.datetime.fromisoformat(value.replace('Z','+00:00'))
    except ValueError:
        raise ValueError('time must be ISO-8601')
    if x.tzinfo is None or x.utcoffset() is None:
        raise ValueError('time needs explicit timezone offset')
    return x.astimezone(dt.timezone.utc)


def _ids(items, kind, issue):
    result={}
    for i, item in enumerate(items):
        if not isinstance(item,dict):
            issue('error','WI8-C03-TYPE', kind, 'record is not an object',str(i))
            continue
        id_=item.get('id')
        if not isinstance(id_,str) or not id_.strip():
            issue('error','WI8-C03-ID',kind,'record requires nonempty id',str(i));continue
        if id_ in result:
            issue('error','WI8-C03-DUPLICATE',kind,'duplicate id within record family',id_)
        result[id_]=item
    return result


def _cycles(graph):
    """Iterative DFS; no recursion overflow on adversarial deep input."""
    state={}
    for root in graph:
        if state.get(root)==2:continue
        stack=[(root,False)]
        while stack:
            node,completed=stack.pop()
            if completed:
                state[node]=2
                continue
            if state.get(node)==2:continue
            if state.get(node)==1:return True
            state[node]=1
            stack.append((node,True))
            for dep in reversed(graph.get(node,[])):
                if dep not in graph:continue
                if state.get(dep)==1:return True
                if state.get(dep)!=2:stack.append((dep,False))
    return False


def _shapes(data,issue):
    """Fail closed for malformed nested containers; no heuristic prose inference."""
    families={
       'opening':('promises','clues','misdirections'),
       'opposition':('forces','plans'),
       'suspense':('pledges','beats','clocks','dialogue'),
    }
    for domain,names in families.items():
        node=data.get(domain,{})
        for k in names:
            value=node.get(k,[])
            if not isinstance(value,list) or any(not isinstance(x,dict) for x in value):
                issue('error','WI8-C03-NESTED-TYPE',domain,k+' must be an array of objects')
    for field in ('events','scenes','spaces','fights','goals','outcomes','twists','references','adaptations','reader_reviews'):
        if any(not isinstance(x,dict) for x in data.get(field,[])):
            issue('error','WI8-C03-NESTED-TYPE',field,'records must be JSON objects')
    for fight in data.get('fights',[]):
        for k in ('actors','beats'):
            if not isinstance(fight.get(k,[]),list) or any(not isinstance(x,dict) for x in fight.get(k,[])):
                issue('error','WI8-C03-NESTED-TYPE','action',k+' requires object records',fight.get('id',''))
    for goal in data.get('outcomes',[]):
        v=goal.get('interpretations',[])
        if not isinstance(v,list) or any(not isinstance(x,dict) for x in v):
            issue('error','WI8-C03-NESTED-TYPE','sequence','interpretations require objects',goal.get('id',''))
    for plan in data.get('opposition',{}).get('plans',[]):
        if not isinstance(plan.get('steps',[]),list) or any(not isinstance(x,dict) for x in plan.get('steps',[])):
            issue('error','WI8-C03-NESTED-TYPE','opposition','plan steps require objects',plan.get('id',''))
        else:
            for step in plan.get('steps',[]):
                if not isinstance(step.get('choice_dependencies',[]),list) or any(not isinstance(x,dict) for x in step.get('choice_dependencies',[])):
                    issue('error','WI8-C03-NESTED-TYPE','opposition','choice dependencies require objects',step.get('id',''))
    # Nested values used as dictionary keys or iterable tuples must be checked
    # before computing graph deltas. A malformed JSON object is a BLOCK, never
    # an uncaught TypeError from inside the evaluator.
    for field in ('events','scenes','spaces','fights','goals','outcomes','twists','references','adaptations','reader_reviews'):
        for rec in data.get(field,[]):
            for key in ('id',):
                if key in rec and not isinstance(rec[key],str):
                    issue('error','WI8-C03-NESTED-TYPE',field,'ID must be a string',str(key))
    for e in data.get('events',[]):
        if not isinstance(e.get('causes',[]),list) or any(not isinstance(x,str) for x in e.get('causes',[])):
            issue('error','WI8-C03-NESTED-TYPE','events','causes must be string identifiers')
    for s in data.get('scenes',[]):
        if not isinstance(s.get('event_id'),str):
            issue('error','WI8-C03-NESTED-TYPE','scenes','event_id must be string',s.get('id',''))
    o=data.get('opening',{})
    for k in ('strategies','causal_anchor_ids'):
        if not isinstance(o.get(k,[]),list) or any(not isinstance(x,str) for x in o.get(k,[])):
            issue('error','WI8-C03-NESTED-TYPE','opening',k+' must be array of strings')
    for k in ('promises','clues','misdirections'):
        for row in o.get(k,[]):
            for f in ('payoff_scene','exposed_scene','revealed_scene','kind'):
                if f in row and row[f] is not None and not isinstance(row[f],str):
                    issue('error','WI8-C03-NESTED-TYPE','opening',f+' must be string')
    for sp in data.get('spaces',[]):
        if not isinstance(sp.get('nodes',[]),list) or any(not isinstance(x,str) for x in sp.get('nodes',[])):
            issue('error','WI8-C03-NESTED-TYPE','action','space nodes require string IDs',sp.get('id',''))
        for k in ('edges','sight_lines'):
            if not isinstance(sp.get(k,[]),list) or any(not isinstance(x,list) or len(x)!=2 or any(not isinstance(y,str) for y in x) for x in sp.get(k,[])):
                issue('error','WI8-C03-NESTED-TYPE','action',k+' must contain string pairs',sp.get('id',''))
    for f in data.get('fights',[]):
        for actor in f.get('actors',[]):
            if not isinstance(actor.get('id'),str) or not isinstance(actor.get('position'),str) or not isinstance(actor.get('resources',{}),dict):
                issue('error','WI8-C03-NESTED-TYPE','action','actor ID, position and resources malformed',f.get('id',''))
        for beat in f.get('beats',[]):
            if not isinstance(beat.get('actor'),str) or ('to' in beat and not isinstance(beat.get('to'),str)):
                issue('error','WI8-C03-NESTED-TYPE','action','beat actor or destination malformed',f.get('id',''))
            if not isinstance(beat.get('resource_delta',{}),dict):
                issue('error','WI8-C03-NESTED-TYPE','action','resource deltas must be object',f.get('id',''))
            if not isinstance(beat.get('perceived_by',[]),list) or any(not isinstance(x,str) for x in beat.get('perceived_by',[])):
                issue('error','WI8-C03-NESTED-TYPE','action','perceived_by must be actor names',f.get('id',''))
    for goal in data.get('goals',[]):
        for field in ('parent_id','replaces_id','cause_event'):
            if field in goal and goal[field] is not None and not isinstance(goal[field],str):
                issue('error','WI8-C03-NESTED-TYPE','sequence','goal reference must be string',goal.get('id',''))
    for outcome in data.get('outcomes',[]):
        for note in outcome.get('interpretations',[]):
            if not isinstance(note.get('observer'),str) or not isinstance(note.get('known_at'),str):
                issue('error','WI8-C03-NESTED-TYPE','sequence','interpretation needs observer and clock',outcome.get('id',''))
    # Malformed record shapes must be fixed before checking causality.


def evaluate(data, known_at=None):
    """Recompute a deterministic report, leaving input unchanged. No remote reads."""
    findings=[]
    def issue(sev,code,domain,message,ref='', req=None):
        findings.append({'severity':sev,'code':code,'dimension':domain,'message':message,
                         'record':ref,'requirement':req})
    if not isinstance(data,dict):
        issue('error','WI8-C03-TYPE','envelope','Input must be JSON object')
        return _finish({},findings)
    if data.get('schema')!=SCHEMA:
        issue('error','WI8-C03-SCHEMA','envelope','Unknown projection schema',str(data.get('schema')))
    if data.get('origin') not in ORIGINS:
        issue('error','WI8-C03-TRUST','envelope','Reject canonical export claims: no trusted core adapter exists',str(data.get('origin')))
    if data.get('publication_ready') or data.get('canon_committed'):
        issue('error','WI8-C03-FALSE-CLAIM','envelope','Projection cannot certify publication or canonical commit')
    for k in DOMAIN_KEYS:
        if k in data and not isinstance(data[k], (dict if k in ('opening','opposition','suspense') else list)):
            issue('error','WI8-C03-TYPE',k,'Invalid domain container type')
    if any(f['severity']=='error' and f['code']=='WI8-C03-TYPE' for f in findings):
        return _finish(data,findings)
    _shapes(data,issue)
    if any(f['severity']=='error' and f['code']=='WI8-C03-NESTED-TYPE' for f in findings):
        return _finish(data,findings)
    events=_ids(data.get('events',[]),'events',issue)
    scenes=_ids(data.get('scenes',[]),'scenes',issue)
    spaces=_ids(data.get('spaces',[]),'spaces',issue)
    fights=_ids(data.get('fights',[]),'fights',issue)
    goals=_ids(data.get('goals',[]),'goals',issue)
    outcomes=_ids(data.get('outcomes',[]),'outcomes',issue)
    twists=_ids(data.get('twists',[]),'twists',issue)
    sources=_ids(data.get('references',[]),'references',issue)
    adaptations=_ids(data.get('adaptations',[]),'adaptations',issue)
    _ids(data.get('reader_reviews',[]),'reader_reviews',issue)
    if any(f['severity']=='error' and f['code'] in ('WI8-C03-ID','WI8-C03-DUPLICATE','WI8-C03-TYPE') for f in findings):
        return _finish(data,findings)

    for e in events.values():
        for p in e.get('causes',[]):
            if p not in events:issue('error','WI8-C03-EVENT-LINK','events','Unknown causal predecessor',e['id'],'C173')
            elif (isinstance(e.get('order'),int) and isinstance(events[p].get('order'),int)
                  and events[p]['order']>=e['order']):
                issue('error','WI8-C03-CAUSAL-ORDER','events','Causal predecessor may not occur at or after its consequence in world order',e['id'],'C173')
        if 'known_at' in e:
            try:_time(e['known_at'])
            except ValueError:issue('error','WI8-C03-TIME','events','Malformed knowledge timestamp',e['id'],'C170')
        if not isinstance(e.get('order'),int) or isinstance(e.get('order'),bool) or e['order']<0:
            issue('error','WI8-C03-ORDER','events','Event requires nonnegative integer world-order rank',e['id'],'C170')
    if _cycles({e['id']:e.get('causes',[]) for e in events.values()}):
        issue('error','WI8-C03-EVENT-CYCLE','events','Causal event graph is cyclic','','C173')
    for s in scenes.values():
        if s.get('event_id') not in events:issue('error','WI8-C03-SCENE-EVENT','scenes','Scene refers to nonexistent event',s['id'])
    opening=data.get('opening',{})
    for s in opening.get('strategies',[]):
        if s not in STRATEGIES:issue('review','WI8-C03-CUSTOM-STRATEGY','opening','Unrecognized strategy, treat as custom rather than failing',s,'C121')
    if opening:
        o_scene=opening.get('scene_id')
        if o_scene not in scenes:issue('error','WI8-C03-OPENING-SCENE','opening','Opening scene is not declared',str(o_scene),'C121')
        for p in opening.get('promises',[]):
            if not isinstance(p,dict):issue('error','WI8-C03-TYPE','opening','Promise must be object');continue
            if p.get('payoff_scene') is None and not p.get('deliberate_defer'):
                issue('review','WI8-C03-PROMISE-DEBT','opening','Opening promise has no payoff or declared deferral',p.get('id',''),'C124')
            if p.get('payoff_scene') is not None and p['payoff_scene'] not in scenes:
                issue('error','WI8-C03-PAYOFF','opening','Promise payoff references unknown scene',p.get('id',''),'C124')
        for clue in opening.get('clues',[]):
            if not isinstance(clue,dict):issue('error','WI8-C03-TYPE','opening','Clue must be object');continue
            if clue.get('exposed_scene') not in scenes or clue.get('revealed_scene') not in scenes:
                issue('error','WI8-C03-CLUE-LINK','opening','Clue requires existing exposure and reveal scenes',clue.get('id',''),'C130')
            elif (scenes[clue['exposed_scene']].get('event_id') in events and
                  scenes[clue['revealed_scene']].get('event_id') in events and
                  isinstance(events[scenes[clue['exposed_scene']]['event_id']].get('order'), int) and
                  isinstance(events[scenes[clue['revealed_scene']]['event_id']].get('order'), int) and
                  events[scenes[clue['exposed_scene']]['event_id']]['order'] > events[scenes[clue['revealed_scene']]['event_id']]['order'] and
                  not clue.get('nonlinear_order')):
                issue('review','WI8-C03-CLUE-ORDER','opening','Reveal precedes exposure in world time; verify nonlinear intent',clue.get('id',''),'C130')
            if clue.get('retroactively_inserted'):
                issue('error','WI8-C03-UNFAIR-CLUE','opening','A retroactively inserted clue cannot prove a fair twist',clue.get('id',''),'C130')
        for m in opening.get('misdirections',[]):
            if m.get('kind') not in ('character_belief','misleading_image','unreliable_speaker','authorial_falsehood'):
                issue('error','WI8-C03-MISDIRECTION','opening','Misdirection requires a valid origin-of-belief class',m.get('id',''),'C131')
            if m.get('kind')=='authorial_falsehood' and not m.get('intentional_unreliability'):
                issue('review','WI8-C03-UNFAIR-NARRATOR','opening','Unjustified authorial falsehood threatens fair reader contract',m.get('id',''),'C131')
        if opening.get('nonlinear') and not opening.get('disclosure_contract'):
            issue('review','WI8-C03-NONLINEAR-DISCLOSURE','opening','Nonlinear entry needs an authored perspective/time disclosure contract',o_scene,'C126')
        if opening.get('quiet'):
            pass # Quiet openings are valid. No arbitrary violence or spectacle requirement.
        if not opening.get('causal_anchor_ids') and opening.get('spectacle'):
            issue('review','WI8-C03-DISCONNECTED-HOOK','opening','Spectacular opening has no declared causal/theme payoff links',o_scene,'C122')

    for fight in fights.values():
        fid=fight['id'];space=spaces.get(fight.get('space_id'))
        if fight.get('scene_id') not in scenes or space is None:
            issue('error','WI8-C03-FIGHT-LINK','action','Fight requires known scene and space',fid,'C135');continue
        nodes=set(space.get('nodes',[]));edges=set()
        for x in space.get('edges',[]):
            if not isinstance(x,list) or len(x)!=2 or x[0] not in nodes or x[1] not in nodes:
                issue('error','WI8-C03-SPACE-EDGE','action','Space edge must connect declared nodes',space['id'],'C135')
            else:edges.add(tuple(x));edges.add((x[1],x[0]))
        los=set(map(tuple,space.get('sight_lines',[])))
        actors={a['id']:dict(a) for a in fight.get('actors',[]) if isinstance(a,dict) and 'id' in a}
        pos={a:p.get('position') for a,p in actors.items()};state={a:dict(p.get('resources',{})) for a,p in actors.items()}
        if len(actors)!=len(fight.get('actors',[])):
            issue('error','WI8-C03-COMBAT-ID','action','Combatant has missing or duplicate id',fid,'C134')
        for a,pools in state.items():
            for key,value in pools.items():
                if key not in ('ammo','stamina','supplies','mobility') or not isinstance(value,int) or isinstance(value,bool) or value<0:
                    issue('error','WI8-C03-INITIAL-RESOURCE','action','Initial resource pools require nonnegative integers',a,'C137')
        for a,p in pos.items():
            if p not in nodes:issue('error','WI8-C03-START-POS','action','Combatant starts outside space graph',a,'C135')
        seen_moves={}
        for beat in fight.get('beats',[]):
            bid=beat.get('id','?');actor=beat.get('actor')
            if actor not in pos:issue('error','WI8-C03-BEAT-ACTOR','action','Unknown combatant',bid,'C134');continue
            old=pos[actor]; dest=beat.get('to',old)
            if dest not in nodes:
                issue('error','WI8-C03-GEOMETRY','action','Destination outside scene geometry',bid,'C135')
            elif dest!=old and (old,dest) not in edges and not beat.get('canon_mobility_exception_ref'):
                issue('error','WI8-C03-IMPOSSIBLE-MOVE','action','Movement crosses disconnected locations',bid,'C135')
            else:pos[actor]=dest
            for perceived in beat.get('perceived_by',[]):
                if perceived not in pos:
                    issue('error','WI8-C03-POV','action','Unknown perceiver in sight claim',bid,'C136')
                elif perceived!=actor and (pos.get(perceived),pos.get(actor)) not in los and pos.get(perceived)!=pos.get(actor):
                    issue('error','WI8-C03-OMNISCIENCE','action','Sight claim violates declared visibility graph',bid,'C136')
            for key,delta in beat.get('resource_delta',{}).items():
                if key not in ('ammo','stamina','supplies','mobility') or not isinstance(delta,int) or isinstance(delta,bool):
                    issue('error','WI8-C03-RESOURCE-TYPE','action','Resource delta must be integer of known resource',bid,'C137');continue
                if key not in state[actor]:
                    issue('error','WI8-C03-UNKNOWN-RESOURCE','action','Actor has no initialized resource pool',bid,'C137');continue
                state[actor][key]+=delta
                if state[actor][key]<0:
                    issue('error','WI8-C03-RESOURCE-NEGATIVE','action','Resource consumed below zero',bid,'C137')
                if key=='stamina' and delta>0 and not beat.get('recovery_ref'):
                    issue('review','WI8-C03-UNEARNED-RECOVERY','action','Stamina recovery lacks causal anchor',bid,'C137')
            move=beat.get('move')
            if move:
                key=(actor,move)
                if key in seen_moves and not beat.get('adaptation_or_motif'):
                    issue('review','WI8-C03-REPEAT-MOVE','action','Repeated signature move lacks adaptation or declared callback',bid,'C139')
                seen_moves[key]=bid
            if beat.get('twist') and not beat.get('setup_ref'):
                issue('review','WI8-C03-UNEARNED-TWIST','action','Environmental twist requires established setup',bid,'C141')
        if not fight.get('resulting_changes'):
            issue('review','WI8-C03-EMPTY-ACTION','action','No consequence or character/plot change recorded for fight',fid,'C145')

    opposition=data.get('opposition',{})
    for force in opposition.get('forces',[]):
        if force.get('harm_refs') and force.get('sympathetic') and force.get('harm_accounted') is False:
            issue('review','WI8-C03-HARM-ERASURE','opposition','Sympathetic framing cannot erase recorded harms',force.get('id',''),'C154')
        if not force.get('archetypes') and force.get('requires_villain'):
            issue('review','WI8-C03-FORCED-VILLAIN','opposition','Antagonism need not be personified',force.get('id',''),'C146')
    for plan in opposition.get('plans',[]):
        pid=plan.get('id','')
        for step in plan.get('steps',[]):
            for c in step.get('choice_dependencies',[]):
                if c.get('independent_actor') and not c.get('established_control') and not c.get('contingency_id'):
                    issue('review','WI8-C03-OMNISCIENT-PLAN','opposition','Plan assumes one precise independent choice without fallback',step.get('id',pid),'C174')
        if plan.get('claimed_robust') and not plan.get('alternative_responses'):
            issue('review','WI8-C03-UNTESTED-PLAN','opposition','Robustness claim has no alternate-response cases',pid,'C171')

    suspense=data.get('suspense',{})
    for pledge in suspense.get('pledges',[]):
        pid=pledge.get('id','')
        if pledge.get('raised_scene') not in scenes:
            issue('error','WI8-C03-PLEDGE-SCENE','suspense','Pledge raised in unknown scene',pid,'C159')
        if pledge.get('payoff_scene') is not None and pledge['payoff_scene'] not in scenes:
            issue('error','WI8-C03-PLEDGE-PAYOFF','suspense','Pledge payoff references unknown scene',pid,'C159')
        if not pledge.get('payoff_scene') and not pledge.get('declared_carry'):
            issue('review','WI8-C03-UNPAID-PLEDGE','suspense','Open scene pledge has no payoff or deliberate carry',pid,'C159')
        if pledge.get('payoff_scene') and not pledge.get('payoff_evidence'):
            issue('review','WI8-C03-EMPTY-PAYOFF','suspense','Referenced scene alone does not establish causal payoff',pid,'C159')
    for beat in suspense.get('beats',[]):
        for actor,known in beat.get('actor_knowledge',{}).items():
            if not isinstance(known,list):
                issue('error','WI8-C03-KNOWLEDGE-TYPE','suspense','Knowledge record must be list',beat.get('id',''),'C161')
        for actor,items in beat.get('used_knowledge',{}).items():
            if not set(items).issubset(set(beat.get('actor_knowledge',{}).get(actor,[]))):
                issue('error','WI8-C03-UNLEARNED-FACT','suspense','Character acts on knowledge not in their state',beat.get('id',''),'C161')
    for clock in suspense.get('clocks',[]):
        if not clock.get('expiry_condition') or not clock.get('changes_choices'):
            issue('review','WI8-C03-EMPTY-CLOCK','suspense','Countdown lacks expiry semantics or choice consequence',clock.get('id',''),'C165')
    for exchange in suspense.get('dialogue',[]):
        if not exchange.get('tactic') or not exchange.get('resulting_change'):
            issue('review','WI8-C03-STATIC-DIALOGUE','suspense','Long conversation turn lacks declared tactical state change',exchange.get('id',''),'C160')

    gdep={}
    for goal in goals.values():
        parent=goal.get('parent_id');gdep[goal['id']]=[parent] if parent else []
        if parent and parent not in goals:
            issue('error','WI8-C03-GOAL-PARENT','sequence','Unknown parent goal',goal['id'],'C168')
        if goal.get('replaces_id') and (goal.get('replaces_id') not in goals or goal.get('cause_event') not in events):
            issue('error','WI8-C03-GOAL-REPLACEMENT','sequence','Replaced goal and its causal event must exist',goal['id'],'C172')
    if _cycles(gdep):issue('error','WI8-C03-GOAL-CYCLE','sequence','Goal hierarchy must be acyclic','','C168')
    for outcome in outcomes.values():
        oid=outcome['id']
        if outcome.get('goal_id') not in goals or outcome.get('event_id') not in events:
            issue('error','WI8-C03-OUTCOME-LINK','sequence','Outcome requires existing goal and event',oid,'C169')
        for k in ('resource_cost','relationship_cost','antagonist_benefit'):
            v=outcome.get(k)
            if v is not None and (not isinstance(v,(int,float)) or isinstance(v,bool) or v<0):
                issue('error','WI8-C03-OUTCOME-VECTOR','sequence','Outcome dimensions must be nonnegative numbers or unknown',oid,'C169')
        knowledge=outcome.get('interpretations',[])
        last_by_observer={}
        for note in knowledge:
            who=note.get('observer'); when=note.get('known_at')
            try:instant=_time(when)
            except ValueError:
                issue('error','WI8-C03-INTERPRET-TIME','sequence','Interpretation requires aware-time with timezone',oid,'C170');continue
            if who in last_by_observer and instant<=last_by_observer[who]:
                issue('error','WI8-C03-KNOWLEDGE-HISTORY','sequence','Observer history must be strictly increasing; past assertions never overwritten',oid,'C170')
            last_by_observer[who]=instant
            if note.get('revealed_by_event') not in (None,*events.keys()):
                issue('error','WI8-C03-REVEAL-EVENT','sequence','Reinterpretation references unrecorded reveal event',oid,'C170')
    for twist in twists.values():
        if not twist.get('required_event_ids'):
            issue('review','WI8-C03-TWIST-PRECONDITION','sequence','Major twist has no declared causal preconditions',twist['id'],'C173')
        for ev in twist.get('required_event_ids',[]):
            if ev not in events:issue('error','WI8-C03-TWIST-REF','sequence','Twist requires nonexistent event',twist['id'],'C173')
        if twist.get('guaranteed') and not twist.get('counterfactuals'):
            issue('review','WI8-C03-UNTESTED-TWIST','sequence','Guaranteed twist lacks alternatives/counterfactuals',twist['id'],'C173')

    for src in sources.values():
        if src.get('kind')=='real_world':
            for required in ('source_uri','effective_at','checked_at','rights_status'):
                if not src.get(required):
                    issue('review','WI8-C03-SOURCE-HYGIENE','provenance','Real-world reference lacks '+required,src['id'],'C179')
            if src.get('claims_current') and not src.get('freshness_policy'):
                issue('review','WI8-C03-FRESHNESS','provenance','Current claim requires explicit freshness policy',src['id'],'C179')
        if src.get('rights_status')=='unknown' and src.get('used_verbatim'):
            issue('review','WI8-C03-RIGHTS','provenance','Reproduced source expression needs licensing review',src['id'],'C178')
    for a in adaptations.values():
        if a.get('source_scene') not in scenes or a.get('target_scene') not in scenes:
            issue('error','WI8-C03-ADAPT-SCENE','adaptation','Adaptation uses unknown source/target scene',a['id'],'C180')
        if set(a.get('source_meaning_ids',[]))!=set(a.get('target_meaning_ids',[])):
            issue('review','WI8-C03-SEMANTIC-LOSS','adaptation','Adaptation meaning sets differ; investigate rather than auto-certify',a['id'],'C180')
        if a.get('medium') not in ('novel','screenplay','audio','comic','game','film','stage'):
            issue('review','WI8-C03-MEDIUM','adaptation','Unrecognized medium; needs adapter review',a['id'],'C180')
    if known_at:
        try:
            instant=_time(known_at)
            sliced={o['id']:[n for n in o.get('interpretations',[]) if _time(n['known_at'])<=instant]
                    for o in outcomes.values() if all(isinstance(n,dict) and n.get('known_at') for n in o.get('interpretations',[]))}
        except (ValueError,TypeError,KeyError):
            issue('error','WI8-C03-ASOF-TIME','sequence','Invalid as-of timestamp or broken history')
            sliced={}
    else:sliced=None
    return _finish(data,findings,sliced)


def _finish(data,findings,knowledge=None):
    findings.sort(key=lambda f:(SEVERITIES.index(f['severity']),f['dimension'],f['code'],str(f['record'])))
    errors=sum(f['severity']=='error' for f in findings)
    reviews=sum(f['severity']=='review' for f in findings)
    return {'schema':'wi8.craft.report/v1','input_digest':digest(data),
      'structural_verdict':'BLOCK' if errors else 'PASS',
      'editorial_verdict':'HOLD' if reviews or errors else 'NOT_MEASURED',
      'publication_verdict':'HOLD',
      'claims_not_established':['reader_emotional_effect','literary_excellence','upstream_canonical_integration','publication_readiness'],
      'counts':{'errors':errors,'review_signals':reviews,'total':len(findings)},'findings':findings,
      'knowledge_as_of':knowledge}
