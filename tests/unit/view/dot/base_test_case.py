# encoding: utf-8

import configparser
from tests.unit.view.base_test_case import BaseViewTestCase
from srclib.view.dot.color_scheme import ViewDotColorScheme


class BaseViewDotTestCase(BaseViewTestCase):
    @property
    def default_color_scheme(self):
        config = configparser.ConfigParser()
        config.read('fake_config')
        return ViewDotColorScheme(config, 'fake_section')
