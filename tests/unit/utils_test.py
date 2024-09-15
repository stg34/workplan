# encoding: utf-8

from tests.unit.base_test_case import BaseTestCase
import unittest
from srclib.utils import execute_git


class UtilsTest(BaseTestCase):
    def test_execute_git(self):
        with self.captured_output() as (out, err):
            ret = execute_git('tests/stub/git.sh', 'ls-files', True)
            self.assertEqual(['GIT STUB'], ret)
            self.assertIn('tests/stub/git.sh', out.getvalue())
            self.assertIn('GIT STUB', out.getvalue())
            self.assertEqual('', err.getvalue())


if __name__ == '__main__':
    unittest.main()
