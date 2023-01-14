import re

class PlainCommentParseException(Exception):
    def __init__(self, message, comment):
        self.message = message
        self.src_line = comment

class PlainComment:
    def __init__(self, scale, todo_suffix):
        self.scale = scale
        self.todo_suffix = todo_suffix
        self.description = ''
        self.time = None
        self.completeness = 0
        self.order = 0
        self.src_line = None
        self.file_name = None
        self.src_line_num = None

    def parse(self, file_name, src_line):
        self.file_name = file_name
        self.src_line = src_line
        self.src_line_num = src_line['num']

        r = re.compile('.*TODO:\s{1,}%s:(.*\s)(\d{1,}(\.\d{1,})?/\d{1,3}/\d{1,})(\s|$).*' % self.todo_suffix)
        match = r.match(src_line['line'])

        if match:
            self.description = match.group(1).strip()

            params = match.group(2).split('/')
            self.time = float(params[0]) * self.scale
            self.completeness = int(params[1])
            self.order = int(params[2])
        else:
            error = f'Wrong format. Expected format: "TODO: {self.todo_suffix}: comment description 1.5/10/50"\n'
            error += src_line['line']
            error += f"\n{file_name}:{src_line['num']}"
            raise PlainCommentParseException(error, self)

    def print(self):
        print(self.inspect())

    def inspect(self):
        return f'{self.file_name}:{self.src_line_num} {self.description} (Time: {self.time}, completeness: {self.completeness}, order: {self.order})'

    def time_complete(self):
        return self.time * self.completeness / 100

    def time_remaining(self):
        return self.time - self.time_complete(self)
