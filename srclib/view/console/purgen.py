# encoding: utf-8

from srclib.view.console.prerequisites import ViewConsolePrerequisites
from srclib.view.console.file_list import ViewConsoleFileList
from srclib.view.console.scanner import ViewConsoleScanner
# from srclib.utils import wrap_success
from srclib.utils import print_success

from srclib.utils import setup_i18n

_ = setup_i18n('..', 'messages')


class ViewConsolePurgen():
    def __init__(self, arguments, prerequisites_checker, file_list, scanner, result) -> None:
        self.arguments = arguments
        self.prerequisites_checker = prerequisites_checker
        self.file_list = file_list
        self.scanner = scanner
        self.result = result

        self.prerequisites_checker_view = ViewConsolePrerequisites(prerequisites_checker)
        self.file_list_view = ViewConsoleFileList(file_list)
        self.scanner_view = ViewConsoleScanner(arguments, scanner)

    def print_summary(self):
        self.prerequisites_checker_view.print_errors()
        self.file_list_view.print_errors()
        self.scanner_view.print_errors()

        result = []
        if self.result['out_patch_file']:
            result.append(_('PATCH FILE: {file}'.format(file=self.result["out_patch_file"])))

        result = '\n'.join(result)
        if result:
            print_success(result)
