"""`wi authorship` runs the one v9 implementation and passes its verdict through.

A wrapper that swallowed exit 3 would turn a HOLD into a success for every
script that trusts `wi`. A wrapper that crashed where the tools are absent
(the runtime bundle carries wi.py but not the v9 tools) would read as a bug.
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WI = REPO / "scripts" / "wi.py"


def run(*args, wi=WI):
    return subprocess.run([sys.executable, str(wi)] + list(args), capture_output=True, text=True)


class WiAuthorship(unittest.TestCase):
    def test_listed_in_help(self):
        self.assertIn("authorship", run("--help").stdout)

    def test_hold_passes_through_as_exit_3(self):
        proc = run("authorship", "audit", "--input", str(REPO / "examples/v9/venue-hold/dossier.json"))
        self.assertEqual(3, proc.returncode)
        self.assertIn("HUMAN_ONLY_CONFLICT", proc.stdout)

    def test_review_passes_through_as_exit_0(self):
        proc = run("authorship", "audit", "--input", str(REPO / "examples/v9/claim-coverage/dossier-cut.json"))
        self.assertEqual(0, proc.returncode, proc.stdout[-400:])
        self.assertIn('"status": "REVIEW"', proc.stdout)

    def test_release_without_an_operator_store_holds(self):
        proc = run("authorship", "release", "--input", str(REPO / "examples/v9/claim-coverage/dossier-cut.json"))
        self.assertEqual(3, proc.returncode)
        self.assertIn("AUTHORITY", proc.stdout)

    def test_scan_runs_the_phrase_rules(self):
        proc = run("authorship", "scan", "--input", str(REPO / "prototypes/wi9/examples/sample_hotphrases.txt"),
                   "--format", "text")
        self.assertEqual(0, proc.returncode)
        self.assertIn("334 rules", proc.stdout)

    def test_absent_tools_are_named_not_crashed(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "scripts").mkdir()
            alone = Path(d) / "scripts" / "wi.py"
            shutil.copy(str(WI), str(alone))
            proc = run("authorship", "audit", "--input", "x.json", wi=alone)
            self.assertEqual(2, proc.returncode)
            self.assertNotIn("Traceback", proc.stderr)
            self.assertIn("writing-intelligence-authorship", proc.stderr)


if __name__ == "__main__":
    unittest.main()
