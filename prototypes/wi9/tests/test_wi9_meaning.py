"""WI9-04: no silent change to what the writer meant.

Each fixture is a synthetic original and a revision that reads well and says
something else. The exit condition is zero silent protected-meaning changes:
every fixture must surface its delta, and the unchanged twin must surface none.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import wi9_ledger  # noqa: E402
import wi9_vault  # noqa: E402
from wi9_meaning import compare, inventory, review  # noqa: E402
from test_wi9_ledger import ACTOR, make_store  # noqa: E402

FIXTURES = [
    ("NUMBER_CHANGED", "It took eleven evenings to finish.", "It took twelve evenings to finish."),
    ("DATE_CHANGED", "Sales rose in 2023.", "Sales rose in 2021."),
    ("PLANNED_TO_COMPLETED", "We will build the harbour model next spring.", "We built the harbour model."),
    ("ESTIMATE_TO_MEASURED", "The run took about forty minutes.", "The run took forty minutes."),
    ("MEASURED_TO_ESTIMATE", "We measured exactly 312 visitors.", "We measured roughly 312 visitors."),
    ("NEGATION_FLIPPED", "The test did not pass on the second machine.", "The test passed on the second machine."),
    ("STANCE_REVERSED", "Remote work is a good idea for small teams.", "Remote work is a bad idea for small teams."),
    ("CAUSE_CHANGED", "The roof warps because the room is damp.", "The roof warps because the glue is cheap."),
    ("CAUSE_ADDED", "The launch slipped a week.", "The launch slipped a week because the vendor was late."),
    ("CAUSE_REMOVED", "The launch slipped because the vendor was late.", "The launch slipped this week."),
    ("UNCERTAINTY_REMOVED", "I think the price is too high for students.", "The price is too high for students."),
    ("CONCESSION_DROPPED", "Although the venue was small, I recommend it.", "I recommend the venue."),
    ("CHRONOLOGY_REVERSED", "We moved before the flood reached the street.",
     "We moved after the flood reached the street."),
    ("QUOTE_ALTERED", "The mayor said the budget was tight.", 'The mayor said "the budget is a disaster."'),
    ("OUTCOME_ADDED", "We changed the checkout page.", "We changed the checkout page, which doubled sales."),
    ("CLAIM_DROPPED", "The roof warps when it rains. Repairs cost 40 dollars a year.", "The roof warps when it rains."),
    ("NEW_AUTOBIOGRAPHICAL_FACT", "The roof warps when it rains.",
     "The roof warps when it rains. I rebuilt it by hand in a single weekend."),
    ("NEW_UNSOURCED_CLAIM", "The roof warps when it rains.",
     "The roof warps when it rains. Roughly 30 percent of models fail this way."),
]


class Deltas(unittest.TestCase):
    def test_every_protected_change_surfaces(self):
        for kind, original, candidate in FIXTURES:
            with self.subTest(kind=kind):
                kinds = [d["kind"] for d in compare(original, candidate)["deltas"]]
                self.assertIn(kind, kinds, (original, candidate, kinds))

    def test_unchanged_twin_has_no_deltas(self):
        for kind, original, _ in FIXTURES:
            with self.subTest(kind=kind):
                report = compare(original, original)
                self.assertEqual([], report["deltas"])
                self.assertEqual("REVIEW", report["status"])

    def test_wording_change_that_keeps_meaning_is_quiet(self):
        report = compare("It took about eleven evenings, I think, because the glue was slow to set.",
                         "I think it took about eleven evenings, because the glue was slow to set.")
        self.assertEqual([], report["deltas"])

    def test_split_sentence_does_not_invent_a_new_claim(self):
        report = compare("The roof warps when the room is damp and the glue lifts.",
                         "The roof warps when the room is damp. The glue lifts.")
        self.assertNotIn("NEW_UNSOURCED_CLAIM", [d["kind"] for d in report["deltas"]])

    def test_report_never_authorizes_release(self):
        self.assertFalse(compare("a.", "b.")["release_authorized"])

    def test_inventory_offsets_are_exact(self):
        text = 'She said "we are late." Then 3.5 hours passed.'
        for p in inventory(text):
            self.assertEqual(p["text"], text[p["start"]:p["end"]])

    def test_quantity_change_needs_the_quantity_capability(self):
        delta = compare("It took eleven evenings.", "It took twelve evenings.")["deltas"][0]
        self.assertEqual("claim.accept.quantity_change", delta["required_capability"])


class Review(unittest.TestCase):
    ORIGINAL = "It took about eleven evenings. The roof warps when it rains."
    CANDIDATE = "It took eleven evenings. The roof warps when it rains. I rebuilt it by hand in a single weekend."

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name)
        self.store = self.base / "authority"
        self.ledger = str(self.base / "ledger")
        self.report = compare(self.ORIGINAL, self.CANDIDATE)
        self.by_kind = {d["kind"]: d for d in self.report["deltas"]}

    def decide(self, kind, decision="accept", capability="claim.accept"):
        return wi9_ledger.record(self.ledger, str(self.store), ACTOR, "meaning", self.report["pair_sha256"],
                                 self.by_kind[kind]["id"], decision, "I checked this against my own notes.",
                                 capability=capability)

    def codes(self, out):
        return {i["code"] for i in out["issues"]}

    def test_undecided_deltas_hold(self):
        make_store(self.store)
        Path(self.ledger).mkdir(mode=0o700)
        out = review(self.ORIGINAL, self.CANDIDATE, self.ledger, str(self.store))
        self.assertEqual("HOLD", out["status"])
        self.assertIn("DELTA_UNDECIDED", self.codes(out))

    def test_every_delta_accepted_and_sourced_reaches_review(self):
        make_store(self.store, capability="claim.accept")
        self.decide("ESTIMATE_TO_MEASURED", capability="claim.accept.quantity_change")
        self.decide("NEW_AUTOBIOGRAPHICAL_FACT")
        vault = str(self.base / "vault")
        wi9_vault.main(["init", "--root", vault, "--project", "p"])
        note = self.base / "note.txt"
        note.write_text("Saturday and Sunday: I rebuilt the roof by hand.")
        wi9_vault.main(["add", "--root", vault, "--file", str(note), "--id", "n", "--label", "observed",
                        "--consent"])
        claims = self.base / "claims.json"
        claims.write_text(json.dumps({"schema": "wi9.vault-claims/1", "project": "p", "claims": [
            {"id": "c", "text": "I rebuilt it by hand in a single weekend.",
             "evidence": [{"item": "n", "excerpt": "I rebuilt the roof by hand"}]}]}))
        out = review(self.ORIGINAL, self.CANDIDATE, self.ledger, str(self.store), vault, str(claims))
        self.assertEqual("REVIEW", out["status"], out["issues"])
        self.assertFalse(out["release_authorized"])

    def test_accepted_new_first_person_fact_without_a_source_holds(self):
        make_store(self.store, capability="claim.accept")
        self.decide("ESTIMATE_TO_MEASURED", capability="claim.accept.quantity_change")
        self.decide("NEW_AUTOBIOGRAPHICAL_FACT")
        out = review(self.ORIGINAL, self.CANDIDATE, self.ledger, str(self.store))
        self.assertIn("DELTA_NEEDS_SOURCE", self.codes(out))

    def test_rejected_delta_holds(self):
        make_store(self.store, capability="claim.accept")
        self.decide("ESTIMATE_TO_MEASURED", "reject", capability="claim.accept.quantity_change")
        self.assertIn("DELTA_REJECTED", self.codes(review(self.ORIGINAL, self.CANDIDATE, self.ledger,
                                                          str(self.store))))

    def test_quantity_change_under_a_weaker_grant_holds(self):
        make_store(self.store, capability="claim.accept.wording_only")
        self.decide("ESTIMATE_TO_MEASURED", capability="claim.accept.wording_only")
        out = review(self.ORIGINAL, self.CANDIDATE, self.ledger, str(self.store))
        self.assertIn("DELTA_CAPABILITY_INSUFFICIENT", self.codes(out))

    def test_decision_for_a_different_candidate_does_not_carry_over(self):
        make_store(self.store, capability="claim.accept")
        self.decide("NEW_AUTOBIOGRAPHICAL_FACT")
        changed = self.CANDIDATE.replace("single weekend", "single night")
        out = review(self.ORIGINAL, changed, self.ledger, str(self.store))
        self.assertIn("DELTA_UNDECIDED", self.codes(out))


if __name__ == "__main__":
    unittest.main()
