class CommentParseException(Exception):
    def __init__(self, message, comment):
        self.message = message
        self.comment = comment

class Comment:
    def __init__(self):
        self.id = None
        self.dependencies = []
        self.description = ''
        self.header = None
        self.time_min = None
        self.time_expected = None
        self.time_max = None
        self.completeness = 0
        self.order = 0
        self.src_lines = []
        self.file_name = None
        self.src_line_num = None

    def clean_line(self, line):
        line = line.strip()
        idx = line.find('%%')
        if idx >= 0:
            line = line[idx + 2:]

        if line.endswith('-->'):
            line = line[:-3].strip()

        return line

    def parse_time_attr(self, time_str):
        time_val = list(map(lambda t: int(t), time_str.split('|')))

        if len(time_val) != 1 and len(time_val) != 3:
            raise CommentParseException('Expected time format: "T 1" or "T 1|2|3"')

        return time_val

    def parse(self, file_name, src_lines):
        self.file_name = file_name
        self.src_lines = src_lines
        self.src_line_num = src_lines[0]['num']

        for src_line in src_lines:
            line = src_line['line']
            idx = line.find('%%')
            line = line[idx + 2:].strip()

            if line.startswith('%%+++++++') or line.startswith('%%--------'):
                continue

            if line.startswith('I '):
                if self.id: raise CommentParseException('ID is already defined', self)
                self.id = line[2:].strip()

            if line.startswith('D '):
                self.dependencies.append(line[2:].strip())

            if line.startswith('H '):
                if self.header: raise CommentParseException('Header is already defined', self)
                self.header = line[2:].strip()

            if line.startswith('T '):
                if self.time_expected: raise CommentParseException('Time is already defined', self)
                t = self.parse_time_attr(line[2:].strip())

                if len(t) == 1:
                    self.time_expected = t[0]
                else:
                    self.time_min = t[0]
                    self.time_expected = t[1]
                    self.time_max = t[2]

            if line.startswith('C '):
                if self.completeness: raise CommentParseException('Completeness is already defined', self)
                self.completeness = int(line[2:].strip())

            if line.startswith('O '):
                if self.order: raise CommentParseException('Order is already defined', self)
                self.order = int(line[2:].strip())

    def validate(self):
        if not self.id: raise CommentParseException('ID is not defined', self)
        if not self.header: raise CommentParseException('Header is not defined', self)

    def print(self):
        print(self.inspect())

    def inspect(self):
        return self.file_name + '\n' + ''.join(map(lambda line: "%4s %s" % (line['num'], line['line']), self.src_lines))
#         return ''.join(map(lambda line: "%4s %s" % (line['num'], line['line']), self.src_lines))

    def time_complete(self):
        return self.time_expected * self.completeness / 100