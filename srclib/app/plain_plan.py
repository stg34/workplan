# encoding: utf-8

from srclib.arguments.plain_arguments import PlainArguments
from srclib.model.prerequisites_checker import PrerequisitesChecker
from srclib.model.file_list import FileList
from srclib.model.plain_scanner import PlainScanner
from srclib.model.comment import Comment
from srclib.utils import branch_name
from srclib.app.base_plan import AppBasePlain
from srclib.app.base_plan import PlanException
from srclib.view.console.task import ViewConsoleTask
from srclib.view.console.plain_plan import ViewConsolePlainPlan
from srclib.view.markdown.builder import ViewMarkdownBuilder
from srclib.model.task import Task


class AppPlanPlain(AppBasePlain):
    def __init__(self, sys_args):
        arguments = PlainArguments(sys_args, '.plan.conf')
        prerequisites_checker = PrerequisitesChecker(arguments.out_dir, arguments.git_binary_path, None)
        file_list = FileList(arguments.base_branch, arguments.verbose)
        scanner = PlainScanner(arguments.todo_suffix)

        super().__init__(arguments, prerequisites_checker, file_list, scanner)
        self.task = Task(arguments.work_hours)
        self.result = {
            'out_graph_file': None,
            'out_markdown_file': None
        }

        self.view = ViewConsolePlainPlan(
            arguments,
            prerequisites_checker,
            file_list,
            scanner,
            self.task,
            self.result
        )

    def parse_comments(self):
        for src_comment in self.scanner.src_comments:
            comment = Comment.parse(src_comment, self.args.scale, self.args.work_hours)
            self.comments.append(comment)

    def document_title(self):
        if self.args.title:
            return self.args.title

        return branch_name()

    def build_main_comment(self, ordered_comments):
        src_comment = {
            'src': [{'num': 1, 'line': 'TODO: PL: Stub 1/1/1\n'}],
            'file_name': 'stub',
            'line_num': 1,
            'id': [Comment.ID_MAIN],
            'header': [self.document_title()],
            'dependencies': [d.id for d in ordered_comments],
            'estimate': ['1'],
            'progress': ['1'],
            'developer_name': [],
            'blocker': [],
            'order': 0,
        }

        return Comment.parse(src_comment, self.args.scale, self.args.work_hours)

    def build_task(self):
        ordered_comments = sorted(self.comments, key=lambda c: c.order)
        self.comments.append(self.build_main_comment(ordered_comments))
        self.task.build(self.comments)
        view = ViewConsoleTask(self.task)
        view.print_errors()

    def build_markdown(self):
        self.markdown = ViewMarkdownBuilder(self.task, self.args.work_hours, self.args.h_start_level)
        self.markdown.build()
        out_markdown_file = self.markdown.write(self.args.out_md_path)
        self.result['out_markdown_file'] = out_markdown_file

    def build(self):
        try:
            self.check_prerequisites()
            self.list_files()
            self.scan_files()
            self.parse_comments()
            self.build_task()
            self.build_markdown()

        except PlanException:
            return AppPlanPlain.FAIL

        finally:
            self.view.print_summary(suppress_error_no_main_comment=True)

        return AppPlanPlain.SUCCESS
