"""Synthetic, deterministic negative controls for WI9 reference specimen."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wi9_core import bounded_read, preflight, profile_text, editorial_diagnostics, voice_baseline, editorial_plan, evaluate_benchmark, METRICS, sha256


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.doc = 'draft.txt'
        self.src = 'note.txt'
        (self.root / self.doc).write_text('I designed a small model.', encoding='utf-8')
        (self.root / self.src).write_text('I designed a small model.', encoding='utf-8')
        self.data = {
            'schema': 'wi9.preflight/1',
            'document': {'path': self.doc, 'arena': 'journalism', 'origin': 'ai_generated',
                         'intended_use': 'research', 'mission': 'Explain the purpose',
                         'expected_sha256': sha256((self.root/self.doc).read_bytes())},
            'venue': {'policy': 'human_only', 'policy_source': 'reporter supplied'},
            'contributions': [{'kind': 'ai_research'}],
            'evidence': [{'id': 's1', 'kind': 'firsthand', 'origin': 'human_authored',
                          'path': self.src, 'claim': 'A small model was designed',
                          'exact_excerpt': 'I designed a small model.', 'consent': True}],
            'claim_links': [{'evidence_id': 's1', 'exact_passage': 'I designed a small model.'}],
            'full_claim_review': False
        }

    def codes(self, data=None):
        return {x['code'] for x in preflight(data if data is not None else self.data, self.root)['issues']}

    def test_experiment_research_not_release(self):
        x = preflight(self.data, self.root)
        self.assertEqual('REVIEW', x['status'])
        self.assertFalse(x['release_authorized'])

    def test_human_only_generated_submission_holds(self):
        self.data['document']['intended_use']='submission'
        self.assertIn('HUMAN_ONLY_ORIGIN', self.codes())

    def test_human_only_substantive_ai_holds_even_with_human_label(self):
        self.data['document'].update(origin='human_authored', intended_use='submission')
        self.data['contributions'] = [{'kind': 'human_original'}, {'kind': 'ai_substantive_rewrite'}]
        self.assertIn('HUMAN_ONLY_AI_PROSE', self.codes())

    def test_unknown_venue_holds(self):
        self.data['document']['intended_use']='submission'
        self.data['venue']['policy']='unknown'
        self.assertIn('POLICY_UNKNOWN', self.codes())

    def test_missing_contributions_holds(self):
        self.data['document']['intended_use']='submission'
        del self.data['contributions']
        self.assertIn('CONTRIBUTIONS_EMPTY', self.codes())

    def test_disclosure_requirement_holds(self):
        self.data['document']['intended_use']='submission'
        self.data['venue']['policy']='disclosure_required'
        self.assertIn('DISCLOSURE_ABSENT', self.codes())

    def test_strict_claim_review_holds(self):
        self.data['document']['intended_use']='submission'
        self.data['document']['origin']='human_authored'
        self.data['contributions']=[{'kind':'human_original'}]
        self.assertIn('FULL_CLAIM_REVIEW_ABSENT', self.codes())

    def test_digest_mutation_holds(self):
        (self.root/self.doc).write_text('Now changed.', encoding='utf-8')
        self.assertIn('DOCUMENT_DIGEST_MISMATCH', self.codes())

    def test_duplicate_evidence_ids_hold(self):
        self.data['evidence'].append(dict(self.data['evidence'][0]))
        self.assertIn('DUPLICATE_ID', self.codes())

    def test_wrong_claim_link_holds(self):
        self.data['claim_links'][0]['evidence_id']='missing'
        self.assertIn('CLAIM_EVIDENCE_UNRESOLVED', self.codes())

    def test_missing_source_excerpt_holds(self):
        self.data['evidence'][0]['exact_excerpt']='A sentence not present'
        self.assertIn('SOURCE_ANCHOR_MISSING', self.codes())

    def test_firsthand_ai_origin_holds(self):
        self.data['evidence'][0]['origin']='ai_generated'
        self.assertIn('FIRSTHAND_NOT_AUTHORED', self.codes())

    def test_consent_missing_holds(self):
        self.data['evidence'][0]['consent']=False
        self.assertIn('SOURCE_CONSENT_ABSENT', self.codes())

    def test_wrong_root_type_holds(self):
        self.assertIn('INVALID_ROOT', self.codes([]))

    def test_invalid_doc_type_holds(self):
        self.data['document']=None
        self.assertIn('DOCUMENT_MISSING', self.codes())

    def test_traversal_rejected(self):
        with self.assertRaises(ValueError):
            bounded_read(self.root, '../outside.txt')

    def test_absolute_path_rejected(self):
        with self.assertRaises(ValueError):
            bounded_read(self.root, '/etc/passwd')

    @unittest.skipUnless(hasattr(os, 'symlink'), 'symlink unsupported')
    def test_symlink_rejected(self):
        (self.root/'link.txt').symlink_to(self.src)
        with self.assertRaises(OSError):
            bounded_read(self.root, 'link.txt')

    def test_directory_rejected(self):
        (self.root/'folder').mkdir()
        with self.assertRaises(ValueError):
            bounded_read(self.root, 'folder')

    def test_large_file_rejected(self):
        (self.root/'large').write_bytes(b'a'*102)
        with self.assertRaises(ValueError):
            bounded_read(self.root, 'large', limit=100)

    def test_profile_measures_not_authorship(self):
        x=profile_text('One sentence. Another, longer sentence here!')
        self.assertEqual(2,x['sentence_count'])
        self.assertNotIn('authorship_probability',x)

    def test_diagnostics_flag_vague_authority(self):
        x=editorial_diagnostics('Studies show that magic works. Many experts agree.')
        self.assertIn('VAGUE_ORIGIN',{y['code'] for y in x['findings']})

    def test_plan_is_questions_not_submission(self):
        x=editorial_plan(self.data)
        self.assertTrue(x['questions'])
        self.assertNotIn('pitch', x.keys())

    def test_voice_three_samples_required(self):
        self.assertIn('VOICE_SAMPLE_COUNT',{x['code'] for x in voice_baseline([],self.root)['issues']})

    def test_voice_wrong_origin_holds(self):
        x=voice_baseline([{'origin':'ai_generated','consent':True,'path':self.src}],self.root)
        self.assertIn('VOICE_SOURCE_INELIGIBLE',{y['code'] for y in x['issues']})

    def test_voice_duplicate_holds(self):
        source=' '.join(['This is an author-supplied sample sentence.']*115)
        (self.root/'voice.txt').write_text(source)
        sample={'id':'v1','path':'voice.txt','consent':True,'origin':'human_authored',
                'sha256':sha256((self.root/'voice.txt').read_bytes()),'genre':'essay'}
        r=voice_baseline([sample,sample,sample],self.root)
        self.assertIn('VOICE_DUPLICATED_SAMPLE',{x['code'] for x in r['issues']})

    def test_benchmark_missing_data_holds(self):
        self.assertEqual('HOLD',evaluate_benchmark({'ratings':[]})['status'])

    def test_benchmark_tiny_paired_set_does_not_claim_success(self):
        ratings=[]
        for arm,n in [('v8',2),('v9',4)]:
            ratings.append({'case_id':'c1','reviewer_id':'rev1','arm':arm,
                            'scores':{m:n for m in METRICS},'critical_violations':0})
        result=evaluate_benchmark({'ratings':ratings})
        self.assertEqual('HOLD',result['status'])
        self.assertEqual(2,result['deltas']['original_thought']['median_v9_minus_v8'])

    def test_benchmark_violations_always_hold(self):
        ratings=[]
        for case in range(2):
            for arm in ('v8','v9'):
                ratings.append({'case_id':str(case),'reviewer_id':'reviewer','arm':arm,
                                'scores':{m:4 for m in METRICS},'critical_violations':1 if case==1 and arm=='v9' else 0})
        self.assertEqual('HOLD',evaluate_benchmark({'ratings':ratings},minimum_pairs=2)['status'])

    def test_benchmark_sufficient_clean_pairs_review_not_release(self):
        ratings=[]
        for case in range(2):
            for arm in ('v8','v9'):
                ratings.append({'case_id':str(case),'reviewer_id':'reviewer','arm':arm,
                                'scores':{m:3 if arm=='v8' else 4 for m in METRICS},'critical_violations':0})
        self.assertEqual('REVIEW',evaluate_benchmark({'ratings':ratings},minimum_pairs=2)['status'])

if __name__=='__main__': unittest.main()
