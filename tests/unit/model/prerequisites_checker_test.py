# encoding: utf-8

import unittest
from tests.unit.base_test_case import BaseTestCase
from srclib.model.prerequisites_checker import PrerequisitesChecker


class PrerequisitesCheckerTest(BaseTestCase):
    def test_scan_files(self):
        checker = PrerequisitesChecker('foo/bar', '/foo/bar/git', '/foo/bar/dot')
        checker.check()

        self.assertTrue(checker.has_errors)
        self.assertCountEqual([
            PrerequisitesChecker.ERROR_NOT_DIRECTORY,
            PrerequisitesChecker.ERROR_GIT_NOT_FOUND,
            PrerequisitesChecker.ERROR_DOT_NOT_FOUND
            ], checker.errors)


if __name__ == '__main__':
    unittest.main()
