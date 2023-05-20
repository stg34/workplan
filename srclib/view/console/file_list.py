# encoding: utf-8

from srclib.presenter.file_list_presenter import FileListPresenter
from srclib.utils import print_error


class ViewConsoleFileList():
    def __init__(self, file_list) -> None:
        self.file_list = file_list

    def print_errors(self):
        if self.file_list.has_errors:
            file_list_presenter = FileListPresenter(self.file_list)

            for error in file_list_presenter.errors:
                print_error(error)
