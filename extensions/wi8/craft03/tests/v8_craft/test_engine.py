"""Structural, negative, adversarial, rights, bitemporal, genre counterexamples.
Run: python3 -m unittest discover -s tests/v8_craft -v
"""
import copy,json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from craft_v8.engine import evaluate,digest
SRC=json.loads((ROOT/'tests/v8_craft/fixtures/valid_quiet_mixed_victory.json').read_text())

def trial(mutate):
    data=copy.deepcopy(SRC);mutate(data);return evaluate(data)

def findings(report):return {f['code'] for f in report['findings']}

class PackageTests(unittest.TestCase):
    def test_positive(self):
        r=evaluate(SRC);self.assertEqual(r['structural_verdict'],'PASS');self.assertEqual(r['counts']['total'],0)
        self.assertEqual(r['publication_verdict'],'HOLD')
    def test_no_mutation(self):
        before=copy.deepcopy(SRC);evaluate(SRC);self.assertEqual(before,SRC)
    def test_deterministic(self):self.assertEqual(evaluate(SRC),evaluate(copy.deepcopy(SRC)))
    def test_reordered_keys_same_digest(self):self.assertEqual(digest(SRC),digest(json.loads(json.dumps(SRC,sort_keys=True))))
    def test_6_genres(self):
        for genre in ('literary','mystery','horror','espionage','fantasy','scifi'):
            d=json.loads((ROOT/f'tests/v8_craft/fixtures/opening_{genre}.json').read_text())
            with self.subTest(genre=genre):self.assertEqual(evaluate(d)['counts']['errors'],0)
    def test_quiet_is_not_defect(self):self.assertNotIn('WI8-C03-DISCONNECTED-HOOK',findings(evaluate(SRC)))
    def test_three_layer_gate(self):
        d=copy.deepcopy(SRC);d['origin']='draft_projection';self.assertEqual(evaluate(d)['structural_verdict'],'PASS')
        self.assertEqual(evaluate(d)['editorial_verdict'],'NOT_MEASURED')
        self.assertEqual(evaluate(d)['publication_verdict'],'HOLD')
    def test_rule_register(self):
        reg=json.loads((ROOT/'rules/craft_c121_c180.json').read_text())
        self.assertEqual([r['id'] for r in reg['rules']],[f'C{x}' for x in range(121,181)])
        self.assertEqual(len({r['title'] for r in reg['rules']}),60)
        self.assertTrue(all(r['acceptance'] and r['source_pages'] and r['owner_existing_path'] for r in reg['rules']))
    def test_waves_only_planned(self):
        d=json.loads((ROOT/'plans/v8-craft03.proposal.json').read_text());self.assertEqual(len(d['waves']),12)
        self.assertTrue(all(x['status']=='planned' and x['upstream_receipt'] is None for x in d['waves']))
    def test_historical_knowledge_reconstruction(self):
        a=evaluate(SRC,known_at='2026-10-23T20:00:00Z')['knowledge_as_of']['outcome-archive']
        b=evaluate(SRC,known_at='2026-10-24T20:00:00Z')['knowledge_as_of']['outcome-archive']
        self.assertEqual(len(a),1);self.assertEqual(len(b),2)
        self.assertEqual(a[0],b[0]);self.assertIn('local victory',a[0]['interpretation'])
    def test_asof_offset_normalization(self):
        a=evaluate(SRC,known_at='2026-10-23T16:30:00Z')
        b=evaluate(SRC,known_at='2026-10-23T11:30:00-05:00')
        self.assertEqual(a['knowledge_as_of'],b['knowledge_as_of'])
    def test_no_reader_causality_claim(self):self.assertIn('reader_emotional_effect',evaluate(SRC)['claims_not_established'])

# Each of these checks has a positive counterpart in the clean base fixture.
NEGATIVE_CASES=[
 ('schema',lambda d:d.update(schema='wi8.craft.projection/v0'),'WI8-C03-SCHEMA'),
 ('untrusted_canonical',lambda d:d.update(origin='canonical_export'),'WI8-C03-TRUST'),
 ('lie_commit',lambda d:d.update(canon_committed=True),'WI8-C03-FALSE-CLAIM'),
 ('lie_publication',lambda d:d.update(publication_ready=True),'WI8-C03-FALSE-CLAIM'),
 ('events_not_list',lambda d:d.update(events={}),'WI8-C03-TYPE'),
 ('duplicate_event',lambda d:d['events'].append(copy.deepcopy(d['events'][0])),'WI8-C03-DUPLICATE'),
 ('missing_event_id',lambda d:d['events'][0].pop('id'),'WI8-C03-ID'),
 ('missing_cause',lambda d:d['events'][1].update(causes=['not-exist']),'WI8-C03-EVENT-LINK'),
 ('causal_cycle',lambda d:d['events'][0].update(causes=['ev-5']),'WI8-C03-EVENT-CYCLE'),
 ('nonint_order',lambda d:d['events'][0].update(order='zero'),'WI8-C03-ORDER'),
 ('broken_event_time',lambda d:d['events'][1].update(known_at='not-a-date'),'WI8-C03-TIME'),
 ('scene_missing_event',lambda d:d['scenes'][2].update(event_id='bad'),'WI8-C03-SCENE-EVENT'),
 ('opening_missing_scene',lambda d:d['opening'].update(scene_id='bad'),'WI8-C03-OPENING-SCENE'),
 ('promise_missing_payoff',lambda d:d['opening']['promises'][0].pop('payoff_scene'),'WI8-C03-PROMISE-DEBT'),
 ('promise_broken_payoff',lambda d:d['opening']['promises'][0].update(payoff_scene='bad'),'WI8-C03-PAYOFF'),
 ('clue_missing_scene',lambda d:d['opening']['clues'][0].update(exposed_scene='bad'),'WI8-C03-CLUE-LINK'),
 ('retroactive_clue',lambda d:d['opening']['clues'][0].update(retroactively_inserted=True),'WI8-C03-UNFAIR-CLUE'),
 ('nonlinear_no_contract',lambda d:d['opening'].update(nonlinear=True),'WI8-C03-NONLINEAR-DISCLOSURE'),
 ('falsehood',lambda d:d['opening']['misdirections'][0].update(kind='authorial_falsehood'),'WI8-C03-UNFAIR-NARRATOR'),
 ('spectacle_only',lambda d:d['opening'].update(spectacle=True,causal_anchor_ids=[]),'WI8-C03-DISCONNECTED-HOOK'),
 ('custom_opening',lambda d:d['opening'].update(strategies=['new invented method']),'WI8-C03-CUSTOM-STRATEGY'),
 ('fight_scene',lambda d:d['fights'][0].update(scene_id='bad'),'WI8-C03-FIGHT-LINK'),
 ('bad_space_edge',lambda d:d['spaces'][0]['edges'].append(['desk','void']),'WI8-C03-SPACE-EDGE'),
 ('actor_outside',lambda d:d['fights'][0]['actors'][0].update(position='void'),'WI8-C03-START-POS'),
 ('actor_bad_dest',lambda d:d['fights'][0]['beats'][0].update(to='void'),'WI8-C03-GEOMETRY'),
 ('impossible_move',lambda d:d['fights'][0]['beats'][0].update(to='stairs'),'WI8-C03-IMPOSSIBLE-MOVE'),
 ('limited_pov',lambda d:(d['spaces'][0].update(sight_lines=[]),d['fights'][0]['beats'][0].update(to='desk')),'WI8-C03-OMNISCIENCE'),
 ('overspent_ammo',lambda d:d['fights'][0]['beats'][0].update(resource_delta={'ammo':-3}),'WI8-C03-RESOURCE-NEGATIVE'),
 ('unearned_fatigue_reset',lambda d:d['fights'][0]['beats'][0].update(resource_delta={'stamina':+2}),'WI8-C03-UNEARNED-RECOVERY'),
 ('actor_unknown_resource',lambda d:d['fights'][0]['beats'][0].update(resource_delta={'supplies':-1}),'WI8-C03-UNKNOWN-RESOURCE'),
 ('beat_unknown_actor',lambda d:d['fights'][0]['beats'][0].update(actor='ghost'),'WI8-C03-BEAT-ACTOR'),
 ('resource_float',lambda d:d['fights'][0]['beats'][0].update(resource_delta={'ammo':-1.5}),'WI8-C03-RESOURCE-TYPE'),
 ('unadapted_move',lambda d:d['fights'][0]['beats'].append({'id':'b-3','actor':'ava','move':'sidestep','to':'hall'}),'WI8-C03-REPEAT-MOVE'),
 ('unearned_twist',lambda d:d['fights'][0]['beats'][0].update(twist=True),'WI8-C03-UNEARNED-TWIST'),
 ('empty_action',lambda d:d['fights'][0].update(resulting_changes=[]),'WI8-C03-EMPTY-ACTION'),
 ('harm_erasure',lambda d:d['opposition']['forces'][0].update(sympathetic=True,harm_refs=['harm-1'],harm_accounted=False),'WI8-C03-HARM-ERASURE'),
 ('forced_villain',lambda d:d['opposition']['forces'][0].update(requires_villain=True),'WI8-C03-FORCED-VILLAIN'),
 ('omniscient_plan',lambda d:d['opposition']['plans'][0]['steps'][0]['choice_dependencies'][0].pop('contingency_id'),'WI8-C03-OMNISCIENT-PLAN'),
 ('unproven_robust',lambda d:d['opposition']['plans'][0].update(claimed_robust=True,alternative_responses=[]),'WI8-C03-UNTESTED-PLAN'),
 ('unknown_pledge',lambda d:d['suspense']['pledges'][0].update(raised_scene='bad'),'WI8-C03-PLEDGE-SCENE'),
 ('unpaid_pledge',lambda d:d['suspense']['pledges'][0].pop('payoff_scene'),'WI8-C03-UNPAID-PLEDGE'),
 ('empty_payoff',lambda d:d['suspense']['pledges'][0].update(payoff_evidence=[]),'WI8-C03-EMPTY-PAYOFF'),
 ('promise_invalid_scene',lambda d:d['suspense']['pledges'][0].update(payoff_scene='bad'),'WI8-C03-PLEDGE-PAYOFF'),
 ('unlearned_knowledge',lambda d:d['suspense']['beats'][0]['used_knowledge']['ava'].append('secret'),'WI8-C03-UNLEARNED-FACT'),
 ('false_countdown',lambda d:d['suspense']['clocks'][0].update(expiry_condition=''),'WI8-C03-EMPTY-CLOCK'),
 ('static_dialogue',lambda d:d['suspense']['dialogue'][0].update(resulting_change=''),'WI8-C03-STATIC-DIALOGUE'),
 ('bad_parent',lambda d:d['goals'][1].update(parent_id='none'),'WI8-C03-GOAL-PARENT'),
 ('goal_cycle',lambda d:d['goals'][0].update(parent_id='goal-archive'),'WI8-C03-GOAL-CYCLE'),
 ('new_goal_uncausal',lambda d:d['goals'][1].update(replaces_id='goal-book'),'WI8-C03-GOAL-REPLACEMENT'),
 ('outcome_bad_ref',lambda d:d['outcomes'][0].update(goal_id='none'),'WI8-C03-OUTCOME-LINK'),
 ('cost_negative',lambda d:d['outcomes'][0].update(resource_cost=-3),'WI8-C03-OUTCOME-VECTOR'),
 ('history_collision',lambda d:d['outcomes'][0]['interpretations'][1].update(known_at='2026-10-23T11:00:00-05:00'),'WI8-C03-KNOWLEDGE-HISTORY'),
 ('history_invalid_date',lambda d:d['outcomes'][0]['interpretations'][0].update(known_at='yesterday'),'WI8-C03-INTERPRET-TIME'),
 ('unknown_reveal',lambda d:d['outcomes'][0]['interpretations'][1].update(revealed_by_event='void'),'WI8-C03-REVEAL-EVENT'),
 ('twist_missing_condition',lambda d:d['twists'][0].update(required_event_ids=[]),'WI8-C03-TWIST-PRECONDITION'),
 ('twist_false_ref',lambda d:d['twists'][0].update(required_event_ids=['bad']),'WI8-C03-TWIST-REF'),
 ('twist_claim_untested',lambda d:d['twists'][0].update(guaranteed=True,counterfactuals=[]),'WI8-C03-UNTESTED-TWIST'),
 ('dated_realworld',lambda d:d['references'][0].update(kind='real_world'),'WI8-C03-SOURCE-HYGIENE'),
 ('freshness_unstated',lambda d:d['references'][0].update(kind='real_world',claims_current=True),'WI8-C03-FRESHNESS'),
 ('copyright_unreviewed',lambda d:d['references'][0].update(used_verbatim=True,rights_status='unknown'),'WI8-C03-RIGHTS'),
 ('adapt_missing_scene',lambda d:d['adaptations'][0].update(target_scene='none'),'WI8-C03-ADAPT-SCENE'),
 ('adapt_change_meaning',lambda d:d['adaptations'][0].update(target_meaning_ids=['different-meaning']),'WI8-C03-SEMANTIC-LOSS'),
 ('adapt_unknown_medium',lambda d:d['adaptations'][0].update(medium='unknown'),'WI8-C03-MEDIUM'),
 ('asof_bad',lambda d:d.update(dummy=True),'WI8-C03-ASOF-TIME'),
]

def build_case(name,change,code):
    def run(self):
        d=copy.deepcopy(SRC);change(d)
        r=evaluate(d,known_at='invalid' if name=='asof_bad' else None)
        self.assertIn(code,findings(r),msg=f'{name} expected {code}; got {findings(r)}')
    return run

for name,change,code in NEGATIVE_CASES:
    setattr(PackageTests,'test_negative_'+name,build_case(name,change,code))

class CLITests(unittest.TestCase):
    def command(self,*args):return subprocess.run([sys.executable,str(ROOT/'scripts/wi-craft.py'),*args],cwd=ROOT,text=True,capture_output=True)
    def test_evaluate(self):
        r=self.command('evaluate','--input','tests/v8_craft/fixtures/valid_quiet_mixed_victory.json')
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout)['structural_verdict'],'PASS')
    def test_gate_refuses_publication(self):
        r=self.command('gate','--input','tests/v8_craft/fixtures/valid_quiet_mixed_victory.json','--stage','publication')
        self.assertEqual(r.returncode,3)
    def test_gate_refuses_editorial(self):
        r=self.command('gate','--input','tests/v8_craft/fixtures/valid_quiet_mixed_victory.json','--stage','editorial')
        self.assertEqual(r.returncode,3)
    def test_mechanical_gate_only(self):
        r=self.command('gate','--input','tests/v8_craft/fixtures/valid_quiet_mixed_victory.json','--stage','mechanical')
        self.assertEqual(r.returncode,0)
    def test_unknown_rule(self):self.assertNotEqual(self.command('rules','--id','C181').returncode,0)
    def test_known_rule(self):
        r=self.command('rules','--id','C174');self.assertEqual(json.loads(r.stdout)['id'],'C174')
    def test_asof(self):
        r=self.command('as-of','--input','tests/v8_craft/fixtures/valid_quiet_mixed_victory.json','--known-at','2026-10-23T20:00:00Z')
        self.assertEqual(len(json.loads(r.stdout)['knowledge_as_of']['outcome-archive']),1)
    def test_invalid_json_is_block(self):
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(mode='w',suffix='.json') as f:
            f.write('{');f.flush();self.assertEqual(self.command('evaluate','--input',f.name).returncode,2)

if __name__=='__main__': unittest.main()
