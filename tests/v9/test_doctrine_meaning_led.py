"""P0-12 / WI9-05A: the craft doctrine edits for meaning, never for a detector.

v7's scan (tests/v7/test_wi7.sh) refuses a short list of evasion phrases. It
did not cover the v8 craft library, which still prescribed sentence-length
quotas, synonym swaps and an operator described as targeting detector
statistics. This test scans the doctrine a model actually reads and refuses
that vocabulary returning. Every positive has a planted twin that must fail.
"""
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]

FORBIDDEN = (
    "inject_variance",
    "variance injection",
    "variance_injection",
    "anti-detector",
    "anti-detection",
    "detectors would flag",
    "ai detection risk",
    "detection risk:",
    "should look random",
    "statistical signal for ai",
    "signature that ai detectors",
    "human-classified",
    "ai-flagged",
    "countermeasure",
    "scores as human-written",
    "likely human-written",
    "human probability",
    "ai-probability",
    "passes ai detection",
    "undetectable",
    "human-sounding",
)

SCAN_FILES = ("SKILL.md", "README.md", "USER_GUIDE.md", "CHEATSHEET.md")
SCAN_DIRS = (
    "packs", "agents",
    "references/anti_patterns", "references/diagnostics", "references/compiler",
    "references/academic", "references/genre_packs", "references/positive_patterns",
    "references/voiceprints",
)


def doctrine_files(repo=REPO):
    files = [repo / name for name in SCAN_FILES if (repo / name).is_file()]
    for directory in SCAN_DIRS:
        root = repo / directory
        if root.is_dir():
            files.extend(sorted(p for p in root.rglob("*") if p.suffix in (".md", ".yaml", ".yml")))
    files.extend(sorted((repo / "tests").glob("*.md")))
    return files


def scan(files):
    hits = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace").lower()
        for phrase in FORBIDDEN:
            if phrase in text:
                hits.append("%s: %s" % (path, phrase))
    return hits


class DoctrineIsMeaningLed(unittest.TestCase):
    def test_scan_reads_the_doctrine(self):
        files = doctrine_files()
        # A scan of nothing is not a pass.
        self.assertGreater(len(files), 100, "scanned only %d files" % len(files))
        self.assertIn(REPO / "SKILL.md", files)
        self.assertIn(REPO / "references/anti_patterns/cadence.md", files)

    def test_no_detector_oriented_instruction_remains(self):
        hits = scan(doctrine_files())
        self.assertEqual([], hits, "detector-oriented doctrine returned:\n" + "\n".join(hits))

    def test_planted_instruction_is_caught(self):
        with tempfile.TemporaryDirectory() as folder:
            planted = Path(folder) / "planted.md"
            planted.write_text("## Polish\nRun inject_variance so the draft reads human-classified.\n",
                               encoding="utf-8")
            self.assertEqual(2, len(scan([planted])))

    def test_retired_operator_has_its_replacement(self):
        ops = (REPO / "references/diagnostics/rewrite_operators.md").read_text(encoding="utf-8")
        self.assertIn("## repair_rhythm", ops)
        self.assertIn("never to meet a count", ops)

    def test_legacy_log_name_still_validates_and_new_name_exists(self):
        import json
        schema = json.loads((REPO / "schemas/prose_rewrite_log.schema.json").read_text(encoding="utf-8"))
        ops = schema["properties"]["transformations"]["items"]["properties"]["op"]["enum"]
        self.assertIn("rhythm_repaired", ops)
        self.assertIn("variance_injected", ops)  # old logs must still validate


if __name__ == "__main__":
    unittest.main()
