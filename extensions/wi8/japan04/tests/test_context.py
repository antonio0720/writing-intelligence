import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from japan_story_os.context import *
from japan_story_os.contracts import ContractError

class ContextTest(unittest.TestCase):
    def test_reiwa_first(self):self.assertEqual(era_from_gregorian(2019,5,1)['year_of_era'],1)
    def test_last_heisei(self):self.assertEqual(era_from_gregorian(2019,4,30)['era'],'Heisei')
    def test_showa_before_heisei(self):self.assertEqual(era_from_gregorian(1989,1,7)['era'],'Shōwa')
    def test_japan_era_refuses_edo_approximation(self):self.assertRaises(ContractError,era_from_gregorian,1850,2,1)
    def test_invalid_date_refuses(self):self.assertRaises(ValueError,era_from_gregorian,2025,2,30)
    def test_kyoto_rule_not_okinawa(self):
        result=cultural_applicability({'region':'Kyoto'},{'region':'Okinawa'})
        self.assertEqual(result['status'],'mismatch')
    def test_kyoto_rule_at_kyoto_scope_only(self):
        result=cultural_applicability({'region':'Kyoto'},{'region':'Kyoto'})
        self.assertFalse(result['source_verified'])
    def test_unavailable_region_unknown(self):self.assertEqual(cultural_applicability({'region':'Kyoto'},{})['status'],'unknown')
    def test_different_custodian_unknown(self):self.assertEqual(cultural_applicability({'site_id':'s1'},{'region':'Kyoto'})['status'],'unknown')
    def test_shrine_not_temple_universal_rule(self):self.assertEqual(tradition_hint('buddhist_temple','torii_required')['status'],'REVIEW')
    def test_shrine_custodian_still_needed(self):self.assertEqual(tradition_hint('shinto_shrine','torii_required')['status'],'CONTEXT_REQUIRED')
    def test_nonreligious_site_without_guess(self):self.assertEqual(tradition_hint('unknown','torii_required')['status'],'CONTEXT_REQUIRED')
    def test_honorific_sarcasm_can_be_intentional(self):self.assertFalse(honorific_transition('-san','bare surname','sarcasm')['forbidden'])
    def test_honorific_change_not_proven_authentic(self):self.assertFalse(honorific_transition('-san','bare surname','sarcasm')['authenticity_proven'])
    def test_honorific_no_change_allowed(self):self.assertFalse(honorific_transition('family','family')['changed'])
    def test_school_not_always_april(self):self.assertEqual(grade_transition(9,17)['start_month'],9)
    def test_school_age_83_permitted(self):self.assertEqual(grade_transition(4,83)['age'],83)
    def test_age_negative_rejected(self):self.assertRaises(ContractError,grade_transition,4,-1)
    def test_declared_same_place(self):self.assertEqual(scene_travel('a','a',{})['plausible'],'same_place')
    def test_route_not_invented(self):self.assertEqual(scene_travel('Tokyo','Osaka',{})['plausible'],'needs_route_evidence')
    def test_adjacent_declared_no_minutes(self):
        r=scene_travel('a','b',{'a':['b']});self.assertEqual(r['plausible'],'declared_adjacent');self.assertIsNone(r['estimated_minutes'])
    def test_magic_route_author_declared(self):self.assertEqual(scene_travel('a','b',{},exception='author-branch')['plausible'],'author_declared_magic')
    def test_nonmagic_no_magic_quota(self):self.assertEqual(simulate_power_ledger([],{})['status'],'CONSISTENT_WITH_DECLARED_RESOURCES')
    def test_power_overspend(self):self.assertEqual(simulate_power_ledger([{'id':'a','resource':'stamina','delta':-11}],{'stamina':10})['status'],'BLOCK_OVERSPENT')
    def test_power_replenish(self):
        r=simulate_power_ledger([{'id':'a','resource':'stamina','delta':-10},{'id':'b','resource':'stamina','delta':5}],{'stamina':10})
        self.assertEqual(r['ending_resources']['stamina'],5)
    def test_power_negative_initial(self):self.assertRaises(ContractError,simulate_power_ledger,[],{'stamina':-1})
    def test_power_cannot_create_new_pool(self):self.assertRaises(ContractError,simulate_power_ledger,[{'resource':'mana','delta':1}],{})

if __name__=='__main__':unittest.main()
