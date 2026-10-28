"""Every writer builds and reviews their own voice baseline, in their own folder.

No corpus ships with v9. These tests use synthetic text written for the test,
never anybody's real writing, and prove the review is bound to the exact samples.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wi9_core import main, sha256, voice_baseline, voice_review

WHEN = "2026-10-28T12:00:00+00:00"


def sample_set(root, n=3, genre="essay"):
    samples = []
    for i in range(n):
        text = " ".join(["Sample %d sentence %d is synthetic test text." % (i, j) for j in range(80)])
        (root / ("s%d.txt" % i)).write_text(text, encoding="utf-8")
        samples.append({"id": "s%d" % i, "path": "s%d.txt" % i, "genre": genre,
                        "origin": "human_authored", "consent": True,
                        "sha256": sha256((root / ("s%d.txt" % i)).read_bytes())})
    return samples


class VoiceReview(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def reviews(self):
        return sorted(p.name for p in self.root.glob("voice-review-*.json"))

    def test_approval_is_written_into_the_writers_own_folder(self):
        samples = sample_set(self.root)
        r = voice_review(samples, self.root, "approve", WHEN, "sentence length is me")
        self.assertEqual("REVIEW", r["status"])
        self.assertEqual([r["written"]], self.reviews())
        record = json.loads((self.root / r["written"]).read_text())
        self.assertEqual(voice_baseline(samples, self.root)["baseline_digest"], record["baseline_digest"])
        self.assertIn("Not proof of authorship", record["scope"])
        self.assertEqual(0o600, os.stat(self.root / r["written"]).st_mode & 0o777)

    def test_rejection_is_recorded_and_is_not_an_approval(self):
        r = voice_review(sample_set(self.root), self.root, "reject", WHEN, "not how I write")
        self.assertEqual("HOLD", r["status"])
        self.assertEqual("reject", json.loads((self.root / r["written"]).read_text())["decision"])

    def test_a_baseline_that_does_not_qualify_cannot_be_approved(self):
        r = voice_review(sample_set(self.root, n=2), self.root, "approve", WHEN)
        self.assertIn("VOICE_BASELINE_NOT_READY", {x["code"] for x in r["issues"]})
        self.assertEqual([], self.reviews())

    def test_a_review_is_never_overwritten(self):
        samples = sample_set(self.root)
        voice_review(samples, self.root, "approve", WHEN)
        again = voice_review(samples, self.root, "reject", WHEN)
        self.assertIn("VOICE_ALREADY_REVIEWED", {x["code"] for x in again["issues"]})
        self.assertEqual(1, len(self.reviews()))

    def test_changing_a_sample_changes_the_baseline_it_binds_to(self):
        samples = sample_set(self.root)
        first = voice_review(samples, self.root, "approve", WHEN)["record"]["baseline_digest"]
        (self.root / "s0.txt").write_text((self.root / "s0.txt").read_text() + " One more.", encoding="utf-8")
        samples[0]["sha256"] = sha256((self.root / "s0.txt").read_bytes())
        second = voice_review(samples, self.root, "approve", WHEN)["record"]["baseline_digest"]
        self.assertNotEqual(first, second)

    def test_a_symlinked_review_name_is_not_followed(self):
        samples = sample_set(self.root)
        digest = voice_baseline(samples, self.root)["baseline_digest"]
        outside = tempfile.NamedTemporaryFile(delete=False)
        self.addCleanup(os.unlink, outside.name)
        os.symlink(outside.name, self.root / ("voice-review-%s.json" % digest[:12]))
        r = voice_review(samples, self.root, "approve", WHEN)
        self.assertIn("VOICE_ALREADY_REVIEWED", {x["code"] for x in r["issues"]})
        self.assertEqual(b"", Path(outside.name).read_bytes())

    def test_unknown_decision_holds(self):
        r = voice_review(sample_set(self.root), self.root, "maybe", WHEN)
        self.assertIn("VOICE_DECISION_INVALID", {x["code"] for x in r["issues"]})

    def test_command_line_round_trip(self):
        (self.root / "voice.json").write_text(json.dumps({"samples": sample_set(self.root)}))
        self.assertEqual(0, main(["voice", "--root", str(self.root), "--input", "voice.json"]))
        self.assertEqual(0, main(["voice-review", "--root", str(self.root), "--input", "voice.json",
                                  "--decision", "approve", "--note", "fits"]))
        self.assertEqual(1, len(self.reviews()))


if __name__ == "__main__":
    unittest.main()
