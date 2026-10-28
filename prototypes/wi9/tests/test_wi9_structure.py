"""WI9-05C: shape findings are questions with exact spans, and real contrasts are left alone."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wi9_structure import analyze  # noqa: E402

TEMPLATE = "\n\n".join([
    "First, community matters. People gather to share stories. This shows the power of connection.",
    "Second, design matters. Small details shape how people feel. This shows the power of craft.",
    "Moreover, scale matters. Tiny worlds invite close attention. This shows the power of focus.",
    "Finally, play matters. Building is a form of thinking. This shows the power of curiosity.",
])
VARIED = "\n\n".join([
    "The harbour model took eleven evenings.",
    "I started with the quay, because the water line sets every other height. The first attempt sat 2 mm "
    "too low and the boats looked sunk. I cut it out.",
    "Paint came last.",
    "When the room is damp the roof still warps, and I have not found a glue that stops it. Next I will "
    "try a thinner card. If that fails I will live with the warp.",
])


def codes(text):
    return [f["code"] for f in analyze(text)["findings"]]


class Structure(unittest.TestCase):
    def test_template_essay_is_flagged(self):
        found = codes(TEMPLATE)
        self.assertIn("TEMPLATE_PARAGRAPHS", found)

    def test_varied_paragraphs_are_not_flagged(self):
        self.assertNotIn("TEMPLATE_PARAGRAPHS", codes(VARIED))

    def test_repeated_openings_are_flagged_with_their_count(self):
        text = "This shows care. This shows patience. This shows skill. The model is done."
        report = analyze(text)
        hits = [f for f in report["findings"] if f["code"] == "REPEATED_OPENING"]
        self.assertEqual(3, len(hits))
        self.assertEqual("this shows", hits[0]["opening"])
        for f in hits:
            self.assertEqual(f["excerpt"], text[f["start"]:f["end"]])

    def test_two_shared_openings_are_not_a_pattern(self):
        self.assertNotIn("REPEATED_OPENING", codes("This works. This fails. The model is done."))

    def test_hollow_contrast_is_flagged(self):
        self.assertIn("HOLLOW_CONTRAST", codes("It's not about the product, it's about the journey."))
        self.assertIn("HOLLOW_CONTRAST", codes("Leadership is less about control and more about trust."))

    def test_necessary_contrast_with_a_concrete_difference_is_left_alone(self):
        for text in ("The delay was not 3 days, but 3 weeks.",
                     "It's not the 2019 contract, it's the 2021 amendment that sets the rate.",
                     "The fault was not in Port Hadley, but in Marsh Creek."):
            self.assertNotIn("HOLLOW_CONTRAST", codes(text), text)

    def test_three_triads_are_flagged_one_is_not(self):
        one = "We packed bread, cheese, and apples."
        self.assertNotIn("TRIAD_RHYTHM", codes(one))
        many = ("It is fast, cheap, and simple. Teams feel calm, focused, and aligned. "
                "Leaders gain clarity, speed, and trust.")
        self.assertEqual(3, codes(many).count("TRIAD_RHYTHM"))

    def test_restatement_is_flagged(self):
        text = ("Small models reward patient builders who measure twice. "
                "Patient builders who measure twice are rewarded by small models.")
        self.assertIn("RESTATEMENT", codes(text))

    def test_report_is_editorial_only(self):
        report = analyze(TEMPLATE)
        self.assertFalse(report["release_authorized"])
        self.assertIn("Not authorship classification", report["scope"])

    def test_oversized_input_refused(self):
        with self.assertRaises(ValueError):
            analyze("a" * 500_001)


if __name__ == "__main__":
    unittest.main()
