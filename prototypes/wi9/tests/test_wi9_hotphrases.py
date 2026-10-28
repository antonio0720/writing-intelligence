"""Meaning-led phrase auditing, with explicit false-positive controls."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wi9_hotphrases import read_rules, scan_text, excluded_intervals


def hits(text, **kwargs):
    return scan_text(text, **kwargs)['findings']


class HotPhrasesTests(unittest.TestCase):
    def test_all_rules_have_unique_identifiers_and_valid_patterns(self):
        r = read_rules()
        self.assertEqual(334, len(r))
        self.assertEqual(len({x['id'] for x in r}), len(r))
        self.assertTrue(all(x['_compiled'] for x in r))

    def test_that_matters_exact(self):
        self.assertTrue(any(x['excerpt'].lower() == 'that matters' for x in hits('That matters.')))

    def test_that_matters_not_substring(self):
        self.assertFalse(any(x['excerpt'].lower() == 'that matters' for x in hits('Whatever matters to her is different.')))

    def test_that_matters_case_independent(self):
        self.assertTrue(any(x['excerpt'] == 'THAT MATTERS' for x in hits('THAT MATTERS to the buyer.')))

    def test_thats_where_interesting(self):
        self.assertTrue(any("that's where things get interesting" == x['excerpt'].lower()
                            for x in hits("That's where things get interesting.")))

    def test_curly_apostrophes_preserve_positions(self):
        s = "Something happened. Here’s the thing: the sale failed."
        match = [x for x in hits(s) if x['excerpt'] == 'Here’s the thing'][0]
        self.assertEqual(s[match['start']:match['end']], match['excerpt'])

    def test_quote_excluded_by_default(self):
        self.assertFalse(hits('The author said “that matters” yesterday.'))

    def test_quote_included_explicitly(self):
        self.assertTrue(any(x['excerpt'].lower() == 'that matters' for x in hits('She said “that matters”.',include_quoted=True)))

    def test_markdown_blockquote_excluded(self):
        self.assertFalse(hits('> That matters.'))

    def test_markdown_blockquote_included(self):
        self.assertTrue(hits('> That matters.',include_quoted=True))

    def test_code_fence_excluded(self):
        self.assertFalse(hits('```python\nprint("that matters")\n```'))

    def test_code_fence_even_with_quotes_enabled(self):
        self.assertFalse(hits('```text\nthat matters\n```',include_quoted=True))

    def test_inline_code_excluded(self):
        self.assertFalse(hits('`that matters`'))

    def test_repeated_phrases_counted(self):
        result = scan_text('That matters. That matters. That matters.')
        self.assertEqual(3, result['repeated_rule_hits']['empty_emphasis_001'])

    def test_false_positive_warning_not_authorship_claim(self):
        result = scan_text('The point that matters most to patients is documented.')
        self.assertTrue(result['findings'])
        self.assertIn('do not prove machine authorship',result['interpretation'])
        self.assertFalse(result['release_authorized'])

    def test_meaningful_emphasis_can_be_accepted(self):
        result = scan_text('That matters because the invoice was paid 32 days late.')
        self.assertTrue(result['findings'])
        self.assertTrue(all(x['severity'] in ('review','evidence') for x in result['findings']))

    def test_unsourced_generic_claim_is_evidence_warning(self):
        result = scan_text('Studies show this always works.')
        self.assertTrue(any(f['severity']=='evidence' for f in result['findings']))

    def test_not_just_but_also_pattern(self):
        self.assertTrue(any(f['id']=='contrast_not_just' for f in hits('It is not just a system, but also a product.')))

    def test_not_because_but_because(self):
        self.assertTrue(any(f['id']=='contrast_not_because' for f in hits('Not because of speed, but because of oversight.')))

    def test_rejected_random_nontext(self):
        with self.assertRaises(TypeError): scan_text(None)

    def test_large_input_fails(self):
        with self.assertRaises(ValueError): scan_text('abc' * 170000)

    def test_max_hit_limit(self):
        result = scan_text('That matters. '*200,max_hits=20)
        self.assertEqual(20,len(result['findings']))
        self.assertTrue(result['truncated'])

    def test_span_location_with_unicode_and_newlines(self):
        text = 'Résumé 📚.\n\nThat matters.'
        loc = [x for x in hits(text) if x['excerpt'].lower()=='that matters'][0]
        self.assertEqual((3,1), (loc['line'],loc['column']))
        self.assertEqual('That matters', text[loc['start']:loc['end']])

    def test_low_risk_regular_phrase_not_hard_banned(self):
        self.assertTrue(hits('In other words, the figures are close.'))
        self.assertEqual('review', next(f for f in hits('In other words, the figures are close.') if f['excerpt']=='In other words')['severity'])

    def test_regex_has_bounded_match(self):
        self.assertTrue(any(x['id']=='empty_impact_claim' for x in hits('The nonprofit achieved significant impact in 2026.')))

    def test_all_rule_categories_have_editorial_question(self):
        self.assertTrue(all(r['question'].endswith(('?','.')) for r in read_rules()))

    def test_duplicate_or_invalid_rule_pack_refused(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as d:
            pack = Path(d)/'bad.json'
            pack.write_text(json.dumps({'schema':'wi9.hotphrases/1','rules':[{'id':'abc','kind':'literal','expression':'that matters','category':'foo','question':'Check?'},{'id':'abc','kind':'literal','expression':'foo','category':'foo','question':'Check?'}]}))
            with self.assertRaises(ValueError): read_rules(pack)

    def test_quoted_phrase_can_be_reported_when_relevant(self):
        text='A document literally contains "that matters".'
        self.assertEqual([],hits(text))
        self.assertTrue(hits(text, include_quoted=True))

    def test_no_detector_probability_or_rewrite_returned(self):
        r=scan_text('That matters')
        self.assertNotIn('ai_probability',r)
        self.assertNotIn('rewritten_text',r)
        self.assertFalse(r['release_authorized'])


if __name__ == '__main__': unittest.main()
