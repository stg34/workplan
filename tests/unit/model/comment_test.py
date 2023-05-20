# encoding: utf-8

import unittest
from tests.unit.base_test_case import BaseTestCase
from srclib.model.comment import Comment
from srclib.model.estimate import Estimate
from srclib.model.progress import Progress


class CommentTest(BaseTestCase):
    def test_parse_01(self):
        scale = 2
        src = {
            'src': [],
            'file_name': 'file.name',
            'line_num': 11,
            'id': ['ID'],
            'header': ['Header'],
            'dependencies': ['dep1', 'dep2'],
            'estimate': ['10'],
            'progress': ['30'],
            'developer_name': ['Developer'],
            'blocker': ['Blocker'],
            'order': 2
        }
        comment = Comment.parse(src, scale, 4)

        self.assertFalse(comment.has_errors)
        self.assertEqual(comment.id, 'ID')
        self.assertEqual(comment.header, 'Header')
        self.assertCountEqual(comment.dependencies, ['dep1', 'dep2'])
        self.assertEqual(comment.estimate.time_expected, 10 * scale)
        self.assertEqual(comment.progress.value, 30)
        self.assertEqual(comment.developer_name, 'Developer')
        self.assertEqual(comment.blocker_comment, 'Blocker')
        self.assertTrue(comment.blocker)
        self.assertFalse(comment.blocked)
        self.assertEqual(comment.order, 2)
        self.assertEqual(comment.file_name, 'file.name')
        self.assertEqual(comment.src_line_num, 11)
        self.assertEqual(comment.def_position, 'file.name:11')
        self.assertEqual(comment.remaining_estimate.time_expected, 14)
        self.assertFalse(comment.is_main)

    def test_parse_02(self):
        comment = Comment.parse(self.src_comment({'id': []}), 1, None)

        self.assertTrue(comment.has_errors)
        self.assertCountEqual([Comment.ERROR_ID_IS_NOT_DEFINED], comment.errors)

    def test_parse_03(self):
        comment = Comment.parse(self.src_comment({'id': ['1', '2']}), 1, None)

        self.assertTrue(comment.has_errors)
        self.assertCountEqual([Comment.ERROR_ID_IS_ALREADY_DEFINED], comment.errors)

    def test_parse_04(self):
        comment = Comment.parse(self.src_comment({'id': [1], 'header': []}), 1, None)

        self.assertTrue(comment.has_errors)
        self.assertCountEqual([Comment.ERROR_HEADER_IS_NOT_DEFINED], comment.errors)

    def test_parse_05(self):
        comment = Comment.parse(self.src_comment({'id': [1], 'header': ['h1', 'h2']}), 1, None)

        self.assertTrue(comment.has_errors)
        self.assertCountEqual([Comment.ERROR_HEADER_IS_ALREADY_DEFINED], comment.errors)

    def test_parse_06(self):
        comment = Comment.parse(self.src_comment({'id': [1], 'developer_name': ['d1', 'd2']}), 1, None)

        self.assertTrue(comment.has_errors)
        self.assertCountEqual([Comment.ERROR_DEVELOPER_IS_ALREADY_DEFINED], comment.errors)

    def test_parse_07(self):
        comment = Comment.parse(self.src_comment({'id': [1], 'blocker': ['b1', 'b2']}), 1, None)

        self.assertTrue(comment.has_errors)
        self.assertCountEqual([Comment.ERROR_BLOCKER_IS_ALREADY_DEFINED], comment.errors)

    def test_parse_08(self):
        comment = Comment.parse(self.src_comment({'id': [1], 'order': None}), 1, None)

        self.assertTrue(comment.has_errors)
        self.assertCountEqual([Comment.ERROR_ORDER_IS_NOT_DEFINED], comment.errors)

    def test_parse_09(self):
        comment = Comment.parse(self.src_comment({'id': [1], 'dependencies': ['', Comment.ID_MAIN, 'Dep']}), 1, None)

        self.assertTrue(comment.has_errors)
        self.assertCountEqual([Comment.ERROR_REFERENCE_TO_MAIN, Comment.ERROR_EMPTY_DEPENDENCY], comment.errors)

    def test_parse_main(self):
        src = {
            'src': [],
            'file_name': 'file.name',
            'line_num': 11,
            'id': [Comment.ID_MAIN],
            'header': ['Header'],
            'dependencies': ['dep1', 'dep2'],
            'estimate': ['10'],
            'progress': ['30'],
            'developer_name': ['Developer'],
            'blocker': ['Blocker'],
            'order': 2
        }
        comment = Comment.parse(self.src_comment(src), 1, None)

        self.assertFalse(comment.has_errors)
        self.assertTrue(comment.is_main)
        self.assertIsInstance(comment.estimate, Estimate)
        self.assertIsInstance(comment.progress, Progress)


if __name__ == '__main__':
    unittest.main()
