# encoding: utf-8

from srclib.utils import setup_i18n

_ = setup_i18n('..', 'messages')


class FileListPresenter():
    def __init__(self, file_list):
        self.file_list = file_list

    @property
    def errors(self):
        errors = []

        for error in self.file_list.errors:
            errors.append(_('EXECUTE GIT ERROR {command} {error}').format(command=error.command, error=error.stderr))

        return errors
