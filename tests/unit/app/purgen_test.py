# encoding: utf-8
from tests.unit.base_test_case import BaseTestCase
import unittest
import shutil
from pathlib import Path
from srclib.app.purgen import AppPurgen


class AppPurgenTest(BaseTestCase):
    def setUp(self):
        if Path('tmp/test').is_dir():
            shutil.rmtree('tmp/test')

        Path('tmp/test').mkdir(parents=True, exist_ok=True)

    # @unittest.skip('coverage')
    def test_purge(self):
        with self.captured_output() as (out, err):
            purgen = AppPurgen(['-bmaster', '--dry-run', '--src=tests/manual/test01.txt', '--out-dir=tmp/test'])
            purgen.purge()
            self.assertIn('PATCH FILE: tmp/test/plan.patch', out.getvalue())
            self.assertTrue(Path('tmp/test/plan.patch').exists())

    def test_remove_comments(self):

        lines = [
            'COMMENT\n',  # 1
            'COMMENT\n',  # 2
            '\n',         # 3
            'COMMENT\n',  # 4
            '\n',         # 5
            'CODE\n',     # 6
            'CODE\n',     # 7
            'COMMENT\n',  # 8
            'COMMENT\n',  # 9
        ]

        expected_lies = [
            'CODE\n',
            'CODE\n',
        ]

        purgen = AppPurgen(['-bmaster', '--dry-run', '--src=tests/manual/test01.txt', '--out-dir=tmp/test'])

        result = purgen.remove_comments(lines, [[1, 2], [4], [8], [9]])

        self.assertEqual(expected_lies, result)


if __name__ == '__main__':
    unittest.main()
