# encoding: utf-8

from srclib.arguments.graph_arguments import GraphArguments
from srclib.model.prerequisites_checker import PrerequisitesChecker
from srclib.model.file_list import FileList
from srclib.model.graph_scanner import GraphScanner
from srclib.model.comment import Comment
from srclib.app.base_plan import AppBasePlain
from srclib.app.base_plan import PlanException
from srclib.view.dot.builder import ViewDotBuilder
from srclib.view.markdown.builder import ViewMarkdownBuilder
from srclib.view.console.graph_plan import ViewConsoleGraphPlan
from srclib.model.task import Task
from srclib.model.colorizer import Colorizer


class AppPlanGraph(AppBasePlain):
    def __init__(self, sys_args):
        arguments = GraphArguments(sys_args, '.plan.conf')
        prerequisites_checker = PrerequisitesChecker(arguments.out_dir, arguments.git_binary_path, arguments.dot_binary_path)
        file_list = FileList(arguments.base_branch, arguments.verbose)
        scanner = GraphScanner(arguments.todo_suffix)
        self.result = {
            'out_graph_file': None,
            'out_markdown_file': None
        }

        # TODO: PL: Создать экземпляр колоризатора, передать ему конфиг на вход
        # ID: srclib/app/graph_plan.py:27
        # DEP: srclib/model/colorizer.py:1
        # TIME: 0.1
        # COMPL: 100

        super().__init__(arguments, prerequisites_checker, file_list, scanner)

        self.colorizer = Colorizer(self.args.config)

        self.task = Task(self.args.work_hours)
        self.view = ViewConsoleGraphPlan(
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

    def build_task(self):
        self.task.build(self.comments)

    def build_dot(self):
        # TODO: PL: Передать во ViewDotBuilder экземпляр колоризатора
        # ID: srclib/app/graph_plan.py:54
        # DEP: srclib/app/graph_plan.py:27
        # TIME: 0.1
        # COMPL: 100

        self.dot_builder = ViewDotBuilder(self.task,
                                          self.args.reverse,
                                          self.args.dot_color_scheme,
                                          self.colorizer,
                                          self.args.graph_dir,
                                          self.args.verbose)

        self.dot_builder.build()
        out_graph_file = self.dot_builder.write(self.args.out_graph_path)
        self.result['out_graph_file'] = out_graph_file

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
            self.build_dot()
            self.build_markdown()

        except PlanException:
            return AppPlanGraph.FAIL

        finally:
            self.view.print_summary()

        return AppPlanGraph.SUCCESS
