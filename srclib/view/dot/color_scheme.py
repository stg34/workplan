# encoding: utf-8

from srclib.view.dot.colors import COLORS


class ViewDotColorScheme:
    ARGS = {
            'dpi': 60,
            'font_name': 'Helvetica,Arial,sans-serif',
            'graph_title_fontsize': 24,
            'node_main_font_size': 16,
            'node_font_size': 14,
            'edge_font_size': 14
        } | COLORS

    def __init__(self, config, section):
        self.config = config
        self.section = section

        self.parse_config(config, section)

    def color(self, name, ver):
        return getattr(self, f'color_{name}v{ver}')

    def font_primary_color(self, ver):
        return getattr(self, f'font_primary_color_{ver}')

    def font_secondary_color(self, ver):
        return getattr(self, f'font_secondary_color_{ver}')

    def node_background_color(self, ver):
        return getattr(self, f'node_color_{ver}')

    def line_1_color(self, ver):
        return getattr(self, f'line_1_color_{ver}')

    def line_2_color(self, ver):
        return getattr(self, f'line_2_color_{ver}')

    def line_error_color(self, ver):
        return getattr(self, f'line_error_color_{ver}')

    def parse_config(self, config, section):
        for key in self.ARGS:
            value = config.get(section, key, fallback=self.ARGS[key])
            setattr(self, key, value)
