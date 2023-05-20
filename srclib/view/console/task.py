# encoding: utf-8

from srclib.presenter.comment_presenter import GraphCommentPresenter
from srclib.presenter.graph_presenter import GraphPresenter
from srclib.utils import print_error


class ViewConsoleTask():
    def __init__(self, task) -> None:
        self.task = task

    def print_errors(self):
        self.print_task_errors()
        self.print_loops_error()

    def print_task_errors(self):
        for comment in self.task.comments:
            presenter = GraphCommentPresenter(comment)
            if presenter.all_errors:
                error_text = presenter.inspect()
                error_text += '\n'
                for error in presenter.all_errors:
                    error_text += '\n'
                    error_text += error

                print_error(error_text)

        self.graph_presenter = GraphPresenter(self.task.graph)

        if self.graph_presenter.errors:
            graph = self.task.graph

            if not graph.semantic_comments:
                print_error(self.graph_presenter.error_no_comments)

            if not graph.has_main_comment:
                print_error(self.graph_presenter.error_no_main_comment)

            self.print_loops_error()

    def print_loops_error(self):
        self.graph_presenter = GraphPresenter(self.task.graph)
        graph = self.task.graph

        for loop in graph.loops:
            loop_error = self.graph_presenter.error_loop + ':\n\n'

            for comment in loop:
                loop_error += f'  {comment.id}\n'

            loop_error += f'  {loop[0].id}'

            print_error(loop_error)
