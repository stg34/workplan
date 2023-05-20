# encoding: utf-8

import unittest
from tests.unit.base_test_case import BaseTestCase
from srclib.model.comment import Comment
from srclib.model.progress import Progress


class ProgressTest(BaseTestCase):
    def test_parse_01(self):
        progress = Progress.parse({'progress': ['50']})
        self.assertEqual(progress.value, 50)
        self.assertCountEqual([], progress.errors)

    def test_parse_02(self):
        progress = Progress.parse({'progress': ['B']})

        self.assertTrue(progress.has_errors)
        self.assertCountEqual([Progress.ERROR_WRONG_PROGRESS_FORMAT], progress.errors)
        self.assertIsNone(progress.value)

    def test_parse_03(self):
        progress = Progress.parse({'progress': ['1', '2']})

        self.assertCountEqual([Progress.ERROR_PROGRESS_IS_ALREADY_DEFINED], progress.errors)

    def test_parse_04(self):
        progress = Progress.parse({'progress': []})

        self.assertCountEqual([Progress.ERROR_PROGRESS_IS_NOT_DEFINED], progress.errors)

    def test_parse_05(self):
        progress = Progress.parse({'progress': ['200']})

        self.assertCountEqual([Progress.ERROR_PROGRESS_GT_100], progress.errors)

    def test_parse_06(self):
        progress = Progress.parse({'progress': ['-200']})

        self.assertCountEqual([Progress.ERROR_PROGRESS_LT_0], progress.errors)

    def test_state(self):
        self.assertEqual(Progress.STATE_ERROR, Progress.parse({'progress': []}).state)
        self.assertEqual(Progress.STATE_NOT_STARTED, Progress.parse({'progress': ['0']}).state)
        self.assertEqual(Progress.STATE_IN_PROGRESS, Progress.parse({'progress': ['20']}).state)
        self.assertEqual(Progress.STATE_ALMOST_DONE, Progress.parse({'progress': ['90']}).state)
        self.assertEqual(Progress.STATE_DONE, Progress.parse({'progress': ['100']}).state)

    def test_is_not_started(self):
        self.assertFalse(Progress.parse({'progress': []}).is_not_started)
        self.assertTrue(Progress.parse({'progress': ['0']}).is_not_started)

    def test_is_in_progress(self):
        self.assertFalse(Progress.parse({'progress': []}).is_in_progress)
        self.assertTrue(Progress.parse({'progress': ['20']}).is_in_progress)

    def test_is_almost_done(self):
        self.assertFalse(Progress.parse({'progress': []}).is_almost_done)
        self.assertTrue(Progress.parse({'progress': ['90']}).is_almost_done)

    def test_is_done(self):
        self.assertFalse(Progress.parse({'progress': []}).is_done)
        self.assertTrue(Progress.parse({'progress': ['100']}).is_done)

    def test_calc_error(self):
        comment_main = Comment.parse(self.src_comment({'id': [Comment.ID_MAIN], 'estimate': ['100'], 'progress': ['90']}), 1, None)
        comment_1 = Comment.parse(self.src_comment({'id': ['1'], 'estimate': ['2'], 'progress': ['25']}), 1, None)
        comment_2 = Comment.parse(self.src_comment({'id': ['2'], 'estimate': ['2'], 'progress': ['50']}), 1, None)
        comment_3 = Comment.parse(self.src_comment({'id': ['3'], 'estimate': [], 'progress': ['50']}), 1, None)

        progress = Progress.calc([comment_main, comment_1, comment_2, comment_3])
        self.assertIsNone(progress.value)
        self.assertCountEqual([Progress.ERROR_CALC_ERROR], progress.errors)

    def test_calc_success(self):
        comment_main = Comment.parse(self.src_comment({'id': [Comment.ID_MAIN], 'estimate': ['100'], 'progress': ['90']}), 1, None)
        comment_1 = Comment.parse(self.src_comment({'id': ['1'], 'estimate': ['2'], 'progress': ['25']}), 1, None)
        comment_2 = Comment.parse(self.src_comment({'id': ['2'], 'estimate': ['2'], 'progress': ['50']}), 1, None)

        progress = Progress.calc([comment_main, comment_1, comment_2])
        self.assertEqual(progress.value, 37.5)

    def test_calc_empty(self):
        progress = Progress.calc([])
        self.assertIsNone(progress.value)
        self.assertCountEqual([Progress.ERROR_CALC_ERROR], progress.errors)


if __name__ == '__main__':
    unittest.main()
