"""Long manuscripts are scanned in chunks with global offsets, never cut off at 500 findings."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wi9_hotphrases  # noqa: E402
from wi9_hotphrases import main, scan_document, scan_text  # noqa: E402

PARA = Path(__file__).resolve().parents[1].joinpath("examples", "sample_hotphrases.txt").read_text()


class Chunked(unittest.TestCase):
    def test_short_document_matches_the_single_scan(self):
        self.assertEqual(scan_text(PARA)["findings"], scan_document(PARA)["findings"])

    def test_long_document_keeps_every_finding_with_exact_global_offsets(self):
        single = scan_text(PARA)["finding_count"]
        big = (PARA + "\n\n") * 700
        self.assertTrue(scan_text(big)["truncated"])
        report = scan_document(big, chunk_chars=20_000)
        self.assertEqual(single * 700, report["finding_count"])
        self.assertTrue(report["complete"])
        self.assertGreater(len(report["chunks"]), 1)
        for f in report["findings"]:
            self.assertEqual(f["excerpt"], big[f["start"]:f["end"]])
        lines = big.split("\n")
        f = report["findings"][-1]
        self.assertEqual(f["excerpt"], lines[f["line"] - 1][f["column"] - 1:f["column"] - 1 + len(f["excerpt"])])

    def test_a_code_fence_is_never_split_across_chunks(self):
        fence = "```\n" + ("That matters.\n" * 400) + "```\n"
        text = ("Plain words here.\n\n" * 50) + fence + ("Plain words again.\n\n" * 50)
        report = scan_document(text, chunk_chars=2_500)
        for c in report["chunks"]:
            body = text[c["start"]:c["end"]]
            self.assertEqual(0, body.count("```") % 2, "a fence was split")
        self.assertEqual([], [f for f in report["findings"] if "That matters" in f["excerpt"]])

    def test_pathological_chunk_is_named_incomplete_not_hidden(self):
        old_hits, old_min = wi9_hotphrases.MAX_HITS, wi9_hotphrases.MIN_CHUNK_CHARS
        wi9_hotphrases.MAX_HITS, wi9_hotphrases.MIN_CHUNK_CHARS = 3, 200
        self.addCleanup(setattr, wi9_hotphrases, "MAX_HITS", old_hits)
        self.addCleanup(setattr, wi9_hotphrases, "MIN_CHUNK_CHARS", old_min)
        report = scan_document("That matters. " * 20, chunk_chars=1_000)
        self.assertFalse(report["complete"])
        self.assertTrue(report["truncated"])
        self.assertTrue(report["incomplete_ranges"])

    def test_cli_scans_a_long_file_in_chunks(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "long.txt"
            path.write_text((PARA + "\n\n") * 700)
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(0, main(["scan", "--input", str(path)]))
            report = json.loads(out.getvalue())
            self.assertIn("chunks", report)
            self.assertTrue(report["complete"])
            self.assertGreater(report["finding_count"], 500)


if __name__ == "__main__":
    unittest.main()
