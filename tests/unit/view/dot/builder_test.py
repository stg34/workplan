# encoding: utf-8

import unittest
import datetime
from tests.unit.view.dot.base_test_case import BaseViewDotTestCase
from srclib.view.dot.builder import ViewDotBuilder


class ViewDotBuilderTest(BaseViewDotTestCase):
    def test_build(self):
        src_main = self.src_comment({
            'id': ['MAIN'],
            'header': ['Task title'],
            'dependencies': ['id1', 'id2'],
        })

        src1 = self.src_comment({
            'id': ['id1'],
            'header': ['comment 1'],
            'estimate': ['8'],
            'progress': ['25'],
            'developer_name': ['Developer 1'],
        })

        src2 = self.src_comment({
            'id': ['id2'],
            'header': ['comment 2'],
            'estimate': ['2'],
            'progress': ['50'],
            'developer_name': ['Developer 1'],
        })

        task = self.build_task_from_src([src_main, src1, src2])
        task.built_at = datetime.datetime(2020, 5, 17, 11, 22, 33)
        self.assertFalse(task.graph.has_error)

        builder = ViewDotBuilder(task, False, self.default_color_scheme, 'tb', 'dot', False)
        builder.build()

        self.assertIn('Task title', builder.content)
        self.assertIn('Developer 1', builder.content)
        self.assertIn('2020.05.17 11:22:33', builder.content)
        self.assertIn('comment 1', builder.content)
        self.assertIn('comment 2', builder.content)


if __name__ == '__main__':
    unittest.main()
