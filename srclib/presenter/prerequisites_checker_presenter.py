# encoding: utf-8

from srclib.model.prerequisites_checker import PrerequisitesChecker
from srclib.utils import setup_i18n

_ = setup_i18n('..', 'messages')


class PrerequisitesCheckerPresenter():
    def __init__(self, prerequisites_checker):
        self.checker = prerequisites_checker

    @property
    def errors(self):
        errors = []

        for error in self.checker.errors:
            if error == PrerequisitesChecker.ERROR_NOT_DIRECTORY:
                errors.append(_("'{path}' IS NOT DIRECTORY").format(path=self.checker.out_dir))
            elif error == PrerequisitesChecker.ERROR_GIT_NOT_FOUND:
                errors.append(_("GIT NOT FOUND"))
            elif error == PrerequisitesChecker.ERROR_DOT_NOT_FOUND:
                errors.append(_("DOT NOT FOUND"))

        return errors
