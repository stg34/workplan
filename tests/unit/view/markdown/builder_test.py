# encoding: utf-8

import unittest
import datetime
from tests.unit.view.base_test_case import BaseViewTestCase
from srclib.view.markdown.builder import ViewMarkdownBuilder
from pathlib import Path
import pycmarkgfm
from parsel import Selector


class ViewMarkdownBuilderTest(BaseViewTestCase):
    def test_builder(self):
        src_main = self.src_comment({
            'id': ['MAIN'],
            'header': ['Task title'],
            'dependencies': ['id1', 'id2'],
        })

        src1 = self.src_comment({
            'id': ['id1'],
            'header': ['Comment 1'],
            'estimate': ['8'],
            'progress': ['25'],
            'dependencies': ['id3'],
            'developer_name': ['Developer 1'],
        })

        src2 = self.src_comment({
            'id': ['id2'],
            'header': ['Comment 2'],
            'estimate': ['2'],
            'progress': ['50'],
            'dependencies': ['id3'],
            'developer_name': ['Developer 1'],
        })

        src3 = self.src_comment({
            'id': ['id3'],
            'header': ['Comment 3'],
            'estimate': ['2'],
            'progress': ['100'],
            'developer_name': ['Developer 2'],
        })

        task = self.build_task_from_src([src_main, src1, src2, src3])
        task.built_at = datetime.datetime(2020, 5, 17, 11, 22, 33)
        self.assertFalse(task.graph.has_error)

        builder = ViewMarkdownBuilder(task, 4, 2)
        builder.build()

        self.assertIn('Task title', builder.content)
        self.assertIn('2020.05.17 11:22:33', builder.content)
        self.assertIn('Comment 1', builder.content)
        self.assertIn('Comment 2', builder.content)
        self.assertIn('Comment 3', builder.content)

        html = pycmarkgfm.gfm_to_html(builder.content)

        Path('plan.html').write_text(html)
        selector = Selector(text=html)

        # Title
        self.assertEqual(selector.xpath('/html/body/h2/text()').get(), 'Task title')

        # Summary
        self.assertEqual(selector.xpath('/html/body/p[1]/strong/text()').get().strip(), 'Time: 12 h.')
        self.assertEqual(selector.xpath('/html/body/p[2]/strong/text()').get().strip(), 'Remaining time: 7 h.')
        self.assertEqual(selector.xpath('/html/body/p[3]/strong/text()').get().strip(), 'Progress: 41 %')
        self.assertEqual(selector.xpath('/html/body/p[4]/text()').get().strip(), '2020.05.17 11:22:33')

        # Comment 1
        self.assertEqual(selector.xpath('/html/body/h3[1]/text()').get().strip(), 'Comment 1')
        self.assertEqual(selector.xpath('/html/body/ul[1]/li[1]/text()').get().strip(), 'File: file.name:1')
        self.assertEqual(selector.xpath('/html/body/ul[1]/li[2]/text()').get().strip(), 'Time: 8 h.')
        self.assertEqual(selector.xpath('/html/body/ul[1]/li[3]/text()').get().strip(), 'Progress: 25 %')

        # Comment 2. Complete, subtask of comment 1
        self.assertEqual(selector.xpath('/html/body/ul[1]/li[3]/h4/del/text()').get().strip(), 'Comment 3')
        self.assertEqual(selector.xpath('/html/body/ul[1]/li[3]/ul/li[1]/del/text()').get().strip(), 'File: file.name:1')
        self.assertEqual(selector.xpath('/html/body/ul[1]/li[3]/ul/li[2]/del/text()').get().strip(), 'Time: 2 h.')
        self.assertEqual(selector.xpath('/html/body/ul[1]/li[3]/ul/li[3]/del/text()').get().strip(), 'Progress: 100 %')

        # Comment 3
        self.assertEqual(selector.xpath('/html/body/h3[2]/text()').get().strip(), 'Comment 2')
        self.assertEqual(selector.xpath('/html/body/ul[2]/li[1]/text()').get().strip(), 'File: file.name:1')
        self.assertEqual(selector.xpath('/html/body/ul[2]/li[2]/text()').get().strip(), 'Time: 2 h.')
        self.assertEqual(selector.xpath('/html/body/ul[2]/li[3]/text()').get().strip(), 'Progress: 50 %')


if __name__ == '__main__':
    unittest.main()
