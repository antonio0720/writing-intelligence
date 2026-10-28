"""plans/v9.manifest.yaml is the v9 status source; references/v9/WAVES.yaml repeats it.

Two copies of one fact drift silently. This fails the moment a wave's stage
differs between them, a wave exists in one and not the other, or the manifest
claims a shipped wave while v9 is unreleased.
"""
import importlib.util
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("check_manifest", str(REPO / "scripts" / "check-manifest.py"))
CM = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CM)
STAGE_TO_STATUS = {"PLANNED": "planned", "IN_PROGRESS": "in_progress",
                   "PROTOTYPE": "in_progress", "VALIDATED": "in_progress"}


def waves_yaml():
    out = {}
    for line in (REPO / "references" / "v9" / "WAVES.yaml").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^  (WI9-\d\d): \{.*status: ([A-Z_]+)", line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


class ManifestParity(unittest.TestCase):
    def setUp(self):
        self.top, waves = CM.load_manifest(REPO / "plans" / "v9.manifest.yaml")
        self.waves = {w["id"]: w for w in waves}

    def test_same_waves_same_stages(self):
        readable = waves_yaml()
        self.assertTrue(readable, "parsed no waves from WAVES.yaml; a parity check of nothing is not a pass")
        self.assertEqual(set(readable), set(self.waves))
        for wid, stage in readable.items():
            with self.subTest(wave=wid):
                self.assertEqual(stage, self.waves[wid].get("stage"))
                self.assertEqual(STAGE_TO_STATUS[stage], self.waves[wid].get("status"))

    def test_nothing_ships_before_release(self):
        self.assertEqual("8.0.0", self.top.get("core_version"))
        self.assertEqual("9.0.0", self.top.get("version_target"))
        self.assertFalse([w for w in self.waves.values() if w.get("status") == "shipped"])

    def test_parity_detects_a_drifted_stage(self):
        readable = waves_yaml()
        readable["WI9-00"] = "PLANNED"
        self.assertNotEqual(readable["WI9-00"], self.waves["WI9-00"].get("stage"))


if __name__ == "__main__":
    unittest.main()
