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
    def font_primary_color(self):
        return self.scheme.font_primary_color(self.color_ver)

    @property
    def font_secondary_color(self):
        return self.scheme.font_secondary_color(self.color_ver)

    @property
    def error_color(self):
        return self.scheme.line_error_color(0)

    def font_primary(self, text, bold=False):
        return self.font_tag(text, self.scheme.node_font_size, self.font_primary_color, bold)

    def font_secondary(self, text, bold=False):
        return self.font_tag(text, self.scheme.node_font_size, self.font_secondary_color, bold)

    def font_error(self, text, bold=False):
        return self.font_tag(text, self.scheme.node_font_size, self.error_color, bold)

    @property
    def border_color(self):
        return self.scheme.line_1_color(0)
