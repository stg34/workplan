# encoding: utf-8

import unittest
from tests.unit.view.dot.base_test_case import BaseViewDotTestCase
from srclib.view.dot.node import ViewDotNode
from parsel import Selector


class ViewDotNodeTest(BaseViewDotTestCase):
    def test_label(self):
        src_main = self.src_comment({
            'id': ['MAIN'],
            'dependencies': ['id1', 'id21', 'id3'],
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
            'header': ['comment 2', 'comment 2'],
            'estimate': [],
            'progress': [],
            'dependencies': ['id3'],
            # 'developer_name': ['Developer 1'],
        })

        src3 = self.src_comment({
            'id': ['id3'],
            'header': ['comment 3'],
            'estimate': ['1/2/3'],
            'progress': [],
            'developer_name': ['Developer 2'],
            'blocker': ['Blocker comment']
        })

        task = self.build_task_from_src([src_main, src1, src2, src3])
        self.assertTrue(task.graph.has_error)

        comment1 = task.graph.comment('id1')

        node1 = ViewDotNode(task.graph, comment1, self.default_color_scheme)
        selector = Selector(text=node1.label)
        rows_selector = selector.css('tr')

        self.assertEqual(len(rows_selector), 3)
        self.assertIn('comment 1', self.get_selector_text(rows_selector[0]))
        self.assertIn('file.name:1', self.get_selector_text(rows_selector[0]))
        self.assertIn('Time: 8 h', self.get_selector_text(rows_selector[1]))
        self.assertIn('Progress: 25 %', self.get_selector_text(rows_selector[1]))
        self.assertIn('Developer 1', self.get_selector_text(rows_selector[2]))

        comment2 = task.graph.comment('id2')
        node2 = ViewDotNode(task.graph, comment2, self.default_color_scheme)
        selector = Selector(text=node2.label)
        rows_selector = selector.css('tr')

        self.assertEqual(len(rows_selector), 7)
        self.assertIn('Time: ?', self.get_selector_text(rows_selector[1]))
        self.assertIn('Progress: ?', self.get_selector_text(rows_selector[1]))
        self.assertIn('Header is already defined', self.get_selector_text(rows_selector[3]))
        self.assertIn('Time is not defined', self.get_selector_text(rows_selector[4]))
        self.assertIn('Progress is not defined', self.get_selector_text(rows_selector[5]))

        comment = task.graph.comment('id3')
        node = ViewDotNode(task.graph, comment, self.default_color_scheme)
        selector = Selector(text=node.label)
        rows_selector = selector.css('tr')

        self.assertEqual(len(rows_selector), 5)
        self.assertIn('Blocker: Blocker comment', self.get_selector_text(rows_selector[3]))
        self.assertIn('Time: 2 h. (1/2/3)', self.get_selector_text(rows_selector[1]))


if __name__ == '__main__':
    unittest.main()
