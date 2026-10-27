"""P0 negative controls for the v9 authorship-claim declaration checker.

Each case names the P0 defect from references/v9/defects.md that it guards.
Every refusal asserts the exit status and the machine-readable reason code.
"""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNNER = Path(__file__).resolve().parents[2] / "scripts" / "wi-authorship.py"
_spec = importlib.util.spec_from_file_location("wi_authorship", str(RUNNER))
WA = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(WA)

DRAFT = ("I built a miniature town in my garage in 2024. "
         "The county reported 412 permits in 2023. "
         "Local shops lost 18 percent of revenue in 2022. "
         "Researchers found that 3 of 5 hobbyists quit within a year.")
NOTES = "I built a miniature town in my garage in 2024."


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class Base(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.write("draft.txt", DRAFT)
        self.write("notes.txt", NOTES)
        self.case = {
            "schema": "wi9-authorship-2",
            "document": {"path": "draft.txt", "origin": "human_authored", "arena": "journalism",
                         "venue_policy": "human_only", "intended_use": "submission",
                         "expected_sha256": sha(DRAFT)},
            "contribution_log": [{"kind": "human_original"}],
            "evidence": [{"id": "e1", "claim": "The author built a miniature town.",
                          "kind": "firsthand", "source_path": "notes.txt", "sha256": sha(NOTES),
                          "exact_excerpt": NOTES, "source_origin": "human_authored",
                          "experience_state": "observed", "consent": True}],
            "document_claim_anchors": [{"exact_excerpt": NOTES, "evidence_id": "e1"}],
            "voice_samples": [],
        }

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def cli(self, case, command="audit", raw=None):
        path = self.root / "dossier.json"
        path.write_text(raw if raw is not None else json.dumps(case), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(RUNNER), command, "--input", str(path)],
                              capture_output=True, text=True)
        self.assertNotIn("Traceback", proc.stderr)
        return proc.returncode, json.loads(proc.stdout), proc.stderr

    def codes(self, report):
        return {f["code"] for f in report["findings"]}

    def assert_hold(self, case, code, command="audit"):
        exit_code, report, _ = self.cli(case, command)
        self.assertEqual(3, exit_code, report)
        self.assertEqual("HOLD", report["status"])
        self.assertIn(code, self.codes(report))
        self.assertFalse(report["release_authorized"])
        return report

    def make_covered(self):
        """A submission whose every discovered claim is anchored."""
        self.write("draft.txt", NOTES)
        self.case["document"]["expected_sha256"] = sha(NOTES)
        return self.case


class InputParsing(Base):  # P0-05
    def test_non_object_roots_hold_structurally(self):
        for raw in ("[]", "null", "7", '"text"', "true"):
            exit_code, report, _ = self.cli(None, raw=raw)
            self.assertEqual(3, exit_code, raw)
            self.assertIn("ROOT_NOT_OBJECT", self.codes(report), raw)

    def test_malformed_json_holds(self):
        exit_code, report, _ = self.cli(None, raw="{not json")
        self.assertEqual(3, exit_code)
        self.assertIn("DOSSIER_JSON_INVALID", self.codes(report))

    def test_deep_nesting_holds(self):
        exit_code, report, _ = self.cli(None, raw="[" * 60 + "]" * 60)
        self.assertEqual(3, exit_code)
        self.assertIn("DOSSIER_TOO_DEEP", self.codes(report))

    def test_wrong_nested_types_hold(self):
        self.case["document"] = ["not", "an", "object"]
        self.assert_hold(self.case, "DOCUMENT_REQUIRED")
        self.setUp()
        self.case["document_claim_anchors"] = "a string"
        self.assert_hold(self.case, "DOCUMENT_CLAIM_ANCHORS_INVALID")
        self.setUp()
        self.case["document"]["arena"] = 12
        self.assert_hold(self.case, "ARENA_INVALID")


class FileBoundary(Base):  # P0-06, P0-07
    def test_oversized_document_refused_before_full_read(self):
        with open(self.root / "big.txt", "wb") as out:
            out.seek(WA.MAX_BYTES)
            out.write(b"x")
        self.case["document"]["path"] = "big.txt"
        report = self.assert_hold(self.case, "DOCUMENT_NOT_READABLE")
        self.assertIn("FILE_TOO_LARGE", json.dumps(report))

    def test_oversized_dossier_refused(self):
        exit_code, report, _ = self.cli(None, raw='{"pad": "' + "x" * WA.MAX_DOSSIER_BYTES + '"}')
        self.assertEqual(3, exit_code)
        self.assertIn("FILE_TOO_LARGE", self.codes(report))

    def test_absolute_and_parent_paths_refused(self):
        for bad, code in (("/etc/hosts", "PATH_ABSOLUTE"), ("../outside.txt", "PATH_ESCAPE"),
                          ("sub/../../outside.txt", "PATH_ESCAPE")):
            self.setUp()
            self.case["evidence"][0]["source_path"] = bad
            report = self.assert_hold(self.case, "SOURCE_NOT_READABLE")
            self.assertIn(code, json.dumps(report))

    def test_symlinked_file_refused(self):
        outside = tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt")
        outside.write(NOTES)
        outside.close()
        self.addCleanup(os.unlink, outside.name)
        os.symlink(outside.name, str(self.root / "link.txt"))
        self.case["evidence"][0]["source_path"] = "link.txt"
        report = self.assert_hold(self.case, "SOURCE_NOT_READABLE")
        self.assertIn("PATH_SYMLINK", json.dumps(report))

    def test_symlinked_directory_component_refused(self):
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(outside.cleanup)
        Path(outside.name, "notes.txt").write_text(NOTES, encoding="utf-8")
        os.symlink(outside.name, str(self.root / "linkdir"))
        self.case["evidence"][0]["source_path"] = "linkdir/notes.txt"
        report = self.assert_hold(self.case, "SOURCE_NOT_READABLE")
        self.assertIn("PATH_SYMLINK", json.dumps(report))

    def test_symlinked_dossier_refused(self):
        real = self.root / "real.json"
        real.write_text(json.dumps(self.case), encoding="utf-8")
        os.symlink(str(real), str(self.root / "alias.json"))
        proc = subprocess.run([sys.executable, str(RUNNER), "audit", "--input",
                               str(self.root / "alias.json")], capture_output=True, text=True)
        self.assertEqual(3, proc.returncode)
        self.assertIn("PATH_SYMLINK", proc.stdout)

    def test_invalid_utf8_refused(self):
        (self.root / "bad.txt").write_bytes(b"\xff\xfe broken")
        self.case["evidence"][0]["source_path"] = "bad.txt"
        report = self.assert_hold(self.case, "SOURCE_NOT_READABLE")
        self.assertIn("FILE_NOT_UTF8", json.dumps(report))


class Immutability(Base):  # P0-08
    def test_changed_draft_after_pin_holds(self):
        self.make_covered()
        self.write("draft.txt", NOTES + " ")
        self.assert_hold(self.case, "DOCUMENT_DIGEST_MISMATCH")

    def test_submission_without_pinned_digest_holds(self):
        del self.case["document"]["expected_sha256"]
        self.assert_hold(self.case, "DOCUMENT_DIGEST_UNPINNED")

    def test_strict_submission_requires_pinned_sources(self):
        self.make_covered()
        del self.case["evidence"][0]["sha256"]
        self.assert_hold(self.case, "SOURCE_DIGEST_UNPINNED")


class EvidenceIdentity(Base):  # P0-04
    def test_duplicate_evidence_id_holds(self):
        self.case["evidence"].append(copy.deepcopy(self.case["evidence"][0]))
        self.assert_hold(self.case, "EVIDENCE_ID_DUPLICATE")

    def test_missing_evidence_id_holds(self):
        self.case["evidence"][0]["id"] = "   "
        self.assert_hold(self.case, "EVIDENCE_ID_MISSING")

    def test_dangling_anchor_holds(self):
        self.case["document_claim_anchors"][0]["evidence_id"] = "nobody"
        self.assert_hold(self.case, "DOCUMENT_EVIDENCE_NOT_FOUND")

    def test_ambiguous_anchor_needs_offset(self):
        twice = NOTES + " " + NOTES
        self.write("draft.txt", twice)
        self.case["document"]["expected_sha256"] = sha(twice)
        self.assert_hold(self.case, "DOCUMENT_ANCHOR_AMBIGUOUS")

    def test_wrong_offset_holds(self):
        self.case["document_claim_anchors"][0]["start"] = 5
        self.assert_hold(self.case, "DOCUMENT_ANCHOR_OFFSET_MISMATCH")

    def test_correct_offset_resolves(self):
        self.make_covered()
        self.case["document_claim_anchors"][0]["start"] = 0
        exit_code, report, _ = self.cli(self.case)
        self.assertEqual(0, exit_code, report["findings"])


class ClaimCoverage(Base):  # P0-02, P0-03
    def test_one_safe_anchor_cannot_carry_three_unsourced_claims(self):
        report = self.assert_hold(self.case, "CLAIM_UNANCHORED")
        unanchored = [c for c in report["claim_coverage"] if not c["anchored"]]
        self.assertGreaterEqual(len(unanchored), 3)

    def test_internal_review_reports_coverage_without_holding_on_it(self):
        self.case["document"]["intended_use"] = "internal_review"
        exit_code, report, _ = self.cli(self.case)
        self.assertEqual(0, exit_code, report["findings"])
        levels = {f["level"] for f in report["findings"] if f["code"] == "CLAIM_UNANCHORED"}
        self.assertEqual({"advisory"}, levels)

    def test_resolved_anchor_is_not_reported_as_support(self):
        self.make_covered()
        exit_code, report, _ = self.cli(self.case)
        self.assertEqual(0, exit_code, report["findings"])
        self.assertEqual("ANCHOR_RESOLVED", report["evidence_anchors"][0]["anchor"])
        self.assertEqual("unadjudicated", report["evidence_anchors"][0]["support_status"])
        self.assertTrue(all(c["support"] == "anchor_resolved_unadjudicated"
                            for c in report["claim_coverage"]))

    def test_needs_source_and_conflicted_evidence_hold_submission(self):
        for state in ("needs_source", "conflicted"):
            self.setUp()
            self.make_covered()
            self.case["evidence"][0]["support_status"] = state
            self.assert_hold(self.case, "SUPPORT_UNRESOLVED")

    def test_planned_work_cannot_support_firsthand(self):
        self.make_covered()
        self.case["evidence"][0]["experience_state"] = "planned"
        self.assert_hold(self.case, "FIRSTHAND_NOT_PERFORMED")


class DeclarationsAndVenue(Base):  # P0-01, P0-09, P0-10
    def test_forged_human_declaration_reaches_review_never_verified(self):
        self.make_covered()
        exit_code, report, stderr = self.cli(self.case)
        self.assertEqual(0, exit_code, report["findings"])
        self.assertEqual("REVIEW", report["status"])
        self.assertEqual("self_reported", report["declaration_status"])
        self.assertEqual("limited_checks", report["decision_scope"])
        self.assertFalse(report["release_authorized"])
        self.assertNotIn("VERIFIED", json.dumps(report))
        self.assertIn("not permission to publish", stderr)

    def test_human_label_with_declared_ai_prose_holds_on_any_venue(self):
        self.case["document"]["venue_policy"] = "unrestricted"
        self.case["contribution_log"] = [{"kind": "human_original"},
                                         {"kind": "ai_generated_prose"}]
        self.assert_hold(self.case, "ORIGIN_CONTRADICTS_LOG")

    def test_human_only_holds_unlisted_ai_research(self):
        self.make_covered()
        self.case["contribution_log"].append({"kind": "ai_research"})
        self.assert_hold(self.case, "ASSISTANCE_NOT_PERMITTED")

    def test_human_only_permits_recorded_assistance(self):
        self.make_covered()
        self.case["contribution_log"].append({"kind": "mechanical_proofread"})
        self.case["venue_contract"] = {"venue": "Example Desk",
                                       "allowed_assistance": ["mechanical_proofread"]}
        exit_code, report, _ = self.cli(self.case)
        self.assertEqual(0, exit_code, report["findings"])

    def test_human_only_contract_cannot_allow_ai_prose(self):
        self.case["venue_contract"] = {"allowed_assistance": ["ai_generated_prose"]}
        self.assert_hold(self.case, "VENUE_CONTRACT_CONTRADICTION")

    def test_expired_venue_policy_holds(self):
        self.case["venue_contract"] = {"expires_at": "2020-01-01T00:00:00+00:00"}
        self.assert_hold(self.case, "VENUE_CONTRACT_EXPIRED")

    def test_audit_never_returns_release(self):
        self.make_covered()
        _, report, _ = self.cli(self.case)
        self.assertNotIn(report["status"], {"RELEASE", "RELEASE_ELIGIBLE"})


class Release(Base):  # P0-10, P0-11
    def eligible(self):
        self.make_covered()
        self.case["venue_contract"] = {"venue": "Example Desk", "allowed_operations": ["submit"],
                                       "deadline": "2999-01-01T00:00:00+00:00"}
        self.case["review_decision"] = {
            "outcome": "approve", "actor": "Antonio T. Smith Jr.", "actor_kind": "human",
            "target_sha256": sha(NOTES), "decided_at": "2026-10-27T12:00:00-05:00",
            "authority": {"holder": "Antonio T. Smith Jr.", "scope": ["release"],
                          "venues": ["Example Desk"], "expires_at": "2999-01-01T00:00:00+00:00"}}
        return self.case

    def test_bound_decision_is_release_eligible_and_sends_nothing(self):
        exit_code, report, _ = self.cli(self.eligible(), "release")
        self.assertEqual(0, exit_code, report["findings"])
        self.assertEqual("RELEASE_ELIGIBLE", report["status"])
        self.assertFalse(report["transmission_performed"])

    def test_release_refusals(self):
        mutations = {
            "DECISION_TARGET_STALE": lambda c: c["review_decision"].update(target_sha256="0" * 64),
            "AUTHORITY_EXPIRED": lambda c: c["review_decision"]["authority"].update(
                expires_at="2020-01-01T00:00:00+00:00"),
            "AUTHORITY_VENUE": lambda c: c["review_decision"]["authority"].update(venues=["Other"]),
            "AUTHORITY_SCOPE": lambda c: c["review_decision"]["authority"].update(scope=["edit"]),
            "AUTHORITY_HOLDER_MISMATCH": lambda c: c["review_decision"]["authority"].update(
                holder="Someone Else"),
            "DECISION_NOT_HUMAN": lambda c: c["review_decision"].update(actor_kind="model"),
            "DECISION_TIME_INVALID": lambda c: c["review_decision"].update(
                decided_at="2026-10-27T12:00:00"),
            "DECISION_TIME_FUTURE": lambda c: c["review_decision"].update(
                decided_at="2999-01-01T00:00:00+00:00"),
            "DECISION_REJECTED": lambda c: c["review_decision"].update(outcome="reject"),
            "DEADLINE_PASSED": lambda c: c["venue_contract"].update(
                deadline="2020-01-01T00:00:00+00:00"),
            "SUBMIT_NOT_PERMITTED": lambda c: c["venue_contract"].update(
                allowed_operations=["research"]),
            "DECISION_REQUIRED": lambda c: c.pop("review_decision"),
            "AUDIT_NOT_REVIEW": lambda c: c["document"].update(origin="ai_generated"),
            "NOT_A_SUBMISSION": lambda c: c["document"].update(intended_use="internal_review"),
        }
        for code, mutate in mutations.items():
            with self.subTest(code=code):
                self.setUp()
                case = self.eligible()
                mutate(case)
                self.assert_hold(case, code, "release")

    def test_grant_that_expired_after_a_valid_decision_still_holds(self):
        # The decision was inside the grant's window; the window has since closed.
        case = self.eligible()
        case["review_decision"]["decided_at"] = "2019-06-01T00:00:00+00:00"
        case["review_decision"]["authority"]["expires_at"] = "2020-01-01T00:00:00+00:00"
        self.assert_hold(case, "AUTHORITY_EXPIRED", "release")

    def test_draft_edited_after_approval_is_stale(self):
        case = self.eligible()
        self.write("draft.txt", NOTES + " Edited.")
        case["document"]["expected_sha256"] = sha(NOTES + " Edited.")
        self.assert_hold(case, "DECISION_TARGET_STALE", "release")


if __name__ == "__main__":
    unittest.main()
