# encoding: utf-8

from pathlib import PurePath


class ColorizerParseError(Exception):
    def __init__(self, opt, val):
        self.opt = opt
        self.val = val


class Colorizer:
    ALLOWED_COLORS = ['color_1', 'color_2', 'color_3']
    DEFAULT_COLOR_NUM = 1

    def __init__(self, config):
        self.config = config
        self.patterns = []

        self.parse()

    def parse(self):
        if 'FILE_COLOR' not in self.config:
            return

        for opt in self.config.options('FILE_COLOR'):
            val = self.config.get('FILE_COLOR', opt)
            if val not in self.ALLOWED_COLORS:
                raise ColorizerParseError(opt, val)

            self.patterns.append([opt, int(val[-1])])

    def match(self, file_name):
        for pattern in self.patterns:
            if PurePath(file_name).match(pattern[0]):
                return pattern[1]

        return self.DEFAULT_COLOR_NUM
