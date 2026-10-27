"""Bounded negative controls for the experimental v9 authorship diagnostic."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNNER = Path(__file__).resolve().parents[2] / "scripts" / "wi-authorship.py"


class AuthorshipTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        (self.root / "draft.txt").write_text("I built a miniature town.", encoding="utf-8")
        (self.root / "notes.txt").write_text("I built a miniature town.", encoding="utf-8")
        self.base = {
            "schema": "wi9-authorship-1",
            "document": {"path": "draft.txt", "origin": "human_authored",
                         "arena": "journalism", "venue_policy": "human_only",
                         "intended_use": "internal_review"},
            "evidence": [{
                "id": "e1", "claim": "A personal miniature was built.",
                "kind": "firsthand", "source_path": "notes.txt",
                "exact_excerpt": "I built a miniature town.",
                "source_origin": "human_authored", "consent": True
            }],
            "voice_samples": []
        }

    def run_case(self, case):
        fp = self.root / "dossier.json"
        fp.write_text(json.dumps(case), encoding="utf-8")
        result = subprocess.run([sys.executable, str(RUNNER), "audit", "--input", str(fp)],
                                capture_output=True, text=True)
        return result.returncode, json.loads(result.stdout)

    def assert_hold(self, case, code):
        exit_code, report = self.run_case(case)
        self.assertEqual(3, exit_code)
        self.assertEqual("HOLD", report["status"])
        self.assertIn(code, {f["code"] for f in report["findings"]})

    def test_human_only_rejects_ai_submission(self):
        self.base["document"].update(origin="ai_generated", intended_use="submission")
        self.assert_hold(self.base, "HUMAN_ONLY_CONFLICT")

    def test_human_only_rejects_ai_assisted_submission(self):
        self.base["document"].update(origin="ai_assisted", intended_use="submission")
        self.assert_hold(self.base, "HUMAN_ONLY_CONFLICT")

    def test_firsthand_cannot_be_inferred_from_ai(self):
        self.base["evidence"][0]["source_origin"] = "ai_generated"
        self.assert_hold(self.base, "FIRSTHAND_UNVERIFIED")

    def test_exact_evidence_anchor_mandatory(self):
        self.base["evidence"][0]["exact_excerpt"] = "A never-said sentence."
        self.assert_hold(self.base, "ANCHOR_MISSING")

    def test_source_hash_mismatch(self):
        self.base["evidence"][0]["sha256"] = "f" * 64
        self.assert_hold(self.base, "SOURCE_DIGEST_MISMATCH")

    def test_author_consent_required(self):
        self.base["evidence"][0]["consent"] = False
        self.assert_hold(self.base, "CONSENT_ABSENT")

    def test_path_escape_blocked(self):
        self.base["evidence"][0]["source_path"] = "../sensitive.txt"
        self.assert_hold(self.base, "SOURCE_NOT_READABLE")

    def test_advisory_is_not_authorship_certificate(self):
        exit_code, report = self.run_case(self.base)
        self.assertEqual(0, exit_code)
        self.assertEqual("REVIEW", report["status"])
        self.assertTrue(any("not independently" in s for s in report["limitations"]))
        self.assertIn("VOICE_BASELINE_INSUFFICIENT",
                      {f["code"] for f in report["findings"]})

    def test_research_demo_is_not_submission(self):
        self.base["document"].update(origin="ai_generated", intended_use="research_demo")
        exit_code, report = self.run_case(self.base)
        self.assertEqual(0, exit_code)
        self.assertEqual("REVIEW", report["status"])
        self.assertIn("RESEARCH_ONLY", {f["code"] for f in report["findings"]})

    def test_bad_schema_holds(self):
        self.base["schema"] = "made-up"
        self.assert_hold(self.base, "SCHEMA_INVALID")


if __name__ == "__main__":
    unittest.main()
