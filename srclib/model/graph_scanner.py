# encoding: utf-8

import re
from pathlib import Path


class GraphScanner:
    def __init__(self, todo_suffix):
        self.src_comments = []
        self.todo_suffix = todo_suffix
        self.files_with_errors = []
        self.line_re = re.compile(r'\W*(ID:|DEP:|COMPL:|TIME:|DEV:|BLOCKER:)')

    @property
    def has_errors(self):
        return bool(self.files_with_errors)

    def add_comment(self, file_name, lines):
        self.src_comments.append(self.parse(file_name, lines))

    def clean_line(self, line):
        line = line.strip()

        if line.endswith('-->'):
            line = line[:-3].strip()

        if line.endswith('*/'):
            line = line[:-2].strip()

        return line

    def extract_value(self, line, marker):
        idx = line.find(marker)

        return self.clean_line(line[idx + len(marker):])

    def parse(self, file_name, src_lines):
        src_comment = {
            'src': src_lines,
            'file_name': file_name,
            'line_num': src_lines[0]['num'],
            'id': [],
            'header': [],
            'dependencies': [],
            'estimate': [],
            'progress': [],
            'developer_name': [],
            'blocker': [],
            'order': 0,
        }

        for src_line in src_lines:
            line = src_line['line']

            for marker in self.marker_map:
                if marker in line:
                    src_comment[self.marker_map[marker]].append(self.extract_value(line, marker))

        return src_comment

    def scan_file(self, file_name):
        lines = []
        line_num = 0

        try:
            with Path(file_name).open(encoding='utf8') as file:
                for line in file:
                    line_num += 1

                    if f'TODO: {self.todo_suffix}:' in line:
                        if len(lines):
                            self.add_comment(file_name, lines)
                            lines = []

                        lines.append({'num': line_num, 'line': line})
                        continue

                    if len(lines):
                        if self.line_re.match(line):
                            lines.append({'num': line_num, 'line': line})
                        else:
                            self.add_comment(file_name, lines)
                            lines = []

                if len(lines):
                    self.add_comment(file_name, lines)

        except (UnicodeDecodeError, FileNotFoundError) as error:
            self.files_with_errors.append({'file_name': file_name, 'error': error})

    def scan_files(self, file_names):
        self.src_comments = []

        for file_name in file_names:
            self.scan_file(file_name)

    @property
    def marker_map(self):
        return {
            f'TODO: {self.todo_suffix}:': 'header',
            'ID:': 'id',
            'DEP:': 'dependencies',
            'TIME:': 'estimate',
            'COMPL:': 'progress',
            'DEV:': 'developer_name',
            'BLOCKER:': 'blocker',
        }
