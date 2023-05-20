# encoding: utf-8

import unittest
from tests.unit.base_test_case import BaseTestCase
from srclib.model.comment import Comment
from srclib.model.task import Task


class TaskTest(BaseTestCase):
    def build_task(self):
        src_main = self.src_comment({'id': [Comment.ID_MAIN], 'dependencies': ['id1', 'id2', 'id3']})
        src_1 = self.src_comment({'id': ['id1'], 'estimate': ['80'], 'progress': ['25'], 'developer_name': ['Foo']})
        src_2 = self.src_comment({'id': ['id2'], 'estimate': ['160'], 'progress': ['50'], 'developer_name': ['Bar']})
        src_3 = self.src_comment({'id': ['id3'], 'estimate': ['40'], 'progress': ['50']})

        task = Task(None)
        comments = []

        comments.append(Comment.parse(src_main, 1, None))
        comments.append(Comment.parse(src_1, 1, None))
        comments.append(Comment.parse(src_2, 1, None))
        comments.append(Comment.parse(src_3, 1, None))

        task.build(comments)

        self.assertFalse(task.graph.has_error)

        return task

    def test_comments(self):
        task = self.build_task()

        self.assertCountEqual([c.id for c in task.comments], [Comment.ID_MAIN, 'id1', 'id2', 'id3'])

    def test_semantic_comments(self):
        task = self.build_task()

        self.assertCountEqual([c.id for c in task.semantic_comments], ['id1', 'id2', 'id3'])

    def test_main_comment(self):
        task = self.build_task()

        self.assertIsNotNone(task.main_comment)
        self.assertEqual(task.main_comment.id, Comment.ID_MAIN)

    def test_estimate(self):
        task = self.build_task()

        self.assertIsNotNone(task.estimate)
        self.assertEqual(task.estimate.time_expected, 280)

    def test_remaining_estimate(self):
        task = self.build_task()

        self.assertIsNotNone(task.remaining_estimate)
        self.assertEqual(task.remaining_estimate.time_expected, 160)

    def test_progress(self):
        task = self.build_task()

        self.assertIsNotNone(task.progress)
        self.assertAlmostEqual(task.progress.value, 42.85, delta=0.1)

    def test_developers(self):
        task = self.build_task()

        self.assertCountEqual([d.name for d in task.developers], ['Foo', 'Bar'])


if __name__ == '__main__':
    unittest.main()
