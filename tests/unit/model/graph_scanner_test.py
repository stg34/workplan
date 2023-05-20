# encoding: utf-8

import unittest
from tests.unit.base_test_case import BaseTestCase
from srclib.model.graph_scanner import GraphScanner


class GraphScannerTest(BaseTestCase):
    def test_scan_files(self):
        scanner = GraphScanner('PL')
        scanner.scan_files(['tests/data/data_01.txt', 'tests/data/plan.png', 'notfound.txt'])

        self.assertEqual(len(scanner.src_comments), 3)

        src_comment = scanner.src_comments[0]
        self.assertEqual(len(src_comment['src']), 1)

        src_comment = scanner.src_comments[1]
        self.assertEqual(len(src_comment['src']), 5)

        src_comment = scanner.src_comments[2]
        self.assertEqual(len(src_comment['src']), 6)
        self.assertEqual(src_comment['id'], ['id2'])
        self.assertEqual(src_comment['header'], ['descr2'])
        self.assertEqual(src_comment['dependencies'], ['id1'])
        self.assertEqual(src_comment['estimate'], ['1.5/2/4.5'])
        self.assertEqual(src_comment['progress'], ['50'])
        self.assertEqual(src_comment['developer_name'], ['Developer name'])

        self.assertTrue(scanner.has_errors)
        self.assertCountEqual(['tests/data/plan.png', 'notfound.txt'], [e['file_name'] for e in scanner.files_with_errors])


if __name__ == '__main__':
    unittest.main()
