"""Review ledger: a decision counts only under the reviewer's own v6 grant.

Each refusal is asserted by its reason code beside a passing twin. The grant
store is a real v6 workspace made with `wi authority issue`.
"""
import contextlib
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import wi9_ledger  # noqa: E402
import wi9_phrase_review  # noqa: E402
from wi9_fs import StoreRefusal  # noqa: E402
from wi9_hotphrases import scan_text  # noqa: E402

WI = str(HERE.parents[1] / "scripts" / "wi.py")
ACTOR = "writer-a"
TEXT = "That matters because the payment was 32 days late."


def wi(*args):
    proc = subprocess.run([sys.executable, WI] + list(args), capture_output=True, text=True)
    if proc.returncode != 0:
        raise AssertionError(proc.stdout + proc.stderr)
    return proc.stdout


def make_store(path, subject=ACTOR, capability="claim.accept", kind="human",
               expires="2999-01-01T00:00:00+00:00"):
    if not (path / ".wi" / "workspace.db").exists():
        wi("init", str(path), "--title", "review authority")
    out = wi("authority", "issue", "--root", str(path), "--subject", subject, "--subject-kind", kind,
             "--capability", capability, "--scope", "workspace", "--issuer", "owner",
             "--activates", "2026-01-01T00:00:00+00:00", "--expires", expires)
    return out.split()[1]


class LedgerBase(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.store = self.base / "authority"
        self.ledger = str(self.base / "ledger")
        self.target = hashlib.sha256(TEXT.encode("utf-8")).hexdigest()

    def record(self, decision="accept", item="d1", kind="meaning", actor=ACTOR, **kw):
        return wi9_ledger.record(self.ledger, str(self.store), actor, kind, self.target, item, decision,
                                 "The number matches the invoice I kept.", **kw)

    def refused(self, code, fn, *args, **kw):
        with self.assertRaises(StoreRefusal) as ctx:
            fn(*args, **kw)
        self.assertEqual(code, ctx.exception.code)


class Grants(LedgerBase):
    def test_granted_person_records_a_decision(self):
        grant = make_store(self.store)
        entry = self.record()
        self.assertEqual(grant, entry["grant"]["grant_id"])
        self.assertEqual("human", entry["grant"]["subject_kind"])

    def test_typed_name_with_no_grant_is_refused(self):
        make_store(self.store, subject="someone-else")
        self.refused("AUTHORITY_DENIED", self.record)

    def test_a_service_cannot_review(self):
        make_store(self.store, kind="service")
        self.refused("AUTHORITY_NOT_HUMAN", self.record)

    def test_wording_grant_does_not_cover_a_meaning_decision(self):
        make_store(self.store, capability="claim.accept.wording_only")
        self.refused("AUTHORITY_DENIED", self.record)

    def test_store_planted_inside_the_ledger_folder_is_untrusted(self):
        Path(self.ledger).mkdir(mode=0o700)
        self.store = Path(self.ledger) / "authority"
        make_store(self.store)
        self.refused("AUTHORITY_STORE_UNTRUSTED", self.record)

    def test_expired_grant_is_refused(self):
        make_store(self.store, expires="2026-02-01T00:00:00+00:00")
        self.refused("AUTHORITY_EXPIRED", self.record)


class AppendOnly(LedgerBase):
    def setUp(self):
        LedgerBase.setUp(self)
        self.grant = make_store(self.store)

    def test_second_decision_needs_explicit_supersession(self):
        first = self.record("accept")
        self.refused("LEDGER_DECISION_EXISTS", self.record, "reject")
        second = self.record("reject", supersedes=first["hash"])
        self.refused("LEDGER_ALREADY_SUPERSEDED", self.record, "accept", supersedes=first["hash"])
        result = wi9_ledger.verify(self.ledger, str(self.store), self.target, "meaning")
        self.assertEqual(2, result["entries"])
        self.assertEqual(second["hash"], result["effective"][("meaning", self.target, "d1")]["hash"])

    def test_edited_ledger_is_refused_and_nothing_more_appends(self):
        self.record()
        path = Path(self.ledger) / "ledger.jsonl"
        entry = json.loads(path.read_text())
        entry["decision"] = "reject"
        path.write_text(json.dumps(entry, sort_keys=True) + "\n")
        self.assertEqual("HOLD", wi9_ledger.verify(self.ledger, str(self.store))["status"])
        self.refused("LEDGER_CHAIN_BROKEN", self.record, item="d2")

    def test_grant_that_has_since_expired_stops_an_entry_counting(self):
        self.record()
        later = wi9_ledger.verify(self.ledger, str(self.store), self.target, "meaning",
                                  now="2999-06-01T00:00:00+00:00")
        self.assertEqual({}, later["effective"])
        self.assertIn("LEDGER_GRANT_AUTHORITY_EXPIRED", {i["code"] for i in later["issues"]})

    def test_revoked_grant_stops_an_entry_counting_without_deleting_it(self):
        self.record()
        wi("authority", "revoke", "--root", str(self.store), "--grant", self.grant)
        result = wi9_ledger.verify(self.ledger, str(self.store), self.target, "meaning")
        self.assertEqual("HOLD", result["status"])
        self.assertEqual({}, result["effective"])
        self.assertEqual(1, result["entries"])
        self.assertIn("LEDGER_GRANT_AUTHORITY_REVOKED", {i["code"] for i in result["issues"]})


class PhraseReview(LedgerBase):
    def setUp(self):
        LedgerBase.setUp(self)
        make_store(self.store, capability="claim.accept.wording_only")
        self.report = scan_text(TEXT)
        self.finding = self.report["findings"][0]
        self.base_files()

    def base_files(self):
        (self.base / "doc.txt").write_text(TEXT, encoding="utf-8")
        (self.base / "report.json").write_text(json.dumps(self.report))

    def run_review(self, *extra):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = wi9_phrase_review.main(["--input", str(self.base / "doc.txt"),
                                           "--report", str(self.base / "report.json")] + list(extra))
        return code, json.loads(out.getvalue())

    def test_grant_bound_decision_reaches_review(self):
        f = self.finding
        wi9_ledger.record(self.ledger, str(self.store), ACTOR, "phrase", self.target,
                          wi9_ledger.phrase_item(f["id"], f["start"], f["end"]), "retain_as_written",
                          "The late payment in the same sentence is the specific.")
        code, out = self.run_review("--ledger", self.ledger, "--authority-store", str(self.store))
        self.assertEqual(0, code, out)
        self.assertEqual("v6_grant", out["reviewer_basis"])
        self.assertFalse(out["release_authorized"])

    def test_typed_reviewer_name_holds_unbound(self):
        f = self.finding
        typed = {"schema": "wi9.editorial.review/1", "document_sha256": self.target,
                 "rules_sha256": self.report["rules_sha256"],
                 "decisions": [{"rule_id": f["id"], "start": f["start"], "end": f["end"], "excerpt": f["excerpt"],
                                "status": "retain_as_written", "rationale": "Specific detail in the sentence.",
                                "reviewer": "Any Name", "reviewed_at": "2026-10-27T12:00:00-05:00"}]}
        (self.base / "typed.json").write_text(json.dumps(typed))
        code, out = self.run_review("--decisions", str(self.base / "typed.json"))
        self.assertEqual(3, code)
        self.assertIn("REVIEWER_UNBOUND:0", out["issues"])
        self.assertEqual("declared", out["reviewer_basis"])

    def test_ledger_without_a_decision_leaves_the_finding_unreviewed(self):
        Path(self.ledger).mkdir(mode=0o700)
        code, out = self.run_review("--ledger", self.ledger, "--authority-store", str(self.store))
        self.assertEqual(3, code)
        self.assertIn("FINDINGS_UNREVIEWED:1", out["issues"])


if __name__ == "__main__":
    unittest.main()
