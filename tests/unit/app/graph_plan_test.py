# encoding: utf-8
from tests.unit.base_test_case import BaseTestCase
import unittest
import shutil
from pathlib import Path
from srclib.app.graph_plan import AppPlanGraph


class AppPlanGraphTest(BaseTestCase):
    def setUp(self):
        if Path('tmp/test').is_dir():
            shutil.rmtree('tmp/test')

        Path('tmp/test').mkdir(parents=True, exist_ok=True)

    # @unittest.skip('coverage')
    def test_build(self):
        with self.captured_output() as (out, err):
            plan = AppPlanGraph(['-bmaster', '--src=tests/manual/test01.txt', '--out-dir=tmp/test'])
            plan.build()
            self.assertIn('Diagram: tmp/test/plan.png', out.getvalue())
            self.assertIn('Plan: tmp/test/plan.md', out.getvalue())
            self.assertTrue(Path('tmp/test/plan.md').exists())
            self.assertTrue(Path('tmp/test/plan.png').exists())


if __name__ == '__main__':
    unittest.main()
