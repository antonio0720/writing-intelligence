"""WI9-02: each writer's firsthand material stays in their own private vault.

Every test uses synthetic text written for the test. Each refusal is asserted by
exit status and reason code, beside a positive twin that must pass.
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wi9_vault  # noqa: E402

NOTE = ("On 2026-03-02 I glued the last tile onto the harbour model. "
        "It took eleven evenings. The roof still warps when the room is damp.")
PLAN = "Next spring we plan to build a solar community model with forty houses."


def run(*argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = wi9_vault.main(list(argv))
    return code, json.loads(out.getvalue())


class VaultBase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = str(self.base / "vault")
        code, out = run("init", "--root", self.root, "--project", "harbour")
        self.assertEqual(0, code, out)

    def add(self, item_id, text, label="observed", *extra):
        path = self.base / ("%s.txt" % item_id)
        path.write_text(text, encoding="utf-8")
        return run("add", "--root", self.root, "--file", str(path), "--id", item_id, "--label", label,
                   "--consent", *extra)

    def check(self, claims, project="harbour"):
        path = self.base / "claims.json"
        path.write_text(json.dumps({"schema": "wi9.vault-claims/1", "project": project, "claims": claims}))
        return run("check", "--root", self.root, "--claims", str(path))

    def codes(self, out):
        return {i["code"] for i in out["issues"]}


class Custody(VaultBase):
    def test_folder_is_private_and_holds_no_plaintext_log(self):
        self.add("n1", NOTE, "observed", "--valid-at", "2026-03-02")
        mode = os.stat(self.root).st_mode & 0o777
        self.assertEqual(0o700, mode)
        log = (Path(self.root) / "events.jsonl").read_text()
        self.assertNotIn("harbour model", log)
        code, listing = run("list", "--root", self.root)
        self.assertEqual(0, code)
        self.assertTrue(listing["event_log_intact"])
        self.assertNotIn("harbour model", json.dumps(listing))

    def test_vault_inside_a_git_repository_is_refused(self):
        repo = self.base / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        code, out = run("init", "--root", str(repo / "notes"), "--project", "x")
        self.assertEqual(3, code)
        self.assertIn("STORE_INSIDE_REPOSITORY", self.codes(out))

    def test_existing_vault_later_placed_inside_a_repository_is_refused(self):
        subprocess.run(["git", "init", "-q", str(self.base)], check=True)
        code, out = run("list", "--root", self.root)
        self.assertEqual(3, code)
        self.assertIn("STORE_INSIDE_REPOSITORY", self.codes(out))

    def test_vault_folder_that_is_a_symlink_is_refused(self):
        link = self.base / "link"
        link.symlink_to(self.root)
        code, out = run("list", "--root", str(link))
        self.assertEqual(3, code)
        self.assertIn("PATH_SYMLINK", self.codes(out))

    def test_adding_requires_consent(self):
        path = self.base / "x.txt"
        path.write_text(NOTE)
        code, out = run("add", "--root", self.root, "--file", str(path), "--id", "x", "--label", "observed")
        self.assertEqual(3, code)
        self.assertIn("CONSENT_REQUIRED", self.codes(out))

    def test_a_future_dated_note_is_refused(self):
        code, out = self.add("f", NOTE, "observed", "--valid-at", "2999-01-01")
        self.assertEqual(3, code)
        self.assertIn("DATE_IMPLAUSIBLE", self.codes(out))

    def test_edited_event_log_is_detected(self):
        self.add("n1", NOTE)
        log = Path(self.root) / "events.jsonl"
        lines = log.read_text().splitlines()
        entry = json.loads(lines[-1])
        entry["item"] = "someone-else"
        lines[-1] = json.dumps(entry, sort_keys=True)
        log.write_text("\n".join(lines) + "\n")
        code, out = run("list", "--root", self.root)
        self.assertEqual(3, code)
        self.assertIn("VAULT_LOG_BROKEN", self.codes(out))


class Claims(VaultBase):
    def claim(self, item="n1", excerpt="I glued the last tile onto the harbour model", **kw):
        c = {"id": "c1", "text": "I built the harbour model over eleven evenings.",
             "evidence": [{"item": item, "excerpt": excerpt}]}
        c.update(kw)
        return c

    def test_anchored_first_person_claim_reaches_review(self):
        self.add("n1", NOTE, "observed", "--valid-at", "2026-03-02")
        code, out = self.check([self.claim()])
        self.assertEqual(0, code, out)
        self.assertEqual("REVIEW", out["status"])
        self.assertFalse(out["release_authorized"])
        self.assertEqual("anchored", out["claims"][0]["state"])

    def test_first_person_claim_with_no_source_holds(self):
        code, out = self.check([{"id": "c1", "text": "I built a solar community model."}])
        self.assertEqual(3, code)
        self.assertIn("CLAIM_NEEDS_SOURCE", self.codes(out))
        self.assertEqual(["c1"], out["needs_source"])

    def test_general_claim_without_source_is_not_held(self):
        code, out = self.check([{"id": "c1", "text": "Scale models reward patience."}])
        self.assertEqual(0, code, out)
        self.assertEqual("not_autobiographical", out["claims"][0]["state"])

    def test_roadmap_presented_as_a_completed_build_holds(self):
        self.add("p1", PLAN, "planned")
        code, out = self.check([self.claim(item="p1", excerpt="build a solar community model")])
        self.assertEqual(3, code)
        self.assertIn("PLANNED_AS_DONE", self.codes(out))

    def test_model_generated_anecdote_holds(self):
        self.add("m1", NOTE, "observed", "--origin", "ai_generated")
        code, out = self.check([self.claim(item="m1")])
        self.assertEqual(3, code)
        self.assertIn("EVIDENCE_MODEL_GENERATED", self.codes(out))

    def test_hypothetical_scenario_cannot_be_experience(self):
        self.add("h1", NOTE, "hypothetical")
        code, out = self.check([self.claim(item="h1")])
        self.assertIn("HYPOTHETICAL_AS_EXPERIENCE", self.codes(out))

    def test_edited_transcript_cannot_back_a_quote(self):
        self.add("t1", NOTE, "said_by_author", "--kind", "transcript")
        code, out = self.check([self.claim(item="t1", quote=True)])
        self.assertEqual(3, code)
        self.assertIn("QUOTE_NOT_VERBATIM", self.codes(out))
        self.add("t2", NOTE, "said_by_author", "--kind", "transcript", "--verbatim")
        code, out = self.check([self.claim(item="t2", quote=True)])
        self.assertEqual(0, code, out)

    def test_conflicting_dated_accounts_hold(self):
        self.add("a", NOTE, "observed", "--valid-at", "2026-03-02")
        self.add("b", NOTE.replace("2026-03-02", "2025-11-20"), "observed", "--valid-at", "2025-11-20")
        claim = self.claim()
        claim["evidence"] = [{"item": "a", "excerpt": "I glued the last tile"},
                             {"item": "b", "excerpt": "I glued the last tile"}]
        code, out = self.check([claim])
        self.assertIn("CONFLICTING_ACCOUNTS", self.codes(out))

    def test_claim_date_that_disagrees_with_the_note_holds(self):
        self.add("n1", NOTE, "observed", "--valid-at", "2026-03-02")
        code, out = self.check([self.claim(date="2024-06")])
        self.assertIn("DATE_CONFLICT", self.codes(out))
        code, out = self.check([self.claim(date="2026-03")])
        self.assertEqual(0, code, out)

    def test_excerpt_absent_from_the_note_holds(self):
        self.add("n1", NOTE)
        code, out = self.check([self.claim(excerpt="I painted the lighthouse")])
        self.assertIn("ANCHOR_NOT_FOUND", self.codes(out))

    def test_stale_bytes_hold(self):
        _, added = self.add("n1", NOTE)
        obj = Path(self.root) / "objects" / added["sha256"]
        obj.write_text(NOTE + " Added later.")
        code, out = self.check([self.claim()])
        self.assertIn("EVIDENCE_STALE", self.codes(out))

    def test_withdrawn_consent_deletes_the_bytes_and_stops_support(self):
        _, added = self.add("n1", NOTE)
        code, out = run("withdraw", "--root", self.root, "--id", "n1")
        self.assertEqual(0, code)
        self.assertFalse((Path(self.root) / "objects" / added["sha256"]).exists())
        code, out = self.check([self.claim()])
        self.assertEqual(3, code)
        self.assertIn("EVIDENCE_WITHDRAWN", self.codes(out))

    def test_redaction_removes_the_earlier_bytes(self):
        _, added = self.add("n1", NOTE)
        start = NOTE.index("The roof")
        code, out = run("redact", "--root", self.root, "--id", "n1", "--start", str(start),
                        "--end", str(len(NOTE)), "--reason", "private detail")
        self.assertEqual(0, code, out)
        self.assertFalse((Path(self.root) / "objects" / added["sha256"]).exists())
        kept = (Path(self.root) / "objects" / out["sha256"]).read_text()
        self.assertNotIn("roof", kept)
        code, out = self.check([self.claim(excerpt="The roof still warps")])
        self.assertIn("ANCHOR_NOT_FOUND", self.codes(out))
        code, out = self.check([self.claim()])
        self.assertEqual(0, code, out)

    def test_claims_from_another_project_cannot_use_this_vault(self):
        self.add("n1", NOTE)
        code, out = self.check([self.claim()], project="someone-elses-book")
        self.assertEqual(3, code)
        self.assertIn("VAULT_PROJECT_MISMATCH", self.codes(out))

    def test_ambiguous_excerpt_needs_an_offset(self):
        self.add("n1", NOTE + " " + NOTE)
        code, out = self.check([self.claim()])
        self.assertIn("ANCHOR_AMBIGUOUS", self.codes(out))
        code, out = self.check([dict(self.claim(), evidence=[{"item": "n1", "start": NOTE.index("I glued"),
                                                              "excerpt": "I glued the last tile"}])])
        self.assertEqual(0, code, out)


if __name__ == "__main__":
    unittest.main()
