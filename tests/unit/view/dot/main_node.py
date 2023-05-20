# encoding: utf-8

from srclib.view.dot.base_node import ViewDotBaseNode
from srclib.presenter.comment_presenter import GraphCommentPresenter


class ViewDotMainNode(ViewDotBaseNode):
    def __init__(self, comments_graph, comment, scheme):
        self.comments_graph = comments_graph
        self.comment = comment
        self.comment_presenter = GraphCommentPresenter(comment)
        self.scheme = scheme

    @property
    def color_ver(self):
        return 0

    @property
    def border_color(self):
        return self.scheme.line_1_color(0)

    @property
    def border_width(self):
        return 1

    @property
    def background_color(self):
        return self.scheme.node_background_color(1)

    @property
    def errors(self):
        errors = ''
        for error in self.comment_presenter.errors:
            errors += f'<tr><td {self.TD_ATTRS}>{self.font_error(self.fit_escape_string(error))}</td></tr>'

        for error in self.comment_presenter.graph_errors:
            errors += f'<tr><td {self.TD_ATTRS}>{self.font_error(self.fit_escape_string(error))}</td></tr>'

        return errors

    @property
    def error_label(self):
        content = f'''
            <table
                border="0"
                cellspacing="5"
                cellpadding="5"
                cellborder="{self.border_width}"
                color="{self.border_color}"
                bgcolor="{self.background_color}"
            >
                {self.errors}
            </table>'''

        return content

    @property
    def content(self):
        if self.comment_presenter.errors or self.comment_presenter.graph_errors:
            return f'"{self.comment.id}" [label=<{self.error_label}>]\n'

        return f'"{self.comment.id}" [shape="circle" label="" width="0.25" style="filled" color="{self.scheme.line_1_color(0)}"]\n'
