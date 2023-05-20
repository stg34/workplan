# encoding: utf-8

import unittest
from tests.unit.base_test_case import BaseTestCase
from srclib.model.developer import Developer
from srclib.model.comment import Comment


class DeveloperTest(BaseTestCase):
    def test_parse_01(self):
        src1 = self.src_comment({
            'id': ['ID1'],
            'estimate': ['8'],
            'progress': ['25'],
            'developer_name': ['Developer'],
        })

        src2 = self.src_comment({
            'id': ['ID2'],
            'estimate': ['2'],
            'progress': ['50'],
            'developer_name': ['Developer'],
        })

        comment1 = Comment.parse(src1, 1, 4)
        comment2 = Comment.parse(src2, 1, 4)

        developer = Developer('Developer')
        developer.add_comment(comment1)
        developer.add_comment(comment2)

        self.assertEqual(developer.estimate.time_expected, 10)
        self.assertEqual(developer.remaining_estimate.time_expected, 7)
        self.assertEqual(developer.progress.value, 30)


if __name__ == '__main__':
    unittest.main()
