"""WI9-05F: deeper voice measures, held-out stability and drift, all on the writer's own samples.

Synthetic writers only. Matching a baseline never proves authorship, and the
report says so.
"""
import json
import random
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wi9_core import main, profile_text, sha256, voice_baseline, voice_compare  # noqa: E402

NOUNS = ["harbour", "quay", "roof", "glue", "card", "boat", "lamp", "window", "street", "tile", "paint", "crane",
         "bridge", "market", "garden", "stair", "fence", "mill", "canal", "tower"]
VERBS = ["warps", "holds", "fails", "settles", "shifts", "cracks", "dries", "bends", "leans", "sets"]


def writer_a(seed, n=70):
    """Short first-person sentences that hedge and argue with themselves."""
    rng = random.Random(seed)
    out = []
    for i in range(n):
        a, b = rng.sample(NOUNS, 2)
        out.append(rng.choice([
            "I think the %s %s when the room is damp." % (a, rng.choice(VERBS)),
            "But the %s probably %s first." % (b, rng.choice(VERBS)),
            "I doubt the %s matters %d times out of ten." % (a, rng.randint(2, 9)),
            "Maybe I glued the %s too early." % a,
        ]))
    return " ".join(out)


def writer_b(seed, n=40):
    """Long impersonal sentences with no hedging and no first person."""
    rng = random.Random(seed)
    out = []
    for i in range(n):
        a, b, c = rng.sample(NOUNS, 3)
        out.append("The %s and the %s were assembled together across the long afternoon while the %s %s "
                   "steadily beside the open window of the workshop" % (a, b, c, rng.choice(VERBS)) + ".")
    return " ".join(out)


class Measures(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def samples(self, texts, genre="essay"):
        out = []
        for i, text in enumerate(texts):
            (self.root / ("s%d.txt" % i)).write_text(text, encoding="utf-8")
            out.append({"id": "s%d" % i, "path": "s%d.txt" % i, "genre": genre, "origin": "human_authored",
                        "consent": True, "sha256": sha256(text.encode("utf-8"))})
        return out

    def test_profile_carries_the_semantic_voice_measures(self):
        p = profile_text(writer_a(1))
        for key in ("qualifiers_per_1000", "intensifiers_per_1000", "disagreement_per_1000",
                    "concrete_detail_share", "example_share", "causal_share", "concession_share",
                    "question_share", "argument_strategy"):
            self.assertIn(key, p)
        self.assertGreater(p["qualifiers_per_1000"], 0)
        self.assertGreater(p["disagreement_per_1000"], 0)

    def test_baseline_reports_held_out_stability_for_every_measure(self):
        base = voice_baseline(self.samples([writer_a(s) for s in (1, 2, 3, 4)]), self.root)
        self.assertEqual("REVIEW", base["status"], base["issues"])
        self.assertIn("qualifiers_per_1000", base["held_out_stability"])
        self.assertTrue(base["held_out_stability"]["mean_sentence_words"]["stable"])
        self.assertEqual(4, base["held_out_stability"]["mean_sentence_words"]["samples"])

    def test_another_writers_sample_mixed_in_shows_as_unstable(self):
        base = voice_baseline(self.samples([writer_a(1), writer_a(2), writer_a(3), writer_b(4)]), self.root)
        self.assertFalse(base["held_out_stability"]["mean_sentence_words"]["stable"])
        self.assertFalse(base["held_out_stability"]["first_person_per_1000"]["stable"])

    def test_wrong_writers_text_drifts(self):
        samples = self.samples([writer_a(s) for s in (1, 2, 3)])
        out = voice_compare(samples, self.root, writer_b(9))
        moved = {d["measure"] for d in out["drift"]}
        self.assertIn("mean_sentence_words", moved)
        self.assertIn("first_person_per_1000", moved)

    def test_held_out_text_by_the_same_writer_stays_inside(self):
        samples = self.samples([writer_a(s) for s in (1, 2, 3)])
        out = voice_compare(samples, self.root, writer_a(42))
        self.assertEqual([], [d["measure"] for d in out["drift"] if d["measure"] in
                              ("mean_sentence_words", "first_person_per_1000", "qualifiers_per_1000")])

    def test_matching_the_baseline_is_not_proof_of_authorship(self):
        samples = self.samples([writer_a(s) for s in (1, 2, 3)])
        out = voice_compare(samples, self.root, writer_a(7))
        self.assertIn("does not show who wrote", out["note"])
        self.assertFalse(out["release_authorized"])

    def test_three_edits_of_one_passage_hold(self):
        one = writer_a(5, n=120)
        edits = [one, one.replace("damp", "wet", 4) + " Then I stopped.",
                 "Notes from Tuesday. " + one.replace("glued", "fixed", 3)]
        base = voice_baseline(self.samples(edits), self.root)
        self.assertIn("VOICE_SAMPLES_TOO_SIMILAR", {i["code"] for i in base["issues"]})

    def test_distinct_pieces_by_one_writer_are_not_too_similar(self):
        base = voice_baseline(self.samples([writer_a(s) for s in (11, 12, 13)]), self.root)
        self.assertNotIn("VOICE_SAMPLES_TOO_SIMILAR", {i["code"] for i in base["issues"]})

    def test_compare_refuses_a_baseline_that_does_not_qualify(self):
        out = voice_compare(self.samples([writer_a(1)]), self.root, writer_a(2))
        self.assertEqual("HOLD", out["status"])

    def test_cross_genre_samples_still_hold(self):
        samples = self.samples([writer_a(1), writer_a(2), writer_a(3)])
        samples[2]["genre"] = "speech"
        self.assertIn("VOICE_GENRE_MIX", {i["code"] for i in voice_baseline(samples, self.root)["issues"]})

    def test_cli_voice_compare(self):
        samples = self.samples([writer_a(s) for s in (1, 2, 3)])
        (self.root / "voice.json").write_text(json.dumps({"samples": samples}))
        draft = self.root.parent / ("draft-%s.txt" % self.root.name)
        draft.write_text(writer_b(3))
        self.addCleanup(draft.unlink)
        self.assertEqual(0, main(["voice-compare", "--root", str(self.root), "--input", "voice.json",
                                  "--text", str(draft)]))


if __name__ == "__main__":
    unittest.main()
