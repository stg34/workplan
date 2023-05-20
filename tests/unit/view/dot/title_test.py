# encoding: utf-8

import unittest
import datetime
from tests.unit.view.dot.base_test_case import BaseViewDotTestCase
from srclib.view.dot.title import ViewDotTitle
from parsel import Selector

LABEL = 0
TIME_LABEL = 1
TIME_VALUE = 2
REMAINING_TIME_LABEL = 3
REMAINING_TIME_VALUE = 4
PROGRESS_LABEL = 5
PROGRESS_VALUE = 6
INFO = 8


class ViewDotTitleTest(BaseViewDotTestCase):
    def test_details_table(self):
        src_main = self.src_comment({
            'id': ['MAIN'],
            'dependencies': ['id1', 'id2', 'id3'],
        })

        src1 = self.src_comment({
            'id': ['id1'],
            'estimate': ['8'],
            'progress': ['25'],
            'developer_name': ['Developer 1'],
        })

        src2 = self.src_comment({
            'id': ['id2'],
            'estimate': ['2'],
            'progress': ['50'],
            'developer_name': ['Developer 1'],
        })

        src3 = self.src_comment({
            'id': ['id3'],
            'estimate': ['2'],
            'progress': ['50'],
            'developer_name': ['Developer 2'],
        })

        task = self.build_task_from_src([src_main, src1, src2, src3])
        task.built_at = datetime.datetime(2020, 5, 17, 11, 22, 33)
        self.assertFalse(task.graph.has_error)

        view_title = ViewDotTitle(task, self.default_color_scheme)
        details_table = view_title.details_table

        selector = Selector(text=details_table)
        rows_selector = selector.css('tr')

        self.assertEqual(len(rows_selector), 3)

        # Total / built time
        total_rows_selector = rows_selector[0]
        cells_selector = total_rows_selector.css('td')
        cells = [self.get_selector_text(cs) for cs in cells_selector]

        self.assertEqual(cells[LABEL], 'Total')
        self.assertEqual(cells[TIME_LABEL], 'Time')
        self.assertEqual(cells[TIME_VALUE], '12 h.')
        self.assertEqual(cells[REMAINING_TIME_LABEL], 'Remaining time')
        self.assertEqual(cells[REMAINING_TIME_VALUE], '8 h.')
        self.assertEqual(cells[INFO], '2020.05.17 11:22:33')

        # Developer 1 / main comment definition
        developer1_rows_selector = rows_selector[1]
        cells_selector = developer1_rows_selector.css('td')
        cells = [self.get_selector_text(cs) for cs in cells_selector]

        self.assertEqual(cells[LABEL], 'Developer 1:')
        self.assertEqual(cells[TIME_LABEL], 'Time')
        self.assertEqual(cells[TIME_VALUE], '10 h.')
        self.assertEqual(cells[REMAINING_TIME_LABEL], 'Remaining time')
        self.assertEqual(cells[REMAINING_TIME_VALUE], '7 h.')
        self.assertEqual(cells[INFO], 'file.name:1')

        # Developer 2 / work hours
        developer1_rows_selector = rows_selector[2]
        cells_selector = developer1_rows_selector.css('td')
        cells = [self.get_selector_text(cs) for cs in cells_selector]

        self.assertEqual(cells[LABEL], 'Developer 2:')
        self.assertEqual(cells[INFO], '')

    def test_errors_table_01(self):
        src_main = self.src_comment({
            'id': ['MAIN'],
        })

        src1 = self.src_comment({
            'id': ['id1'],
            'estimate': ['8'],
            'progress': ['25'],
            'developer_name': ['Developer 1'],
        })

        task = self.build_task_from_src([src_main, src1])
        self.assertTrue(task.graph.has_error)

        view_title = ViewDotTitle(task, self.default_color_scheme)
        errors_table = view_title.errors_table

        selector = Selector(text=errors_table)
        rows_selector = selector.css('tr')

        self.assertEqual(len(rows_selector), 1)
        self.assertEqual(self.get_selector_text(rows_selector[0]), 'Comments with errors')

    def test_errors_table_02(self):
        src_main = self.src_comment({
            'id': ['MAIN'],
            'dependencies': ['id1'],
        })

        src1 = self.src_comment({
            'id': ['id1'],
            'estimate': ['8'],
            'progress': ['25'],
            'developer_name': ['Developer 1'],
        })

        task = self.build_task_from_src([src_main, src1])
        self.assertFalse(task.graph.has_error)

        view_title = ViewDotTitle(task, self.default_color_scheme)
        errors_table = view_title.errors_table

        self.assertEqual(errors_table, '')

    def test_label(self):
        src_main = self.src_comment({
            'id': ['MAIN'],
            'header': ['Task title'],
        })

        src1 = self.src_comment({
            'id': ['id1'],
            'estimate': ['8'],
            'progress': ['25'],
        })

        task = self.build_task_from_src([src_main, src1], work_hours=4)
        task.built_at = datetime.datetime(2020, 5, 17, 11, 22, 33)
        self.assertTrue(task.graph.has_error)

        view_title = ViewDotTitle(task, self.default_color_scheme)
        label_table = view_title.label

        selector = Selector(text=label_table)
        rows_selector = selector.css('body>table>tr')

        self.assertEqual(len(rows_selector), 4)
        self.assertEqual(self.get_selector_text(rows_selector[0]), 'Task title')
        self.assertEqual(self.get_selector_text(rows_selector[2]), 'Comments with errors')


if __name__ == '__main__':
    unittest.main()
