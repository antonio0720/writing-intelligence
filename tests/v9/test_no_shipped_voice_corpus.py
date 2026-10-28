"""v9 ships no voice corpus, no firsthand vault and no review ledger. Each writer supplies their own samples, privately.

A voice baseline describes one person. If one were committed it would publish that
person's writing in a public repository and nudge every other user toward a voice
that is not theirs. This test fails if a voice manifest or review record is tracked,
or if a bundle payload would carry one.
"""
import re
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CORPUS = re.compile(r"(^|/)(voice\.json|voice-review-[0-9a-f]+\.json|vault\.json|ledger\.jsonl)$"
                    r"|(^|/)wi9-private(/|$)")


class NoShippedVoiceCorpus(unittest.TestCase):
    def tracked(self):
        out = subprocess.run(["git", "ls-files"], cwd=str(REPO), capture_output=True, text=True)
        if out.returncode != 0:
            self.skipTest("not a git checkout (an extracted bundle); the bundle check below still runs")
        return out.stdout.splitlines()

    def test_no_voice_manifest_or_review_is_tracked(self):
        found = [p for p in self.tracked() if CORPUS.search(p)]
        self.assertEqual([], found)

    def test_the_pattern_would_catch_one(self):
        for planted in ("voice.json", "a/voice.json", "notes/vault.json", "r/ledger.jsonl", "x/voice-review-50faca482d6a.json", "wi9-private/voice/essay/s.txt"):
            self.assertTrue(CORPUS.search(planted), planted)
        for fine in ("references/voiceprints/custom_voiceprint_builder.md", "schemas/voice_fingerprint.schema.json"):
            self.assertFalse(CORPUS.search(fine), fine)

    def test_no_file_on_disk_here_is_a_voice_corpus(self):
        found = [str(p.relative_to(REPO)) for p in REPO.rglob("*")
                 if p.is_file() and ".git" not in p.parts and CORPUS.search(str(p.relative_to(REPO)))]
        self.assertEqual([], found)


if __name__ == "__main__":
    unittest.main()
