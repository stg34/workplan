# encoding: utf-8

import unittest
from tests.unit.view.dot.base_test_case import BaseViewDotTestCase
from srclib.view.dot.base_node import ViewDotBaseNode


class ViewDotBaseNodeTest(BaseViewDotTestCase):
    def test_fit_escape_string(self):
        node = ViewDotBaseNode()
        str = node.fit_escape_string('aaa/ssss/ddddd/fffff/ggggg/hhhhh/jjjjj/kkkkk/aaa.txt', width=40, splitter='/')
        self.assertEqual(str, 'aaa/ssss/ddddd/fffff/ggggg/hhhhh/jjjjj/<br/>kkkkk/aaa.txt')


if __name__ == '__main__':
    unittest.main()
