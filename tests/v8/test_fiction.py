"""Deterministic unit, invariance, and adversarial controls for the proposed extension."""
import copy
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from fiction_v8.engine import audit, catalog, digest, load_json, release_gate, text_signals, validate


def fixture(name):return load_json(ROOT/'tests'/'v8'/'fixtures'/name)


class Contracts(unittest.TestCase):
    def setUp(self):self.base=fixture('valid_draft.json')
    def test_catalog_60_exact(self):self.assertEqual([r['id'] for r in catalog()['rules']],[f'FI-{i:02d}' for i in range(1,61)])
    def test_baseline_contract(self):self.assertEqual([],validate(self.base))
    def test_duplicate_scene_id_rejected(self):
        o=copy.deepcopy(self.base);o['scenes'].append(dict(o['scenes'][0],order=6));self.assertTrue(any('duplicate id' in e for e in validate(o)))
    def test_duplicate_order_rejected(self):
        o=copy.deepcopy(self.base);o['scenes'][1]['order']=1;self.assertTrue(any('order values must be unique' in e for e in validate(o)))
    def test_dangling_mystery_rejected(self):self.assertTrue(any('unknown scene' in e for e in validate(fixture('dangling_reference.json'))))
    def test_actor_reference_rejected(self):
        o=copy.deepcopy(self.base);o['relationships'][0]['actors']=['A','NOTREAL'];self.assertTrue(validate(o))
    def test_bad_assessment_rejected(self):
        o=copy.deepcopy(self.base);o['assessments']=[{'rule_id':'FI-99','verdict':'blessed','reviewer_type':'machine'}];self.assertTrue(validate(o))
    def test_scope_bound_waiver(self):
        o=copy.deepcopy(self.base);o['waivers']=[{'rule_id':'FI-05','scope':'other-book','actor':'author','rationale':'intentional','evidence_refs':['S1']}];self.assertTrue(any('scope' in e for e in validate(o)))
    def test_input_immutable(self):
        before=digest(self.base);audit(self.base);self.assertEqual(before,digest(self.base))
    def test_deterministic(self):
        a=audit(self.base);b=audit(copy.deepcopy(self.base));self.assertEqual(json.dumps(a,sort_keys=True),json.dumps(b,sort_keys=True))
    def test_unassessed_not_passed(self):self.assertEqual('UNASSESSED',audit(self.base)['results'][59]['status'])
    def test_nonfiction_is_not_relabelled(self):self.assertTrue(all(r['id'].startswith('FI-') for r in audit(self.base)['results']))


class Adversarial(unittest.TestCase):
    def test_forbidden_power_blocks(self):
        d=fixture('forbidden_power.json');report=audit(d);self.assertEqual('DEFECT',report['results'][35]['status']);self.assertEqual('BLOCK',release_gate(d,report,mode='draft')['verdict'])
    def test_unverified_retcon_string_cannot_override_canon(self):
        d=fixture('forbidden_power.json');d['scenes'][3]['power_uses'][0]['canon_exception']='because I say so'
        self.assertEqual('DEFECT',audit(d)['results'][35]['status'])
    def test_readerless_editorial_waiver_cannot_approve_release(self):
        d=fixture('valid_draft.json');d['waivers']=[{'rule_id':'FI-25','scope':'sample-novel','actor':'writer','rationale':'intentional','evidence_refs':['S4']}]
        self.assertEqual('HOLD',release_gate(d,audit(d),mode='editorial')['verdict'])
    def test_emotional_residue_signal(self):
        d=fixture('valid_draft.json');d['coverage']['emotional_events']=True
        d['emotional_events']=[{'id':'E1','scene_id':'S2','major':True,'residue_scene_ids':[]}]
        self.assertEqual('SIGNAL',audit(d)['results'][29]['status'])
    def test_act_transformation_signal(self):
        d=fixture('valid_draft.json');d['coverage']['act_states']=True
        d['act_states']=[{'act':i,'objective':'same','available_options':['x'],'known_facts':[],'stakes':'same','relationship_state':'same'} for i in range(1,4)]
        self.assertEqual('SIGNAL',audit(d)['results'][44]['status'])
    def test_stale_span_digest_invalid(self):
        d=fixture('valid_draft.json');d['scenes'][0]['anchor']={'start':0,'end':4,'source_digest':'sha256:'+'0'*64}
        self.assertTrue(any('stale' in e for e in audit(d,text='some text')['schema_errors']))
    def test_unknown_cost_stays_unassessed(self):
        d=fixture('valid_draft.json');d['interventions'][0].pop('cost_paid')
        self.assertEqual('DATA_GAP',audit(d)['results'][36]['status'])
        self.assertEqual('HOLD',release_gate(d,audit(d),mode='editorial')['verdict'])
    def test_unknown_power_operation_not_granted(self):
        d=fixture('valid_draft.json');d['scenes'][3]['power_uses']=[{'rule_id':'P1','action':'surprise_beam'}]
        self.assertEqual('DATA_GAP',audit(d)['results'][34]['status'])
    def test_unknown_emotional_residue_reference_fails_validation(self):
        d=fixture('valid_draft.json');d['emotional_events']=[{'id':'E1','scene_id':'S1','residue_scene_ids':['MISSING']}]
        self.assertTrue(any('residue' in x for x in validate(d)))
    def test_unpaid_cost_blocks(self):
        d=fixture('unpaid_cost.json');report=audit(d);self.assertEqual('DEFECT',report['results'][36]['status']);self.assertEqual('BLOCK',release_gate(d,report,mode='publication')['verdict'])
    def test_waiver_cannot_erase_canon_violation(self):
        d=fixture('forbidden_power.json');d['waivers']=[{'rule_id':'FI-36','scope':'sample-novel','actor':'author','rationale':'I like it','evidence_refs':['S4']}]
        self.assertEqual('DEFECT',audit(d)['results'][35]['status'])
    def test_flats_are_signals_not_certainty(self):
        r=audit(fixture('flat_tension.json'))
        self.assertIn('SIGNAL',[r['results'][13]['status'],r['results'][22]['status']]);self.assertNotEqual('DEFECT',r['results'][13]['status'])
    def test_rare_plain_prose_has_no_figuration_signal(self):
        passage='She put down the key. The door opened. Nobody spoke. '*100
        self.assertNotIn('FI-01',[s['rule_id'] for s in text_signals(passage)])
    def test_overused_figuration_signal(self):
        passage=('It was like a clock, like a bell, like a drum. ' * 70)
        self.assertIn('FI-01',[s['rule_id'] for s in text_signals(passage)])
    def test_raw_latex_signal(self):self.assertIn('FI-55',[s['rule_id'] for s in text_signals('the exported math showed \\alpha and \\frac{}{}')])
    def test_short_text_does_not_trigger_density(self):self.assertNotIn('FI-01',[s['rule_id'] for s in text_signals('Like a clock, she waited.')])
    def test_model_cannot_independently_pass(self):
        d=copy.deepcopy(fixture('valid_draft.json'));d['assessments'].append({'rule_id':'FI-25','verdict':'pass','reviewer_type':'model','reviewer':'llm','rationale':'I like it','evidence_refs':['S1']})
        self.assertEqual('UNASSESSED',audit(d)['results'][24]['status'])
    def test_human_can_review_art_but_not_prove_it(self):
        d=copy.deepcopy(fixture('valid_draft.json'));d['assessments'].append({'rule_id':'FI-25','verdict':'pass','reviewer_type':'human','reviewer':'Reader A','rationale':'two unforced choices','evidence_refs':['S1','S4']})
        self.assertEqual('REVIEWED_PASS',audit(d)['results'][24]['status'])
        self.assertEqual('HOLD',release_gate(d,audit(d),mode='editorial')['verdict'])
    def test_publication_cannot_pass_without_external_readers(self):
        d=fixture('valid_draft.json');d['publication'].update({'release_target':'ebook','title':'The Quiet Signal','edition':'First','publisher':'Example Press','copyright':'Copyright 2026'})
        self.assertEqual('HOLD',release_gate(d,audit(d),mode='publication')['verdict'])
    def test_mismatched_reader_study_stays_hold(self):
        d=fixture('valid_draft.json');d['publication']['release_target']='ebook'
        study={'schema':'wi.fiction.reader-study/v1','work_id':'sample-novel','manuscript_digest':'sha256:BAD','independent_readers':4,'consent_confirmed':True,'methodology':'blind','findings':[1],'reconciliation':'done'}
        res=release_gate(d,audit(d),study,mode='publication');self.assertTrue(any('version' in x['reason'] for x in res['issues']))
    def test_no_silent_zero(self):
        d=fixture('valid_draft.json');d.pop('coverage');r=audit(d);self.assertEqual('UNASSESSED',r['results'][18]['status'])
    def test_falsepositive_intentional_motif_not_defect(self):
        d=fixture('valid_draft.json');d['motifs']=[{'id':'clock','uses':[{'meaning':'waiting','scene_id':x,'intentional':True} for x in ('S1','S2','S4')]}]
        self.assertNotEqual('DEFECT',audit(d)['results'][3]['status'])
    def test_review_cannot_override_contradiction(self):
        d=fixture('forbidden_power.json');d['assessments']=[{'rule_id':'FI-36','verdict':'pass','reviewer_type':'human','reviewer':'editor','rationale':'dramatic','evidence_refs':['S4']}]
        self.assertEqual('DEFECT',audit(d)['results'][35]['status'])


class CLI(unittest.TestCase):
    def run_cli(self,*args):
        return subprocess.run([sys.executable,str(ROOT/'scripts'/'wi-fiction.py'),*args],capture_output=True,text=True)
    def test_cli_validate(self):self.assertEqual(0,self.run_cli('validate','--input',str(ROOT/'tests/v8/fixtures/valid_draft.json')).returncode)
    def test_cli_validation_exit_two(self):self.assertEqual(2,self.run_cli('validate','--input',str(ROOT/'tests/v8/fixtures/dangling_reference.json')).returncode)
    def test_cli_gate_block_exit_two(self):self.assertEqual(2,self.run_cli('gate','--input',str(ROOT/'tests/v8/fixtures/forbidden_power.json')).returncode)
    def test_cli_publication_hold_exit_three(self):self.assertEqual(3,self.run_cli('gate','--input',str(ROOT/'tests/v8/fixtures/valid_draft.json'),'--mode','publication').returncode)
    def test_cli_audit_60(self):
        res=self.run_cli('audit','--input',str(ROOT/'tests/v8/fixtures/valid_draft.json'))
        self.assertEqual(0,res.returncode);self.assertEqual(60,len(json.loads(res.stdout)['results']))
    def test_cli_unsupported_rule_fails(self):self.assertNotEqual(0,self.run_cli('explain-rule','FI-61').returncode)


if __name__=='__main__':unittest.main(verbosity=2)
