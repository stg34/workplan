# encoding: utf-8

from pathlib import Path
import re


class PlainScanner:
    def __init__(self, todo_suffix):
        self.src_comments = []
        self.todo_suffix = todo_suffix
        self.files_with_errors = []

    @property
    def has_errors(self):
        return bool(self.files_with_errors)

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

    def parse(self, file_name, line_num, src_line):
        src_comment = {
            'src': [{'num': line_num, 'line': src_line}],
            'file_name': file_name,
            'line_num': line_num,
            'id': [f'{file_name}:{line_num}'],
            'header': [],
            'dependencies': [],
            'estimate': [],
            'progress': [],
            'developer_name': [],
            'blocker': [],
            'order': None,
        }

        line = self.extract_value(src_line, f'TODO: {self.todo_suffix}:')

        r = re.compile(r'(.*\s)(\d{1,}(\.\d{1,})?/\d{1,3}/\d{1,})(\s|$).*')
        match = r.match(line)

        if match:
            src_comment['header'] = [match.group(1).strip()]
            params = match.group(2).split('/')

            src_comment['estimate'] = [params[0]]
            src_comment['progress'] = [params[1]]
            src_comment['order'] = params[2]
        else:
            src_comment['header'] = [self.extract_value(src_line, f'TODO: {self.todo_suffix}:')]

        return src_comment

    def scan_file(self, file_name):
        line_num = 0

        try:
            with Path(file_name).open(encoding='utf8') as file:
                for line in file:
                    line_num += 1

                    if f'TODO: {self.todo_suffix}:' in line:
                        self.src_comments.append(self.parse(file_name, line_num, line))

        except (UnicodeDecodeError, FileNotFoundError) as error:
            self.files_with_errors.append({'file_name': file_name, 'error': error})

    def scan_files(self, file_names):
        self.src_comments = []

        for file_name in file_names:
            self.scan_file(file_name)
