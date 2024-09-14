# encoding: utf-8

from srclib.view.dot.base_node import ViewDotBaseNode
from srclib.presenter.comment_presenter import GraphCommentPresenter


class ViewDotNode(ViewDotBaseNode):
    def __init__(self, graph, comment, scheme, colorizer):
        self.graph = graph
        self.comment = comment
        self.comment_presenter = GraphCommentPresenter(comment)
        self.scheme = scheme
        self.colorizer = colorizer

    @property
    def color_ver(self):
        if self.comment.blocked or self.comment.estimate.has_errors:
            return 0

        if self.comment.progress.is_almost_done:
            return 1
        elif self.comment.progress.is_done:
            return 2

        return 0

    @property
    def border_color(self):
        ver = self.color_ver

        if self.comment.blocked or self.comment.estimate.has_errors:
            return self.scheme.error_color(ver)

        # TODO: PL: В классе ViewDotNode определить с помощью колоризатора цвет узла
        # ID: srclib/view/dot/node.py:30
        # DEP: srclib/view/dot/builder.py:47
        # TIME: 0.1
        # COMPL: 100

        color_name = self.colorizer.match(self.comment.file_name)

        if color_name == 1:
            return self.scheme.color_1(ver)

        if color_name == 2:
            return self.scheme.color_2(ver)

        return self.scheme.color_3(ver)

    @property
    def border_width(self):
        if self.comment.estimate.has_errors:
            return 1

        if self.comment.progress.is_in_progress:
            return 2

        return 1

    @property
    def background_color(self):
        if self.comment.estimate.has_errors:
            return self.scheme.node_background_color(1)

        if self.comment.progress.is_done:
            return self.scheme.node_background_color(2)

        if self.comment.progress.is_almost_done:
            return self.scheme.node_background_color(1)

        return self.scheme.node_background_color(0)

    @property
    def header(self):
        file_name = self.font_primary(self.fit_escape_string(self.comment_presenter.file_value, splitter='/'))
        header = self.font_primary(self.fit_escape_string(self.comment_presenter.header) + '<br/><br/>' + file_name)
        return f'<tr><td {self.TD_ATTRS} colspan="2">{header}</td></tr>'

    @property
    def time_progress(self):
        time = f'<td {self.TD_ATTRS}>{self.font_secondary(self.comment_presenter.estimate.time)}</td>'
        progress = f'<td {self.TD_ATTRS}>{self.font_secondary(self.comment_presenter.progress.label_value)}</td>'
        return f'<tr>{time}{progress}</tr>'

    @property
    def developer_name(self):
        if not self.comment_presenter.developer_name:
            return ''

        developer_name = self.font_secondary(self.fit_escape_string(self.comment_presenter.developer_name))
        return f'<tr><td {self.TD_ATTRS} colspan="2">{developer_name}</td></tr>'

    @property
    def blocker(self):
        if not self.comment_presenter.blocker:
            return ''

        blocker = self.font_error(self.fit_escape_string(self.comment_presenter.blocker))
        return f'<tr><td {self.TD_ATTRS} colspan="2">{blocker}</td></tr>'

    @property
    def blocked(self):
        if not self.comment_presenter.blocked or self.comment_presenter.blocker:
            return ''

        blocked = self.font_error(self.fit_escape_string(self.comment_presenter.blocked))
        return f'<tr><td {self.TD_ATTRS} colspan="2">{blocked}</td></tr>'

    @property
    def errors(self):
        errors = ''
        for error in self.comment_presenter.errors:
            errors += f'<tr><td {self.TD_ATTRS} colspan="2">{self.font_error(self.fit_escape_string(error))}</td></tr>'

        for error in self.comment_presenter.estimate.errors:
            errors += f'<tr><td {self.TD_ATTRS} colspan="2">{self.font_error(self.fit_escape_string(error))}</td></tr>'

        for error in self.comment_presenter.progress.errors:
            errors += f'<tr><td {self.TD_ATTRS} colspan="2">{self.font_error(self.fit_escape_string(error))}</td></tr>'

        for error in self.comment_presenter.graph_errors:
            errors += f'<tr><td {self.TD_ATTRS} colspan="2">{self.font_error(self.fit_escape_string(error))}</td></tr>'

        return errors

    @property
    def label(self):
        content = f'''
            <table
                border="0"
                cellspacing="5"
                cellpadding="5"
                cellborder="{self.border_width}"
                color="{self.border_color}"
                bgcolor="{self.background_color}"
            >
                {self.header}
                {self.time_progress}
                {self.developer_name}
                {self.blocker}
                {self.blocked}
                {self.errors}
            </table>'''

        return content

    @property
    def content(self):
        return f'"{self.comment.id}" [label=<{self.label}>]\n'
