"""The v9 dossier schema and the checker must name the same vocabularies.

A schema that drifts from the code validates dossiers the checker refuses, or
refuses ones it accepts. Every enum is compared in both directions.
"""
import importlib.util
import json
from pathlib import Path
import unittest

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("wi_authorship", str(REPO / "scripts" / "wi-authorship.py"))
WA = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(WA)
SCHEMA = json.loads((REPO / "schemas" / "v9" / "authorship-dossier.schema.json").read_text(encoding="utf-8"))


def enum(path):
    node = SCHEMA
    for key in path:
        node = node[key]
    return set(node["enum"])


class SchemaParity(unittest.TestCase):
    def test_vocabularies_match(self):
        props = ("properties",)
        pairs = {
            "schema": (props + ("schema",), WA.SCHEMAS),
            "origin": (("$defs", "origin"), WA.ORIGINS),
            "venue_policy": (props + ("document", "properties", "venue_policy"), WA.VENUES),
            "intended_use": (props + ("document", "properties", "intended_use"), WA.INTENDED),
            "contribution kind": (("$defs", "contributionKind"), WA.CONTRIBUTION_KINDS),
            "evidence kind": (props + ("evidence", "items", "properties", "kind"), WA.KINDS),
            "experience_state": (props + ("evidence", "items", "properties", "experience_state"),
                                 WA.EXPERIENCE_STATES),
            "support_status": (props + ("evidence", "items", "properties", "support_status"),
                               WA.SUPPORT_STATES),
            "decision outcome": (props + ("review_decision", "properties", "outcome"),
                                 WA.DECISION_OUTCOMES),
        }
        for name, (path, code) in pairs.items():
            with self.subTest(vocabulary=name):
                self.assertEqual(enum(path), set(code))

    def test_parity_check_can_fail(self):
        # Negative control: a vocabulary with one extra member is detected.
        self.assertNotEqual(enum(("$defs", "origin")), set(WA.ORIGINS) | {"unknown"})


if __name__ == "__main__":
    unittest.main()
