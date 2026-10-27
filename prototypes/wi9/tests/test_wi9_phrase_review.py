import hashlib
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from wi9_hotphrases import scan_text
from wi9_phrase_review import audit_decisions

class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.text='That matters because the payment was 32 days late.'
        self.report=scan_text(self.text)
        f=self.report['findings'][0]
        self.decisions={'schema':'wi9.editorial.review/1','document_sha256':self.report['document_sha256'],
                        'rules_sha256':self.report['rules_sha256'],
                        'decisions':[{'rule_id':f['id'],'start':f['start'],'end':f['end'],'excerpt':f['excerpt'],
                                      'status':'retain_as_written','rationale':'The specificity is in the same sentence.',
                                      'reviewer':'Antonio T. Smith Jr.','reviewed_at':'2026-10-27T12:00:00-05:00'}]}
    def test_valid_edit_review_is_not_release(self):
        out=audit_decisions(self.text,self.report,self.decisions)
        self.assertEqual('REVIEW',out['status'])
        self.assertFalse(out['release_authorized'])
    def test_changed_text_invalidates_report(self):
        out=audit_decisions(self.text+' Plus',self.report,self.decisions)
        self.assertEqual('HOLD',out['status'])
        self.assertIn('DOCUMENT_STALE',out['issues'])
    def test_rules_digest_change_invalidates_decision(self):
        self.decisions['rules_sha256']='0'*64
        out=audit_decisions(self.text,self.report,self.decisions)
        self.assertIn('REVIEW_RULESET_STALE',out['issues'])
    def test_missing_rationale_holds(self):
        self.decisions['decisions'][0]['rationale']='ok'
        self.assertIn('RATIONALE_MISSING:0',audit_decisions(self.text,self.report,self.decisions)['issues'])
    def test_unfound_hit_holds(self):
        self.decisions['decisions'][0]['start']=800
        self.assertIn('DECISION_TARGET_UNKNOWN:0',audit_decisions(self.text,self.report,self.decisions)['issues'])
    def test_duplicate_review_holds(self):
        self.decisions['decisions'].append(dict(self.decisions['decisions'][0]))
        self.assertIn('DECISION_DUPLICATE:1',audit_decisions(self.text,self.report,self.decisions)['issues'])
    def test_no_review_leaves_zero_coverage(self):
        self.decisions['decisions']=[]
        out=audit_decisions(self.text,self.report,self.decisions)
        self.assertEqual(0,out['review_coverage'])
        self.assertFalse(out['release_authorized'])
    def test_unsupported_root_is_hold(self):
        self.assertEqual('HOLD',audit_decisions(self.text,[],self.decisions)['status'])

    def test_naive_review_time_holds(self):
        self.decisions['decisions'][0]['reviewed_at']='2026-10-27T21:00:00'
        self.assertIn('REVIEW_DATE_INVALID:0',audit_decisions(self.text,self.report,self.decisions)['issues'])
    def test_unparseable_review_time_holds(self):
        self.decisions['decisions'][0]['reviewed_at']='last Tuesday'
        self.assertIn('REVIEW_DATE_INVALID:0',audit_decisions(self.text,self.report,self.decisions)['issues'])
    def test_future_review_time_holds(self):
        self.decisions['decisions'][0]['reviewed_at']='2999-01-01T00:00:00+00:00'
        self.assertIn('REVIEW_DATE_INVALID:0',audit_decisions(self.text,self.report,self.decisions)['issues'])
