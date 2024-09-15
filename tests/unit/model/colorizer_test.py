# encoding: utf-8

import unittest
import configparser
from srclib.model.colorizer import Colorizer
from tests.unit.base_test_case import BaseTestCase


class ColorizerTest(BaseTestCase):
    def test_match(self):
        config = configparser.ConfigParser()

        config['FILE_COLOR'] = {
            '*.py': 'color_1',
            '*.js': 'color_2'
        }
        colorizer = Colorizer(config)

        self.assertEqual(colorizer.match('file.py'), 1)
        self.assertEqual(colorizer.match('file.js'), 2)


if __name__ == '__main__':
    unittest.main()
