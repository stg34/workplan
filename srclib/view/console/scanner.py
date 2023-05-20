# encoding: utf-8

from srclib.presenter.scanner_presenter import ScannerPresenter
from srclib.utils import print_warning


class ViewConsoleScanner():
    def __init__(self, args, scanner) -> None:
        self.args = args
        self.scanner = scanner

    def print_errors(self):
        if self.scanner.has_errors:
            presenter = ScannerPresenter(self.scanner, self.args.excluded_extensions)
            for error in presenter.errors:
                print_warning(error)

            if presenter.exclude_hint:
                print_warning(presenter.exclude_hint)
