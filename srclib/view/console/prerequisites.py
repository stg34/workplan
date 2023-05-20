# encoding: utf-8

from srclib.presenter.prerequisites_checker_presenter import PrerequisitesCheckerPresenter
from srclib.utils import print_error


class ViewConsolePrerequisites():
    def __init__(self, prerequisites_checker) -> None:
        self.prerequisites_checker = prerequisites_checker

    def print_errors(self):
        checker_presenter = PrerequisitesCheckerPresenter(self.prerequisites_checker)
        for error in checker_presenter.errors:
            print_error(error)
