"""Negative controls for the independent review of the reference kernel.

Each case reproduces a confirmed finding (references/v9/defects.md, R-07..R-14)
and asserts the repaired behaviour.
"""
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wi9_hotphrases import scan_text
from wi9_phrase_review import audit_decisions
from wi9_composition import prepare_request, inspect_candidate
from wi9_core import preflight, MAX_LIST


def dossier(policy):
    return {"document": {"intended_use": "internal_review", "arena": "essay", "mission": "m"},
            "venue": {"policy": policy},
            "evidence": [{"id": "e1", "claim": "c", "kind": "firsthand", "exact_excerpt": "quoted words",
                          "consent": True, "origin": "human_authored"}]}


class HotPhraseCost(unittest.TestCase):  # R-07, R-08
    def test_long_whitespace_after_a_closing_word_is_linear(self):
        t = time.time()
        scan_text("ultimately" + " " * 40000)
        self.assertLess(time.time() - t, 5)

    def test_many_masked_spans_are_cheap(self):
        # The reviewer's case: 60,000 masked spans, then a fence holding 17,000 matches.
        text = "`x` " * 60000 + "\n```\n" + "that matters. " * 17000 + "\n```\n"
        self.assertLess(len(text), 500000)
        t = time.time()
        report = scan_text(text)
        self.assertLess(time.time() - t, 10)
        self.assertEqual(0, report["finding_count"])

    def test_masking_still_masks_and_still_reports(self):
        report = scan_text('She said "that matters." That matters here.')
        self.assertEqual(1, report["finding_count"])


class CompositionFailsClosed(unittest.TestCase):  # R-09, R-10
    def test_unrecognised_policies_never_open_a_prose_request(self):
        for policy in ("human-only", "Human_Only", "humanonly", "ai_forbidden", ["x"], None, ""):
            with self.subTest(policy=policy):
                self.assertEqual("HOLD", prepare_request(dossier(policy))["status"])

    def test_permitted_policy_still_opens_a_request(self):
        self.assertEqual("REQUEST_READY", prepare_request(dossier("ai_permitted"))["status"])

    def test_malformed_evidence_ids_hold_without_a_traceback(self):
        request = prepare_request(dossier("ai_permitted"))
        for ids in ([["x"]], None, 5, [5]):
            with self.subTest(ids=ids):
                candidate = {"schema": "wi9.candidate/1", "paragraphs": [
                    {"text": "t", "evidence_ids": ids, "author_review_required": True,
                     "asserts_firsthand": True}]}
                self.assertEqual("HOLD", inspect_candidate(candidate, request)["status"])

    def test_empty_quotation_is_not_verified(self):
        request = prepare_request(dossier("ai_permitted"))
        candidate = {"schema": "wi9.candidate/1", "paragraphs": [
            {"text": "t", "evidence_ids": ["e1"], "author_review_required": True,
             "direct_quotes": [{"source_id": "e1", "exact_text": ""}]}]}
        result = inspect_candidate(candidate, request)
        self.assertIn("QUOTATION_UNVERIFIED:0", result["errors"])


class ReviewLedgerHonesty(unittest.TestCase):  # R-11, R-12
    def setUp(self):
        self.text = "That matters. Studies show it. Here's the thing about it."
        self.report = scan_text(self.text)
        self.empty = {"schema": "wi9.editorial.review/1",
                      "document_sha256": self.report["document_sha256"],
                      "rules_sha256": self.report["rules_sha256"], "decisions": []}

    def test_nothing_reviewed_is_not_review(self):
        self.assertGreater(self.report["finding_count"], 1)
        out = audit_decisions(self.text, self.report, self.empty)
        self.assertEqual("HOLD", out["status"])
        self.assertTrue(any(i.startswith("FINDINGS_UNREVIEWED") for i in out["issues"]))

    def test_forged_report_with_findings_removed_holds(self):
        forged = dict(self.report, findings=[])
        out = audit_decisions(self.text, forged, self.empty)
        self.assertEqual("HOLD", out["status"])
        self.assertIn("REPORT_NOT_REPRODUCED", out["issues"])

    def test_unhashable_decision_fields_hold_without_a_traceback(self):
        bad = dict(self.empty, decisions=[{"rule_id": ["x"], "start": 0, "end": 1, "excerpt": "T"}])
        out = audit_decisions(self.text, self.report, bad)
        self.assertEqual("HOLD", out["status"])


class CoreWorkCaps(unittest.TestCase):  # R-14
    def test_oversized_evidence_list_holds(self):
        with tempfile.TemporaryDirectory() as d:
            data = {"schema": "wi9.preflight/1", "document": {}, "venue": {},
                    "evidence": [{}] * (MAX_LIST + 1)}
            result = preflight(data, d)
            self.assertEqual("HOLD", result["status"])
            self.assertEqual("LIST_TOO_LONG", result["issues"][0]["code"])


if __name__ == "__main__":
    unittest.main()
