# encoding: utf-8

# TODO: PL: Создать класс колоризатора, который будет отвечать за цвет в зависимости от пути или имени файла.
# ID: srclib/model/colorizer.py:1
# TIME: 2
# COMPL: 90


from pathlib import PurePath


class ColorizerParseError(Exception):
    def __init__(self, opt, val):
        self.opt = opt
        self.val = val


class Colorizer:
    ALLOWED_COLORS = ['color1', 'color2', 'color3']
    DEFAULT_COLOR_NUM = 2

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
