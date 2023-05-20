# encoding: utf-8

import shutil
from pathlib import Path


class PrerequisitesChecker():
    ERROR_NOT_DIRECTORY = 'NOT_DIRECTORY'
    ERROR_GIT_NOT_FOUND = 'GIT_NOT_FOUND'
    ERROR_DOT_NOT_FOUND = 'DOT_NOT_FOUND'

    def __init__(self, out_dir, git_path, dot_path):
        self.out_dir = out_dir
        self.git_path = git_path
        self.dot_path = dot_path
        self.errors = []

    @property
    def has_errors(self):
        return bool(self.errors)

    def check(self):
        if self.out_dir and not Path(self.out_dir).is_dir():
            self.errors.append(self.ERROR_NOT_DIRECTORY)

        if self.git_path and not shutil.which(self.git_path):
            self.errors.append(self.ERROR_GIT_NOT_FOUND)

        if self.dot_path and not shutil.which(self.dot_path):
            self.errors.append(self.ERROR_DOT_NOT_FOUND)
