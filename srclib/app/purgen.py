# encoding: utf-8

from srclib.arguments.purgen_arguments import PurgenArguments
from srclib.model.prerequisites_checker import PrerequisitesChecker
from srclib.model.file_list import FileList
from srclib.model.graph_scanner import GraphScanner
from srclib.view.console.purgen import ViewConsolePurgen
from collections import defaultdict
from srclib.utils import execute_command
from pathlib import Path
from srclib.app.base_plan import AppBasePlain
from tempfile import NamedTemporaryFile


class PlanException(Exception):
    ...


class AppPurgen(AppBasePlain):
    def __init__(self, sys_args):
        arguments = PurgenArguments(sys_args, '.plan.conf')
        prerequisites_checker = PrerequisitesChecker(arguments.out_dir, arguments.git_binary_path, None)
        file_list = FileList(arguments.base_branch, arguments.verbose)
        scanner = GraphScanner(arguments.todo_suffix)
        super().__init__(arguments, prerequisites_checker, file_list, scanner)
        self.result = {
            'out_patch_file': None,
        }

        self.view = ViewConsolePurgen(
            arguments,
            prerequisites_checker,
            file_list,
            scanner,
            self.result
        )

    def check_prerequisites(self):
        self.checker.check()
        if self.checker.has_errors:
            self.view.print_checker_presenter_errors()
            raise PlanException()

    def remove_comments(self, lines, blocks):
        lines_num = len(lines)

        # align lines numbering to zero
        blocks = [[line - 1 for line in block] for block in blocks]

        for block in blocks:
            if block[-1] < lines_num - 1 and not lines[block[-1] + 1].strip():
                block.append(block[-1] + 1)

        lines_to_delete = [n for block in blocks for n in block]

        new_lines = []
        line_num = 0

        for line in lines:
            if line_num not in lines_to_delete:
                new_lines.append(line)

            line_num += 1

        return new_lines

    def purge(self):
        self.list_files()
        self.scan_files()

        patch = []
        comment_lines_by_file = defaultdict(list)

        for src_comment in self.scanner.src_comments:
            comment_lines_by_file[src_comment['file_name']].append([src['num'] for src in src_comment['src']])

        for file_name in comment_lines_by_file:
            lines_to_delete = comment_lines_by_file[file_name]
            lines = self.remove_comments(list(Path(file_name).open()), lines_to_delete)
            content = ''.join(lines)

            with NamedTemporaryFile('w+t') as tf:
                tf.write(content)
                tf.flush()

                patch += execute_command(f'git -c core.quotepath=false diff --no-index "{tf.name}" "{file_name}"', False, True)

            self.write_file(file_name, content)

            patch = [line.replace(f'--- a{tf.name}', f'--- a/{file_name}') for line in patch]

        Path(self.args.out_patch_path).write_text('\n'.join(patch))
        self.result['out_patch_file'] = self.args.out_patch_path

        self.view.print_summary()

    def write_file(self, file_name, content):
        if not self.args.dry_run:
            Path(file_name).write_text(content)  # TODO: errors handling
