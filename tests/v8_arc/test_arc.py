import copy
import json
import pathlib
import subprocess
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[2]
FIX=pathlib.Path(__file__).resolve().parent/'fixtures'
sys.path.insert(0,str(ROOT/'scripts'))
from arc_v8.engine import validate, classify, evaluate, as_of, impact, gate, digest, state_diff

def load(name):return json.loads((FIX/name).read_text())

class ClassifierTests(unittest.TestCase):
    def test_all_quadrants(self):
        choices={('attained','fulfilled'):'sweet',('sacrificed','fulfilled'):'semi_sweet',
                 ('attained','unfulfilled'):'bittersweet',('thwarted','rejected'):'bitter'}
        for (want,need),expected in choices.items():
            with self.subTest(want=want,need=need):
                self.assertEqual(classify({'want_outcome':want,'need_outcome':need,'closure':'closed'})['quadrant'],expected)
    def test_nonbinary_not_invented(self):
        for want in ('partial','unresolved','disputed','n_a'):
            with self.subTest(want=want):
                self.assertEqual(classify({'want_outcome':want,'need_outcome':'fulfilled','closure':'closed'})['quadrant'],'not_classifiable')
    def test_need_nonbinary_not_invented(self):
        for need in ('partial','unresolved','disputed','n_a'):
            with self.subTest(need=need):
                self.assertEqual(classify({'want_outcome':'attained','need_outcome':need,'closure':'closed'})['quadrant'],'not_classifiable')
    def test_intentional_ambiguity_no_quadrant(self):
        self.assertEqual(classify({'want_outcome':'attained','need_outcome':'fulfilled','closure':'deliberately_ambiguous'})['quadrant'],'not_classifiable')
    def test_open_arc_no_forced_classification(self):
        self.assertEqual(classify({'want_outcome':'attained','need_outcome':'fulfilled','closure':'open'})['quadrant'],'not_classifiable')
    def test_reviewer_inference_not_canon(self):
        self.assertEqual(classify({'want_outcome':'attained','need_outcome':'fulfilled','closure':'closed'},'reviewer_inferred')['quadrant'],'not_classifiable')
    def test_reader_inference_not_canon(self):
        self.assertEqual(classify({'want_outcome':'attained','need_outcome':'fulfilled','closure':'closed'},'author_asserted','reader_reported')['quadrant'],'not_classifiable')

class StructuralTests(unittest.TestCase):
    def test_main_valid(self):self.assertEqual(validate(load('four_quadrants.json')),[])
    def test_allow_working_draft_without_ending(self):self.assertEqual(validate(load('working_draft.json')),[])
    def test_duplicate_state_revision_refused(self):
        d=load('four_quadrants.json')
        d['assertions'][1]['logical_id']='want-ada-v2'
        d['assertions'][1]['revision']=1
        d['assertions'][1].pop('supersedes')
        d['assertions'][0]['logical_id']='want-ada-v2'
        self.assertIn('ARC_DUPLICATE_REVISION',{f['code'] for f in validate(d)})
    def test_foreign_repo_refused(self):
        d=load('four_quadrants.json');d['source']['repo']='unknown/example'
        self.assertIn('ARC_SOURCE_REPO',{f['code'] for f in validate(d)})
    def test_fake_canonical_export_has_no_readback(self):
        d=load('four_quadrants.json');d['source']['origin']='canonical_export'
        self.assertIn('ARC_READBACK_MISSING',{f['code'] for f in validate(d)})
    def test_unexpected_payload_type_does_not_crash(self):
        d=load('four_quadrants.json');d['assertions'][0]['payload']=['malformed']
        self.assertIn('ARC_PAYLOAD',{f['code'] for f in validate(d)})
    def test_invalid_fixtures(self):
        for name,code in [('dangling.json','ARC_REF_DANGLING'),('unowned_focus.json','ARC_FOCUS_WRONG_OWNER'),
                          ('invalid_interval.json','ARC_TIME_INTERVAL'),('wrong_revision.json','ARC_REVISION_GAP'),
                          ('cycle.json','ARC_CAUSAL_CYCLE')]:
            with self.subTest(fixture=name):
                found={x['code'] for x in validate(load(name))};self.assertIn(code,found)
    def test_global_duplicate_ids(self):
        d=load('four_quadrants.json');d['events'][0]['id']=d['characters'][0]['id']
        self.assertIn('ARC_DUPLICATE_ID',{x['code'] for x in validate(d)})
    def test_must_declare_source(self):
        d=load('four_quadrants.json');d.pop('source')
        self.assertIn('ARC_SOURCE_MISSING',{x['code'] for x in validate(d)})
    def test_invalid_known_at(self):
        d=load('four_quadrants.json');d['assertions'][0]['known_at']='2026-10-24'
        self.assertIn('ARC_KNOWLEDGE_TIME',{x['code'] for x in validate(d)})
    def test_invalid_ending_status(self):
        d=load('four_quadrants.json');d['assertions'][4]['payload']['want_outcome']='success'
        self.assertIn('ARC_WANT_OUTCOME',{x['code'] for x in validate(d)})
    def test_invalid_realm_semantics_flag(self):
        d=load('four_quadrants.json');d['assertions'][0]['provenance']['basis']='external_scientific_fact'
        self.assertIn('ARC_PROVENANCE',{x['code'] for x in validate(d)})

class EvaluationTests(unittest.TestCase):
    def test_four_separate_endings(self):
        r=evaluate(load('four_quadrants.json'))
        self.assertEqual([x['endings'][0]['projection']['quadrant'] for x in r['characters']], ['sweet','semi_sweet','bittersweet','bitter'])
    def test_flat_arc_stays_flat_even_sweet(self):
        r=evaluate(load('flat_arc.json'))
        self.assertEqual(r['characters'][0]['arc_family'],'flat')
        self.assertEqual(r['characters'][0]['endings'][0]['projection']['quadrant'],'sweet')
    def test_open_family_not_inferred_from_bitter(self):
        r=evaluate(load('four_quadrants.json'))
        self.assertEqual(r['characters'][3]['arc_family'],'open')
        self.assertEqual(r['characters'][3]['endings'][0]['projection']['quadrant'],'bitter')
    def test_ambiguous_fixture_not_classifiable(self):
        r=evaluate(load('ambiguous.json'))
        self.assertEqual(r['characters'][0]['endings'][0]['projection']['quadrant'],'not_classifiable')
    def test_no_false_reader_observation(self):
        r=evaluate(load('false_reader_claim.json'))
        self.assertIn('ARC_READER_VALENCE_ASSERTED',{x['code'] for x in r['findings']})
    def test_missing_choice_needs_review(self):
        r=evaluate(load('missing_choice.json'))
        self.assertIn('ARC_CLAIMED_CHANGE_NO_CHOICE',{x['code'] for x in r['findings']})
    def test_closed_ending_without_witness_requires_review(self):
        r=evaluate(load('lost_witness.json'))
        self.assertIn('ARC_ENDING_UNWITNESSED',{x['code'] for x in r['findings']})
    def test_unverified_need_needs_review(self):
        r=evaluate(load('no_need_assertion.json'))
        self.assertIn('ARC_NEED_UNVERIFIED',{x['code'] for x in r['findings']})
    def test_negative_invalid_cannot_be_evaluated(self):
        r=evaluate(load('dangling.json'))
        self.assertEqual(r['status'],'invalid')
    def test_digest_stable_cross_calls(self):
        d=load('four_quadrants.json');self.assertEqual(digest(d),digest(copy.deepcopy(d)))
    def test_digest_changes_on_edit(self):
        d=load('four_quadrants.json');old=digest(d);d['assertions'][0]['payload']['proposition']='different'
        self.assertNotEqual(old,digest(d))

class TemporalTests(unittest.TestCase):
    def test_first_want_stays_in_past(self):
        d=load('four_quadrants.json');r=as_of(d,'ev-0','2026-10-24T13:00:00-05:00')
        self.assertEqual(r['states']['want-ada-v1']['state_id'],'want-ada-v1')
    def test_revised_want_at_new_event(self):
        d=load('four_quadrants.json');r=as_of(d,'ev-2','2026-10-24T13:00:00-05:00')
        self.assertEqual(r['states']['want-ada-v1']['state_id'],'want-ada-v2')
    def test_later_known_want_not_visible_early(self):
        d=load('four_quadrants.json');r=as_of(d,'ev-2','2026-10-24T11:00:00-05:00')
        self.assertNotIn('want-ada-v1',r['states'])
    def test_historical_state_kept_even_after_future_known(self):
        d=load('four_quadrants.json');r=as_of(d,'ev-0','2026-10-24T13:00:00-05:00')
        self.assertEqual(r['states']['want-ada-v1']['payload']['proposition'],'Win the city medal')
    def test_missing_event_refused(self):
        self.assertEqual(as_of(load('four_quadrants.json'),'fake','2026-10-24T13:00:00Z')['status'],'invalid')
    def test_invalid_time_refused(self):
        self.assertEqual(as_of(load('four_quadrants.json'),'ev-0','yesterday')['status'],'invalid')

class ImpactTests(unittest.TestCase):
    def test_revised_want_impacts_ending(self):
        r=impact(load('four_quadrants.json'),['want-ada-v2'])
        self.assertIn('ending-ada',r['downstream_may_be_stale'])
    def test_event_changes_propagate(self):
        r=impact(load('four_quadrants.json'),['ev-0'])
        self.assertIn('ev-4',r['downstream_may_be_stale'])
    def test_unrelated_character_not_impacted_by_want(self):
        r=impact(load('four_quadrants.json'),['want-ada-v2'])
        self.assertNotIn('ending-beck',r['downstream_may_be_stale'])
    def test_unknown_impact_ref_refused(self):
        self.assertEqual(impact(load('four_quadrants.json'),['fake'])['status'],'invalid')

class GateTests(unittest.TestCase):
    def test_valid_mechanics_is_not_publication(self):
        self.assertEqual(gate(load('four_quadrants.json'),stage='mechanical')['verdict'],'PASS_MECHANICAL_ONLY')
    def test_invalid_blocks(self):
        self.assertEqual(gate(load('dangling.json'),stage='mechanical')['verdict'],'BLOCK')
    def test_editorial_requires_people(self):
        self.assertEqual(gate(load('four_quadrants.json'),stage='editorial')['verdict'],'HOLD')
    def test_publication_without_readers_holds(self):
        self.assertEqual(gate(load('four_quadrants.json'),stage='publication')['verdict'],'HOLD')
    def test_fabricated_matching_reader_study_still_not_certified(self):
        d=load('four_quadrants.json');review=load('stale_reader_reviews.json');review['source_digest']=digest(d)
        self.assertEqual(gate(d,reader_reviews=review,stage='publication')['verdict'],'HOLD')
    def test_stale_reader_study_rejected(self):
        self.assertIn('digest',gate(load('four_quadrants.json'),reader_reviews=load('stale_reader_reviews.json'),stage='publication')['reason'])

class DiffTests(unittest.TestCase):
    def test_start_and_final_want_change(self):
        r=state_diff(load('four_quadrants.json'),'ev-0','ev-4','2026-10-24T13:00:00-05:00','ch-ada')
        self.assertEqual(r['status'],'projection_only')
        self.assertIn('want-ada-v1', {c['logical_id'] for c in r['changes']})
        item=next(c for c in r['changes'] if c['logical_id']=='want-ada-v1')
        self.assertEqual(item['before']['state_id'],'want-ada-v1')
        self.assertEqual(item['after']['state_id'],'want-ada-v2')
    def test_no_other_character_in_diff(self):
        r=state_diff(load('four_quadrants.json'),'ev-0','ev-4','2026-10-24T13:00:00-05:00','ch-ada')
        self.assertTrue(all((x.get('before') or x.get('after'))['character_ref']=='ch-ada' for x in r['changes']))
    def test_unknown_character_refused(self):
        r=state_diff(load('four_quadrants.json'),'ev-0','ev-4','2026-10-24T13:00:00-05:00','ch-fake')
        self.assertEqual(r['status'],'invalid')

class CommandTests(unittest.TestCase):
    def run_cli(self,*args):
        p=subprocess.run([sys.executable,str(ROOT/'scripts'/'wi-arc.py'),*args],capture_output=True,text=True)
        return p, json.loads(p.stdout) if p.stdout.strip() else None
    def test_cli_validate(self):
        p,o=self.run_cli('validate','--input',str(FIX/'four_quadrants.json'))
        self.assertEqual(p.returncode,0);self.assertTrue(o['valid'])
    def test_cli_invalid_exit(self):
        p,o=self.run_cli('validate','--input',str(FIX/'dangling.json'))
        self.assertEqual(p.returncode,2);self.assertFalse(o['valid'])
    def test_cli_mechanical_only(self):
        p,o=self.run_cli('gate','--input',str(FIX/'four_quadrants.json'))
        self.assertEqual(p.returncode,0);self.assertEqual(o['verdict'],'PASS_MECHANICAL_ONLY')
    def test_cli_publication_hold(self):
        p,o=self.run_cli('gate','--input',str(FIX/'four_quadrants.json'),'--stage','publication')
        self.assertEqual(p.returncode,3);self.assertEqual(o['verdict'],'HOLD')
    def test_cli_asof(self):
        p,o=self.run_cli('as-of','--input',str(FIX/'four_quadrants.json'),'--event','ev-2','--known-at','2026-10-24T13:00:00-05:00')
        self.assertEqual(p.returncode,0);self.assertEqual(o['states']['want-ada-v1']['state_id'],'want-ada-v2')
    def test_cli_diff(self):
        p,o=self.run_cli('diff','--input',str(FIX/'four_quadrants.json'),'--start','ev-0','--end','ev-4','--known-at','2026-10-24T13:00:00-05:00','--character','ch-ada')
        self.assertEqual(p.returncode,0);self.assertEqual(o['status'],'projection_only')
    def test_cli_rule_list(self):
        p,o=self.run_cli('rules','--id','N064')
        self.assertEqual(p.returncode,0);self.assertIn('Outcome Quadrant',o['title'])
    def test_cli_carried_forward_rule(self):
        p,o=self.run_cli('rules','--id','B001')
        self.assertEqual(p.returncode,0);self.assertEqual(o['implementation'],'existing_separate_zip_not_imported')
    def test_cli_complete_register(self):
        p,o=self.run_cli('rules')
        self.assertEqual(p.returncode,0);self.assertEqual(len(o['requirements']),120)

if __name__=='__main__': unittest.main(verbosity=2)
