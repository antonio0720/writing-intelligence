import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
INSTALL=ROOT/'tools/additive_install.py'
VERIFY=ROOT/'tools/verify_manifest.py'
CLI=ROOT/'cli/wi8_japan.py'

class IntegrationTest(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def gitrepo(self):
        repo=self.root/'project';repo.mkdir()
        def cmd(*argv):return subprocess.check_output(['git','-C',str(repo),*argv],text=True,stderr=subprocess.DEVNULL).strip()
        cmd('init','-q');cmd('config','user.email','test@local.invalid');cmd('config','user.name','Tester')
        (repo/'README.md').write_text('test repo')
        cmd('add','.');cmd('commit','-qm','init');return repo,cmd('rev-parse','HEAD')
    def install(self,repo,sha,apply=False):
        return subprocess.run([sys.executable,str(INSTALL),'--repo',str(repo),'--expected-head',sha]+(['--apply'] if apply else []),capture_output=True,text=True)
    def test_manifest_check(self):self.assertEqual(subprocess.run([sys.executable,str(VERIFY)],capture_output=True).returncode,0)
    def test_manifest_160_unique(self):
        r=json.loads((ROOT/'references/JAPAN_REQUIREMENTS_181_340.json').read_text())
        self.assertEqual([x['id'] for x in r['requirements']],list(range(181,341)))
    def test_waves_planned(self):
        r=json.loads((ROOT/'plans/japan04_waves.json').read_text())
        self.assertEqual(len(r['waves']),20);self.assertTrue(all(x['status']=='planned' for x in r['waves']))
    def test_seeds_all_unadopted(self):
        d=json.loads((ROOT/'fixtures/proposed_seed_catalog.json').read_text())
        self.assertEqual(len(d['entries']),6);self.assertTrue(all(not x['adopted_by_child'] for x in d['entries']))
    def test_pdf_index_97_pages(self):self.assertEqual(len(json.loads((ROOT/'references/ORIGINAL_PDF_PAGE_INDEX.json').read_text())['records']),97)
    def test_install_dry_run_read_only(self):
        repo,sha=self.gitrepo();r=self.install(repo,sha)
        self.assertEqual(r.returncode,0);self.assertFalse((repo/'extensions/wi8/japan04').exists())
    def test_install_actual_additive(self):
        repo,sha=self.gitrepo();r=self.install(repo,sha,True)
        self.assertEqual(r.returncode,0,msg=r.stderr);self.assertTrue((repo/'extensions/wi8/japan04/src/japan_story_os/contracts.py').exists())
        self.assertEqual(subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip(),sha)
    def test_no_second_install_overwrite(self):
        repo,sha=self.gitrepo();self.assertEqual(self.install(repo,sha,True).returncode,0)
        self.assertNotEqual(self.install(repo,sha,True).returncode,0)
    def test_install_changed_head_refusal(self):
        repo,sha=self.gitrepo();self.assertNotEqual(self.install(repo,'a'*40,True).returncode,0)
    def test_install_dirty_worktree_refusal(self):
        repo,sha=self.gitrepo();(repo/'dirty').write_text('new');self.assertNotEqual(self.install(repo,sha,True).returncode,0)
    def test_schema_contract_json_parse(self):
        files=list((ROOT/'schemas').glob('*.schema.json'));self.assertEqual(len(files),12)
        self.assertTrue(all(json.loads(p.read_text())['$schema'].endswith('2020-12/schema') for p in files))
    def test_japanese_unicode_fixture(self):
        s=(ROOT/'fixtures/sample_project.json').read_text()
        self.assertIn('結衣',s)
    def test_cli_check_exit_zero_or_review(self):
        r=subprocess.run([sys.executable,str(CLI),'check',str(ROOT/'fixtures/sample_project.json')],capture_output=True,text=True)
        self.assertEqual(r.returncode,0);self.assertIn('JP_SOURCE_REQUIRED',r.stdout)
    def test_cli_preflight_fails_closed(self):
        r=subprocess.run([sys.executable,str(CLI),'preflight',str(ROOT/'fixtures/sample_project.json')],capture_output=True,text=True)
        self.assertEqual(r.returncode,2);self.assertIn('PREVIEW_ONLY',r.stdout)
    def test_cli_untrusted_refuses_instructions(self):
        r=subprocess.run([sys.executable,str(CLI),'untrusted-scan',str(ROOT/'fixtures/untrusted_lore.txt')],capture_output=True,text=True)
        self.assertEqual(r.returncode,0);self.assertIn('possible_injection',r.stdout)
    def test_cli_migration_preview_noncanonical(self):
        r=subprocess.run([sys.executable,str(CLI),'migration-preview',str(ROOT/'fixtures/legacy_v1.json')],capture_output=True,text=True)
        self.assertEqual(r.returncode,0);self.assertIn('PREVIEW_ONLY_NOT_COMMITTED',r.stdout)

if __name__=='__main__':unittest.main()
