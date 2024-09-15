# encoding: utf-8

import unittest
from unittest.mock import patch
from tests.unit.base_test_case import BaseTestCase
from srclib.model.file_list import FileList
from srclib.utils import ExecuteCommandError


class FileListTest(BaseTestCase):
    def test_file_list_01(self):
        with patch('srclib.model.file_list.execute_git', return_value=['a.py', 'a.py', 'b.py', 'c.txt']):
            file_list = FileList('git', 'master')
            file_list.list(exclude_ext=['txt', 'log'])
            self.assertCountEqual(['a.py', 'b.py'], file_list.file_names)
            self.assertFalse(file_list.has_errors)

    def test_file_list_02(self):
        with patch('srclib.model.file_list.execute_git', side_effect=ExecuteCommandError('command', 'stdout', 'stderr', 'ret')):
            file_list = FileList('git', 'master')
            file_list.list(exclude_ext=['txt', 'log'])
            self.assertCountEqual([], file_list.file_names)
            self.assertTrue(file_list.has_errors)


if __name__ == '__main__':
    unittest.main()
