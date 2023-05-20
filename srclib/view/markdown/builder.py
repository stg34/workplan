# encoding: utf-8

import pathlib
from srclib.model.comment import Comment
from srclib.presenter.task_presenter import TaskPresenter
from srclib.presenter.graph_presenter import GraphPresenter
from srclib.presenter.comment_presenter import GraphCommentPresenter

# https://github.github.com/gfm/#what-is-github-flavored-markdown-

class ViewMarkdownBuilder:
    def __init__(self, task, work_hours, h_start_level, debug=False):
        self.work_hours = work_hours
        self.h_start_level = h_start_level
        self.comments_graph = task.graph
        self.debug = debug
        self.content = ''
        self.task_presenter = TaskPresenter(task)
        self.graph_presenter = GraphPresenter(task.graph)

    def h_tag(self, level):
        level += self.h_start_level - 1
        level = min(level, 6)

        h = '#' * level
        return h

    def build_comment(self, comment, level):
        if comment.is_main:
            return

        indent_str = '  ' * level

        if comment.progress.is_done:
            strike_open = ' ~~'
            strike_close = '~~ '
        else:
            strike_open = ''
            strike_close = ''

        comment_presenter = GraphCommentPresenter(comment)

        content = ''
        content += f'{indent_str}{self.h_tag(level + 2)} {strike_open}{comment_presenter.header}{strike_close}\n'
        content += f'{indent_str}- {strike_open}{comment_presenter.file}{strike_close}\n'
        content += f'{indent_str}- {strike_open}{comment_presenter.estimate.time}{strike_close}\n'
        content += f'{indent_str}- {strike_open}{comment_presenter.progress.label_value}{strike_close} \n'

        self.cb_content += content

    def tree_callback(self, comment, _parent, level, path):
        if not comment.is_main and Comment.ID_MAIN not in path:
            level += 1

        self.build_comment(comment, level - 1)

    def build_summary(self):
        content = f'**{self.task_presenter.estimate.time}**\n\n'
        content += f'**{self.task_presenter.remaining_estimate.remaining_time}**\n\n'
        content += f'**{self.task_presenter.progress.label_value}**\n\n'
        content += f'{self.task_presenter.built_at}\n\n'

        if self.graph_presenter.errors:
            content += f'{self.h_tag(self.h_start_level + 1)} Errors\n'

            for error in self.graph_presenter.errors:
                content += f'- {error}\n'

            content += '\nSee console or diagram for details\n\n'  # TODO: i18n

        return content

    def build(self):
        self.cb_content = ''
        self.content = '\n'
        self.content += f'{self.h_tag(1)} {self.task_presenter.title}\n\n'

        self.content += self.build_summary()

        self.comments_graph.walk_through_tree(self.tree_callback)
        self.content += self.cb_content
        self.content += '\n'

    def write(self, file_name):
        pathlib.Path(file_name).write_text(self.content)

        return file_name  # TODO: check write file errors
