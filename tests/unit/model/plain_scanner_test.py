# encoding: utf-8

import unittest
from tests.unit.base_test_case import BaseTestCase
from srclib.model.plain_scanner import PlainScanner


class PlainScannerTest(BaseTestCase):
    def test_scan_files(self):
        scanner = PlainScanner('PPL01')
        scanner.scan_files(['tests/data/plain/data_01.txt', 'tests/data/plan.png', 'notfound.txt'])

        self.assertEqual(len(scanner.src_comments), 3)
        src_comment = scanner.src_comments[0]
        self.assertEqual(src_comment['id'], ['tests/data/plain/data_01.txt:1'])

        src_comment = scanner.src_comments[1]
        self.assertEqual(src_comment['id'], ['tests/data/plain/data_01.txt:3'])
        self.assertEqual(src_comment['header'], ['description 2'])
        self.assertEqual(src_comment['estimate'], ['1'])
        self.assertEqual(src_comment['progress'], ['100'])
        self.assertEqual(src_comment['order'], '21')

        src_comment = scanner.src_comments[2]
        self.assertEqual(src_comment['id'], ['tests/data/plain/data_01.txt:5'])
        self.assertEqual(src_comment['header'], ['description 3 1/20/'])

        self.assertTrue(scanner.has_errors)
        self.assertCountEqual(['tests/data/plan.png', 'notfound.txt'], [e['file_name'] for e in scanner.files_with_errors])


if __name__ == '__main__':
    unittest.main()
