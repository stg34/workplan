# encoding: utf-8

import pathlib
from srclib.utils import execute_command
from srclib.utils import ExecuteCommandError


class FileList():
    def __init__(self, base_branch, verbose=False):
        self.base_branch = base_branch
        self.verbose = verbose
        self.file_names = []
        self.errors = []

    @property
    def has_errors(self):
        return bool(self.errors)

    def list(self, exclude_ext=None):
        exclude_ext = ['.' + ext for ext in exclude_ext or []]
        self.file_names = []

        try:
            self.file_names += execute_command("git -c core.quotepath=false ls-files --modified", self.verbose)
            self.file_names += execute_command("git -c core.quotepath=false ls-files --others --exclude-standard", self.verbose)
            self.file_names += execute_command(f"git -c core.quotepath=false diff --name-only --diff-filter=d --merge-base {self.base_branch}", self.verbose)
        except ExecuteCommandError as error:
            self.errors.append(error)

        self.file_names = list(set(self.file_names))
        self.file_names.sort()
        self.file_names = [n for n in self.file_names if pathlib.Path(n).suffix not in exclude_ext]
