# encoding: utf-8

from srclib.view.dot.base_node import ViewDotBaseNode
from srclib.presenter.task_presenter import TaskPresenter
from srclib.presenter.graph_presenter import GraphPresenter


class ViewDotTitle(ViewDotBaseNode):
    def __init__(self, task, scheme):
        self.comments_graph = task.graph
        self.task_presenter = TaskPresenter(task)
        self.graph_presenter = GraphPresenter(task.graph)
        self.scheme = scheme

    def background_color(self):
        return self.scheme.node_background_color(2)

    def wrap_font(self, row):
        font_size = self.scheme.node_main_font_size
        primary_color = self.scheme.font_color_1(0)
        secondary_color = self.scheme.font_color_2(0)

        return [
            self.font_tag(row[0], font_size, primary_color),
            self.font_tag(row[1], font_size, secondary_color),
            self.font_tag(row[2], font_size, secondary_color),
            self.font_tag(row[3], font_size, secondary_color),
            self.font_tag(row[4], font_size, secondary_color),
            self.font_tag(row[5], font_size, secondary_color),
            self.font_tag(row[6], font_size, secondary_color)
        ]

    @property
    def comment(self):
        return self.comments_graph.main_comment

    @property
    def details_data(self):
        primary_color = self.scheme.font_color_1(0)
        font_size = self.scheme.node_main_font_size

        left = [self.wrap_font([
            self.task_presenter.total_label,
            self.task_presenter.estimate.time_label,
            self.task_presenter.estimate.time_value,
            self.task_presenter.remaining_estimate.remaining_time_label,
            self.task_presenter.remaining_estimate.time_value,
            self.task_presenter.progress.label,
            self.task_presenter.progress.value,
        ])]

        for developer in self.task_presenter.developers:
            row = self.wrap_font([
                developer.name,
                developer.estimate.time_label,
                developer.estimate.time_value,
                developer.remaining_estimate.remaining_time_label,
                developer.remaining_estimate.time_value,
                developer.progress.label,
                developer.progress.value,
            ])

            left.append(row)

        right = [
            [self.font_tag(self.task_presenter.built_at, font_size, primary_color)],
        ]

        if self.comment:
            file_name = self.fit_escape_string(self.comment.def_position, splitter='/')
            right.append([self.font_tag(file_name, font_size, primary_color)])

        if self.task_presenter.work_hours:
            right.append([self.font_tag(self.task_presenter.work_hours, font_size, primary_color)])

        return self.merge_table_data(left, right)

    def align_data(self, list, padding, size):
        return list + [padding] * (size - len(list))

    def merge_table_data(self, left, right):
        n = max(len(left), len(right))

        if len(left) < len(right):
            left = self.align_data(left, [' '] * len(left[0]), n)
        else:
            right = self.align_data(right, [' '] * len(right[0]), n)

        result = []
        for i in range(n):
            result.append(left[i] + right[i])

        return result

    @property
    def details_table(self):
        content = '<table border="0" cellborder="0" cellpadding="2" cellspacing="0" color="red">\n'

        for data in self.details_data:
            content += '<tr>\n'

            # Row Label
            content += f'<td align="left">{data[0]}</td>\n'

            # Time
            content += f'<td align="right">&nbsp;&nbsp;{data[1]}</td>\n'
            content += f'<td align="left">&nbsp;{data[2]}&nbsp;&nbsp;</td>\n'

            # Remaining time
            content += f'<td align="right">&nbsp;&nbsp;{data[3]}</td>\n'
            content += f'<td align="left">&nbsp;{data[4]}&nbsp;&nbsp;</td>\n'

            # Progress
            content += f'<td align="right">&nbsp;&nbsp;{data[5]}</td>\n'
            content += f'<td align="left">&nbsp;{data[6]}&nbsp;&nbsp;</td>\n'

            # Spacer
            content += '<td align="right">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>\n'

            # Additional info
            content += f'<td align="right">{data[7]}</td>\n'
            content += '</tr>\n'

        content += '</table>'

        return content

    @property
    def errors_table(self):
        if len(self.graph_presenter.errors) == 0:
            return ''

        font_color = self.scheme.error_color_0
        font_size = self.scheme.node_main_font_size

        content = '<table border="0" cellborder="0" cellpadding="2" cellspacing="0" color="red">\n'

        for error in self.graph_presenter.errors:
            content += '<tr>\n'
            content += f'<td align="left">{self.font_tag(error, font_size, font_color)} </td>\n'
            content += '</tr>\n'

        content += '</table>'

        return content

    @property
    def label(self):
        font_size = self.scheme.graph_title_fontsize
        font_color = self.scheme.font_color_1(0)
        title = self.font_tag(self.fit_escape_string(self.task_presenter.title, width=100), font_size, font_color)

        content = f'''
            <table
                color="{self.scheme.font_color_1(0)}"
                bgcolor="{self.background_color()}"
                border="0"
                cellborder="0"
                cellspacing="5"
                cellpadding="3"
            >
                <tr><td balign="left" align="left">{title}</td></tr>
                <hr/>
                <tr><td balign="left" align="left">{self.details_table}</td></tr>
                <tr><td balign="left" align="left">{self.errors_table}</td></tr>
                <tr><td balign="left" align="left">&nbsp;</td></tr>
            </table>'''

        return content
