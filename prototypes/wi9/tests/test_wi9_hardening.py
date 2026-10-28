"""Untrusted nested input cannot bypass checks or crash core analyzers."""
import unittest, tempfile, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from wi9_core import preflight, evaluate_benchmark, voice_baseline
from wi9_composition import inspect_candidate, prepare_request

class Hardening(unittest.TestCase):
    def test_unhashable_claim_id_stays_structured(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d,'doc').write_text('test')
            data={'schema':'wi9.preflight/1','document':{'path':'doc','origin':'human_authored','intended_use':'internal_review','arena':'essay'},'venue':{'policy':'ai_permitted','policy_source':'test'},'evidence':[],'contributions':[], 'claim_links':[{'evidence_id':['bad'],'exact_passage':'test'}]}
            r=preflight(data,d)
            self.assertEqual('HOLD',r['status'])
            self.assertIn('CLAIM_EVIDENCE_UNRESOLVED',{x['code'] for x in r['issues']})

    def test_unhashable_benchmark_key_stays_structured(self):
        r=evaluate_benchmark({'ratings':[{'case_id':[],'reviewer_id':'person','arm':'v9','scores':{},'critical_violations':0}]})
        self.assertEqual('HOLD',r['status'])
        self.assertTrue(r['errors'])

    def test_invalid_quote_collection_holds(self):
        d={'document':{'intended_use':'internal_review','arena':'essay','mission':'test'},'venue':{'policy':'ai_permitted'},'evidence':[{'id':'e1','claim':'x','kind':'external','exact_excerpt':'x','consent':True,'origin':'human_authored'}]}
        q=prepare_request(d)
        c={'schema':'wi9.candidate/1','paragraphs':[{'text':'x','evidence_ids':['e1'],'author_review_required':True,'direct_quotes': {'bad':True}}]}
        r=inspect_candidate(c,q)
        self.assertEqual('HOLD',r['status'])
        self.assertIn('QUOTE_LIST_INVALID:0',r['errors'])

if __name__=='__main__':unittest.main()
