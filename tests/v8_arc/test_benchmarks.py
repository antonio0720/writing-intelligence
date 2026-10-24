import json
import pathlib
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from arc_v8.engine import classify, evaluate, digest
class BenchmarkTests(unittest.TestCase):
    def test_exact_vectors(self):
        v=json.loads((ROOT/'benchmarks/arc_v8_vectors.json').read_text())
        self.assertEqual(v['schema'],'wi.arc.benchmark/v1')
        self.assertGreaterEqual(len(v['vectors']),7)
        for x in v['vectors']:
            with self.subTest(case=x['id']):
                p=classify({'want_outcome':x['want'],'need_outcome':x['need'],'closure':x['closure']},x.get('need_basis','author_asserted'))
                self.assertEqual(p['quadrant'],x['expected'])
    def test_report_no_reader_quality_claim(self):
        d=json.loads((ROOT/'tests/v8_arc/fixtures/four_quadrants.json').read_text())
        report=evaluate(d)
        self.assertEqual(report['coverage']['human_review'],'not_performed_by_this_tool')
        self.assertEqual(report['coverage']['reader_study'],'not_performed_by_this_tool')
        self.assertEqual(report['source_digest'],digest(d))

if __name__=='__main__':unittest.main()
