"""Every skill's frontmatter stays inside the loader's hard limits.

A description over 1024 characters is not truncated — the bundle is rejected,
and every install instruction in the repository becomes false. The builder
checks this when bundles are built; this checks it on every commit, so the
trap is caught when the sentence is written, not at release.
"""
from pathlib import Path
import re
import unittest

REPO = Path(__file__).resolve().parents[2]
MAX_NAME, MAX_DESC = 64, 1024


def frontmatter(path):
    src = path.read_text(encoding="utf-8")
    if not src.startswith("---\n"):
        return None
    return src[4:src.find("\n---", 4)]


def field(fm, key):
    m = re.search(r"^%s:[ \t]+(.*)$" % key, fm, re.M)
    return m.group(1).strip().strip('"\'') if m else None


def problems(fm):
    out = []
    name, desc = field(fm, "name"), field(fm, "description")
    if name is None or desc is None:
        return ["missing name or description"]
    if len(name) > MAX_NAME or not re.match(r"^[a-z0-9][a-z0-9-]*$", name):
        out.append("name %r invalid" % name)
    if len(desc) > MAX_DESC:
        out.append("description is %d characters; the limit is %d" % (len(desc), MAX_DESC))
    if ": " in desc:
        out.append("description contains ': '")
    return out


class SkillFrontmatter(unittest.TestCase):
    def test_every_skill_is_inside_the_limits(self):
        skills = [p for p in [REPO / "SKILL.md"] + sorted((REPO / "packs").glob("*/SKILL.md"))
                  if p.is_file()]
        self.assertTrue(skills, "found no SKILL.md; a check of nothing is not a pass")
        for path in skills:
            with self.subTest(skill=str(path.relative_to(REPO))):
                fm = frontmatter(path)
                self.assertIsNotNone(fm, "no YAML frontmatter")
                self.assertEqual([], problems(fm))

    def test_the_check_refuses_an_oversized_description(self):
        self.assertTrue(problems("name: x\ndescription: " + "a" * (MAX_DESC + 1)))
        self.assertTrue(problems("name: x\ndescription: one: two"))
        self.assertEqual([], problems("name: x\ndescription: " + "a" * MAX_DESC))


if __name__ == "__main__":
    unittest.main()
