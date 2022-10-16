import re

class PlainCommentParseException(Exception):
    def __init__(self, message, comment):
        self.message = message
        self.src_line = comment

class PlainComment:
    def __init__(self):
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

        r = re.compile('.*TODO:\s{1,}PL:(.*\s)(\d{1,}(\.\d{1,})?/\d{1,3}/\d{1,})(\s|$).*')
        match = r.match(src_line['line'])
        
        if match:
            self.description = match.group(1).strip()

            params = match.group(2).split('/')
            self.time = float(params[0])
            self.completeness = int(params[1])
            self.order = int(params[2])
        else:
            raise PlainCommentParseException('Wrong format. Expected format: "TODO: PL: comment description 1.5/10/50"', self)

    def print(self):
        print(self.inspect())

    def inspect(self):
        return f'{self.file_name}:{self.src_line_num} {self.description} (Time: {self.time}, completeness: {self.completeness}, order: {self.order})'

    def time_complete(self):
        return self.time * self.completeness / 100
    