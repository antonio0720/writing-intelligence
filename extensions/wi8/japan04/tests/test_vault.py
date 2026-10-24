import tempfile
import unittest
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from japan_story_os.vault import DraftVault,ConflictError
from japan_story_os.contracts import ContractError

class VaultTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.v=DraftVault(Path(self.tmp.name)/'private')
    def tearDown(self):self.tmp.cleanup()
    def save(self,text='Original\n'):return self.v.save('chapter-1',text)
    def test_private_vault_initial(self):self.assertTrue(self.v.index.is_file())
    def test_first_draft_exact_bytes(self):
        self.save('彼女は帰った。\n');self.assertEqual(self.v.read('chapter-1'),'彼女は帰った。\n')
    def test_first_revision_zero(self):self.assertEqual(self.save()['revision'],0)
    def test_stale_write_fails(self):
        self.save();self.assertRaises(ConflictError,self.v.save,'chapter-1','different')
    def test_revision_with_cas(self):
        self.save();self.assertEqual(self.v.save('chapter-1','Second',0)['revision'],1)
    def test_old_bytes_survive(self):
        self.save();self.v.save('chapter-1','Second',0)
        self.assertEqual(self.v.read('chapter-1',0),'Original\n')
    def test_proposal_does_not_edit(self):
        d=self.save();p=self.v.propose('chapter-1',d['sha256'],'Suggested','reason')
        self.assertFalse(p['changes_committed']);self.assertEqual(self.v.read('chapter-1'),'Original\n')
    def test_rejection_restores_exact_bytes(self):
        d=self.save();p=self.v.propose('chapter-1',d['sha256'],'Suggested','reason')
        self.v.decide(p['proposal_id'],'author','reject');self.assertEqual(self.v.read('chapter-1'),'Original\n')
    def test_author_can_adopt(self):
        d=self.save();p=self.v.propose('chapter-1',d['sha256'],'Suggested','reason')
        self.v.decide(p['proposal_id'],'author','accept');self.assertEqual(self.v.read('chapter-1'),'Suggested')
    def test_assistant_cannot_accept(self):
        d=self.save();p=self.v.propose('chapter-1',d['sha256'],'Suggested','reason')
        self.assertRaises(ContractError,self.v.decide,p['proposal_id'],'assistant','accept')
    def test_guardian_cannot_rewrite_private_draft(self):
        d=self.save();p=self.v.propose('chapter-1',d['sha256'],'Suggested','reason')
        self.assertRaises(ContractError,self.v.decide,p['proposal_id'],'guardian','accept')
    def test_double_accept_refused(self):
        d=self.save();p=self.v.propose('chapter-1',d['sha256'],'Suggested','reason');self.v.decide(p['proposal_id'],'author','accept')
        self.assertRaises(ConflictError,self.v.decide,p['proposal_id'],'author','accept')
    def test_stale_proposal_refused(self):
        d=self.save();p=self.v.propose('chapter-1',d['sha256'],'Suggested','reason');self.v.save('chapter-1','New original',0)
        self.assertRaises(ConflictError,self.v.decide,p['proposal_id'],'author','accept')
    def test_suggested_origin_needs_proposal(self):self.assertRaises(ContractError,self.v.save,'chapter-1','Text',None,'AI_GENERATED')
    def test_metadata_minimization(self):
        self.save();r=self.v.preview_publication('chapter-1',{'school':'school-secret','legal_name':'Minor Name','title':'Fantasy','home_address':'street'})
        self.assertEqual(r['metadata'],{'title':'Fantasy'});self.assertFalse(r['external_effects'])
    def test_never_publishes(self):self.save();self.assertEqual(self.v.preview_publication('chapter-1')['status'],'NOT_PUBLISHED')
    def test_tampered_blob_refused(self):
        s=self.save();p=self.v._blob_path(s['sha256']);p.write_text('Modified')
        self.assertRaises(ContractError,self.v.read,'chapter-1')
    def test_symlink_refused(self):
        src=Path(self.tmp.name)/'sample';src.write_text('data');target=Path(self.tmp.name)/'unsafe';target.symlink_to(src)
        self.assertRaises(ContractError,DraftVault,target)
    def test_missing_draft_refused(self):
        src=Path(self.tmp.name)/'notafile';src.mkdir()
        self.save()
        self.assertRaises(KeyError,self.v.read,'missing-draft')
    def test_history_has_origin(self):
        self.save();self.assertEqual(self.v.history('chapter-1')[0]['origin'],'human_authored')
    def test_two_chapters_isolated(self):
        self.save();self.v.save('chapter-2','B');self.assertEqual(self.v.read('chapter-1'),'Original\n')
    def test_malformed_revision_not_silent(self):
        self.save();self.assertRaises(KeyError,self.v.read,'chapter-1',99)
    def test_lock_concurrency_refuses(self):
        h=self.v._lock()
        try:self.assertRaises(ConflictError,self.v.save,'chapter-1','text')
        finally:self.v._unlock(h)

if __name__=='__main__':unittest.main()
