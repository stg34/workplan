# encoding: utf-8

from srclib.view.console.prerequisites import ViewConsolePrerequisites
from srclib.view.console.file_list import ViewConsoleFileList
from srclib.view.console.scanner import ViewConsoleScanner
from srclib.view.console.task import ViewConsoleTask
from srclib.utils import print_success

from srclib.utils import setup_i18n

_ = setup_i18n('..', 'messages')


class ViewConsolePlainPlan():
    def __init__(self, arguments, prerequisites_checker, file_list, scanner, task, result) -> None:
        self.arguments = arguments
        self.prerequisites_checker = prerequisites_checker
        self.file_list = file_list
        self.scanner = scanner
        self.task = task
        self.result = result

        self.prerequisites_checker_view = ViewConsolePrerequisites(prerequisites_checker)
        self.file_list_view = ViewConsoleFileList(file_list)
        self.scanner_view = ViewConsoleScanner(arguments, scanner)
        self.task_view = ViewConsoleTask(self.task)

    def print_summary(self, suppress_error_no_main_comment=False):
        self.prerequisites_checker_view.print_errors()
        self.file_list_view.print_errors()
        self.scanner_view.print_errors()
        self.task_view.print_errors(suppress_error_no_main_comment)
        self.scanner_view.print_comment_positions()

        result = []
        if self.result['out_markdown_file']:
            result.append(_('MARKDOWN FILE: {file}').format(file=self.result["out_markdown_file"]))

        result = '\n'.join(result)
        if result:
            print_success(result)
