# encoding: utf-8

from html import escape


class ViewDotBaseNode:
    TD_ATTRS = 'balign="left" align="left"'

    def fit_escape_string(self, string, width=40, splitter=' '):
        lines = []
        current_line = ''
        parts = string.split(splitter)

        for part in parts:
            if len(current_line + part) >= width:
                lines.append(current_line + f'{splitter}<br/>')
                current_line = ''
            elif current_line:
                current_line += splitter

            current_line += escape(part)

        if current_line:
            lines.append(current_line)

        return ''.join(lines).strip()

    def font_tag(self, text, size, color, bold=False):
        if bold:
            bold_open = '<b>'
            bold_close = '</b>'
        else:
            bold_open = ''
            bold_close = ''

        return f'<font point-size="{size}" color="{color}">{bold_open}{text}{bold_close}</font>'

    @property
    def font_color_1(self):
        return self.scheme.font_color_1(self.color_ver)

    @property
    def font_color_2(self):
        return self.scheme.font_color_2(self.color_ver)

    @property
    def error_color(self):
        return self.scheme.error_color(0)

    def font_primary(self, text, bold=False):
        return self.font_tag(text, self.scheme.node_font_size, self.font_color_1, bold)

    def font_secondary(self, text, bold=False):
        return self.font_tag(text, self.scheme.node_font_size, self.font_color_2, bold)

    def font_error(self, text, bold=False):
        return self.font_tag(text, self.scheme.node_font_size, self.error_color, bold)

    @property
    def border_color(self):
        return self.scheme.color_1(0)
