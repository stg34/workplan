# encoding: utf-8

from srclib.view.dot.colors import COLORS_DARK
from srclib.view.dot.colors import COLORS_LIGHT


class ViewDotColorScheme:
    def __init__(self, config, section):
        self.config = config
        self.section = section

        self.parse_config(config, section)

    @property
    def args(self):
        if self.section == 'COLOR_SCHEME_DARK':
            colors = COLORS_DARK
        else:
            colors = COLORS_LIGHT

        return {
            'dpi': 60,
            'font_name': 'Helvetica,Arial,sans-serif',
            'graph_title_fontsize': 24,
            'node_main_font_size': 16,
            'node_font_size': 14,
            'edge_font_size': 14
        } | colors

    def font_color_1(self, ver):
        return getattr(self, f'font_color_1_{ver}')

    def font_color_2(self, ver):
        return getattr(self, f'font_color_2_{ver}')

    def node_background_color(self, ver):
        return getattr(self, f'node_background_color_{ver}')

    def color_1(self, ver):
        return getattr(self, f'color_1_{ver}')

    def color_2(self, ver):
        return getattr(self, f'color_2_{ver}')

    def color_3(self, ver):
        return getattr(self, f'color_3_{ver}')

    def error_color(self, ver):
        return getattr(self, f'error_color_{ver}')

    def parse_config(self, config, section):
        for key in self.args:
            value = config.get(section, key, fallback=self.args[key])
            setattr(self, key, value)
