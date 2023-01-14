from srclib.file_list import FileList
from srclib.file_list import FileListError
from srclib.plain_scanner import PlainScanner
from srclib.plain_comment import PlainComment
from srclib.plain_comment import PlainCommentParseException
from srclib.plain_markdown import PlainMarkdown
from argparse import ArgumentParser
import configparser

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

def wrap_error(text):
    return Color.FAIL + text + Color.ENDC

def wrap_warning(text):
    return Color.WARNING + text + Color.ENDC

class PlainPlan():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('.planplain.conf')

        self.base_branch = config.get('MAIN', 'base-branch', fallback = 'master')
        self.outfile = config.get('MAIN', 'outfile', fallback = 'plan.md')
        self.verbose = config.getboolean('MAIN', 'verbose', fallback = False)
        self.unit = config.get('MAIN', 'unit', fallback = 'hours')
        self.scale = config.getfloat('MAIN', 'scale', fallback = 1)
        self.title = config.get('MAIN', 'title', fallback = FileList().branch_name())
        self.todo_suffix = config.get('MAIN', 'todo-suffix', fallback = 'PL')
        self.work_hours = config.getint('MAIN', 'work-hours', fallback = None)

        parser = ArgumentParser()
        parser.add_argument('-b', '--base-branch')
        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('-t', '--title')
        parser.add_argument('-s', '--scale', type=float)
        parser.add_argument('-f', '--todo-suffix')
        parser.add_argument('-w', '--work-hours', type=int)
        parser.add_argument('-u', '--unit', default = 'hour', choices=['sp', 'hour'])
        parser.add_argument('-o', '--outfile', default = 'plan.md')
        self.args = parser.parse_args()

        if self.args.base_branch: self.base_branch = self.args.base_branch
        if self.args.verbose: self.verbose = self.args.verbose
        if self.args.title: self.title = self.args.title
        if self.args.outfile: self.outfile = self.args.outfile
        if self.args.unit: self.unit = self.args.unit
        if self.args.scale: self.scale = self.args.scale
        if self.args.work_hours: self.work_hours = self.args.work_hours
        if self.args.todo_suffix: self.todo_suffix = self.args.todo_suffix

    def build(self):
        try:
            file_list = FileList()
            file_names = file_list.list(self.base_branch, self.verbose)
        except FileListError as error:
            print(wrap_error('=' * 80))
            print(wrap_error('Execute command error. Command: '))
            print(wrap_error(error.command))
            print()
            print(wrap_error('Error:'))
            print(wrap_error(error.error))
            print()
            print(wrap_error('=' * 80))
            exit(1)

        scanner = PlainScanner(self.todo_suffix)
        comments = []

        for file_name in file_names:
            try:
                scanner.scan_file(file_name)
            except Exception as error:
                print(wrap_warning('Scan file error: %s' % file_name))
                continue

            for src_comment in scanner.comments:
                try:
                    comment = PlainComment(self.scale, self.todo_suffix)
                    comment.parse(file_name, src_comment)
                    comments.append(comment)

                except PlainCommentParseException as error:
                    print(wrap_error('=' * 80))
                    print(wrap_error('Parse comment error: %s' % error.message))
                    print()
                    print(wrap_error(comment.inspect()))
                    print(wrap_error('=' * 80))
                    exit(1)

        comments.sort(key = lambda c : f'{c.file_name}:{c.src_line_num}')
        for comment in comments:
            print(f'{comment.file_name}:{comment.src_line_num}')

        comments.sort(key = lambda c : c.order)

        markdown_builder = PlainMarkdown(comments, self.title, self.unit, self.work_hours, self.verbose)
        md = markdown_builder.build()

        with open(self.outfile, 'w') as f:
            f.write(md)

if __name__ == '__main__':
    plan = PlainPlan()
    plan.build()
