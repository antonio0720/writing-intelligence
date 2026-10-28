"""Composition contract negative controls: synthetic fixtures only."""
import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wi9_composition import prepare_request, inspect_candidate, render_research_only

class ComposeTests(unittest.TestCase):
    def setUp(self):
        self.data={
          'document': {'arena':'essay','intended_use':'internal_review','mission':'Explain a design choice'},
          'venue': {'policy':'ai_permitted'},
          'author_thesis':'Model constraints affect real design decisions',
          'evidence': [{'id':'e1','claim':'A model was made','kind':'firsthand','exact_excerpt':'I built a model.','consent':True,'origin':'human_authored'}]
        }
        self.candidate={'schema':'wi9.candidate/1','paragraphs':[{
          'text':'I built a model.','evidence_ids':['e1'],'author_review_required':True,
          'asserts_firsthand':True,'direct_quotes':[{'source_id':'e1','exact_text':'I built a model.'}]}]}

    def test_valid_eligible_request_is_not_release(self):
        q=prepare_request(self.data)
        self.assertEqual('REQUEST_READY',q['status'])
        self.assertFalse(q['release_authorized'])

    def test_human_only_blocks_request_even_internal_review(self):
        self.data['venue']['policy']='human_only'
        q=prepare_request(self.data)
        self.assertEqual('HOLD',q['status'])
        self.assertEqual('HUMAN_ONLY_NO_GENERATED_PROSE',q['reason'])

    def test_human_only_outputs_questions_not_submittable_prose(self):
        self.data['venue']['policy']='human_only'
        r=render_research_only(self.data)
        self.assertIsNone(r['submission_text'])
        self.assertTrue(r['source_questions'])

    def test_unknown_venue_blocks(self):
        self.data['venue']['policy']='unknown'
        self.assertEqual('VENUE_POLICY_UNKNOWN',prepare_request(self.data)['reason'])

    def test_disclosure_plan_required(self):
        self.data['venue']['policy']='disclosure_required'
        self.assertEqual('DISCLOSURE_PLAN_REQUIRED',prepare_request(self.data)['reason'])

    def test_duplicate_evidence_id_blocks(self):
        self.data['evidence'].append(dict(self.data['evidence'][0]))
        self.assertEqual('DUPLICATE_EVIDENCE_ID',prepare_request(self.data)['reason'])

    def test_candidate_passes_only_as_review_required(self):
        q=prepare_request(self.data)
        r=inspect_candidate(self.candidate,q)
        self.assertEqual('DRAFT_REVIEW_REQUIRED',r['status'])
        self.assertFalse(r['release_authorized'])

    def test_human_memory_cannot_be_inferred_from_external_note(self):
        self.data['evidence'][0]['kind']='external'
        q=prepare_request(self.data)
        self.assertIn('UNANCHORED_FIRSTHAND:0',inspect_candidate(self.candidate,q)['errors'])

    def test_fabricated_quote_blocked(self):
        self.candidate['paragraphs'][0]['direct_quotes'][0]['exact_text']='I invented a different quote.'
        q=prepare_request(self.data)
        self.assertIn('QUOTATION_UNVERIFIED:0',inspect_candidate(self.candidate,q)['errors'])

    def test_nonexistent_source_blocked(self):
        self.candidate['paragraphs'][0]['evidence_ids']=['does-not-exist']
        q=prepare_request(self.data)
        self.assertIn('EVIDENCE_UNRESOLVED:0',inspect_candidate(self.candidate,q)['errors'])

    def test_review_flag_mandatory(self):
        self.candidate['paragraphs'][0]['author_review_required']=False
        q=prepare_request(self.data)
        self.assertIn('REVIEW_FLAG_ABSENT:0',inspect_candidate(self.candidate,q)['errors'])

if __name__ == '__main__': unittest.main()
