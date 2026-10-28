"""Bring-your-own-model: the gates run first, the best result is a draft, and no key leaks.

The "model" here is a small local program written by the test. It records that
it was called, so a refusal can prove the model was never reached.
"""
import json
import os
import stat
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wi9_provider import run_provider  # noqa: E402

KEY_VALUE = "test-key-value-not-a-real-secret-9f2c"

PROGRAM = textwrap.dedent("""\
    #!{python}
    import json, os, sys, time
    req = json.load(sys.stdin)
    open({marker!r}, "w").write(json.dumps({{"key_seen": os.environ.get("MY_MODEL_KEY"),
                                           "env": sorted(os.environ)}}))
    mode = {mode!r}
    if mode == "sleep":
        time.sleep(5)
    if mode == "fail":
        sys.exit(4)
    if mode == "huge":
        sys.stdout.write("x" * 2100000); sys.exit(0)
    card = req["source_cards"][0]
    quote = card["source_quote"] if mode != "fabricate" else "a sentence the source never said"
    out = {{"schema": "wi9.candidate/1", "paragraphs": [{{
        "text": "The note says: " + quote + ".", "evidence_ids": [card["id"]],
        "author_review_required": True,
        "direct_quotes": [{{"source_id": card["id"], "exact_text": quote}}]}}]}}
    if mode == "claims":
        out["release_authorized"] = True
        out["human_authored"] = True
    json.dump(out, sys.stdout)
""")


def dossier(policy="ai_permitted"):
    return {"document": {"intended_use": "internal_review", "arena": "essay", "mission": "explain the model"},
            "venue": {"policy": policy, "disclosure_plan": "Drafted with a model I chose; edited by me."},
            "author_thesis": "Patience is a design tool.",
            "evidence": [{"id": "e1", "consent": True, "kind": "firsthand", "origin": "human_authored",
                          "claim": "The roof warps in damp weather.",
                          "exact_excerpt": "The roof still warps when the room is damp"}]}


class Provider(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        self.marker = self.dir / "called.json"
        self.env = {"PATH": os.environ.get("PATH", ""), "MY_MODEL_KEY": KEY_VALUE, "HOME": "/should/not/pass",
                    "AWS_SECRET_ACCESS_KEY": "also-should-not-pass"}

    def program(self, mode="ok"):
        path = self.dir / ("model-%s.py" % mode)
        path.write_text(PROGRAM.format(python=sys.executable, marker=str(self.marker), mode=mode))
        path.chmod(path.stat().st_mode | stat.S_IXUSR)
        return str(path)

    def run_it(self, mode="ok", policy="ai_permitted", **kw):
        args = dict(key_env="MY_MODEL_KEY", consent_to_send=True, environ=self.env)
        args.update(kw)
        return run_provider(dossier(policy), self.program(mode), **args)

    def codes(self, out):
        return {i["code"] for i in out["issues"]}

    def test_good_candidate_is_a_draft_and_never_release(self):
        out = self.run_it()
        self.assertEqual("DRAFT_REVIEW_REQUIRED", out["status"], out["issues"])
        self.assertFalse(out["release_authorized"])
        self.assertEqual("ai_generated", out["candidate_origin"])

    def test_human_only_venue_never_reaches_the_model(self):
        out = self.run_it(policy="human_only")
        self.assertEqual("HOLD", out["status"])
        self.assertIn("HUMAN_ONLY_NO_GENERATED_PROSE", self.codes(out))
        self.assertFalse(self.marker.exists())
        self.assertFalse(out["provider_called"])

    def test_unknown_policy_never_reaches_the_model(self):
        self.assertIn("VENUE_POLICY_UNKNOWN", self.codes(self.run_it(policy="Human-Only")))
        self.assertFalse(self.marker.exists())

    def test_missing_evidence_never_reaches_the_model(self):
        d = dossier()
        d["evidence"][0]["consent"] = False
        out = run_provider(d, self.program(), key_env="MY_MODEL_KEY", consent_to_send=True, environ=self.env)
        self.assertIn("EVIDENCE_INVALID", self.codes(out))
        self.assertFalse(self.marker.exists())

    def test_without_send_consent_nothing_leaves(self):
        out = self.run_it(consent_to_send=False)
        self.assertIn("SEND_CONSENT_REQUIRED", self.codes(out))
        self.assertFalse(self.marker.exists())

    def test_only_the_named_key_reaches_the_program_and_never_the_report(self):
        out = self.run_it()
        seen = json.loads(self.marker.read_text())
        self.assertEqual(KEY_VALUE, seen["key_seen"])
        self.assertNotIn("HOME", seen["env"])
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", seen["env"])
        self.assertNotIn(KEY_VALUE, json.dumps(out))

    def test_a_key_value_passed_as_the_name_is_refused(self):
        out = self.run_it(key_env=KEY_VALUE)
        self.assertIn("KEY_ENV_INVALID", self.codes(out))
        self.assertNotIn(KEY_VALUE, json.dumps(out))
        self.assertFalse(self.marker.exists())

    def test_fabricated_quotation_holds(self):
        self.assertIn("QUOTATION_UNVERIFIED:0", self.codes(self.run_it("fabricate")))

    def test_model_cannot_authorize_or_declare_authorship(self):
        out = self.run_it("claims")
        self.assertIn("PROVIDER_CLAIMED_AUTHORITY", self.codes(out))
        self.assertFalse(out["release_authorized"])
        self.assertEqual("ai_generated", out["candidate_origin"])

    def test_timeout_failure_and_oversize_hold(self):
        self.assertIn("PROVIDER_TIMEOUT", self.codes(self.run_it("sleep", timeout=1)))
        self.assertIn("PROVIDER_FAILED", self.codes(self.run_it("fail")))
        self.assertIn("PROVIDER_OUTPUT_TOO_LARGE", self.codes(self.run_it("huge")))

    def test_program_writes_land_in_a_scratch_folder_not_the_callers(self):
        before = set(Path.cwd().iterdir())
        self.run_it()
        self.assertEqual(before, set(Path.cwd().iterdir()))

    def test_relative_provider_path_is_refused(self):
        out = run_provider(dossier(), "model.py", consent_to_send=True, environ=self.env)
        self.assertIn("PROVIDER_PATH_RELATIVE", self.codes(out))


if __name__ == "__main__":
    unittest.main()
