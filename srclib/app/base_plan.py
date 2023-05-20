# encoding: utf-8

class PlanException(Exception):
    ...


class AppBasePlain():
    SUCCESS = 0
    FAIL = 1

    def __init__(self, arguments, prerequisites_checker, file_list, scanner):
        self.file_names = []
        self.comments = []
        self.args = arguments
        self.prerequisites_checker = prerequisites_checker
        self.file_list = file_list
        self.scanner = scanner

    def check_prerequisites(self):
        self.prerequisites_checker.check()
        if self.prerequisites_checker.has_errors:
            raise PlanException()

    def list_files(self):
        if self.args.src:
            self.file_names = [self.args.src]
            return

        self.file_list.list(exclude_ext=self.args.excluded_extensions)

        if self.file_list.has_errors:
            raise PlanException()

        self.file_names = self.file_list.file_names

    def scan_files(self):
        self.scanner.scan_files(self.file_names)
