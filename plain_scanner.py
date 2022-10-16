class PlainScanner:
    def __init__(self):
        self.comments = []

    def scan_file(self, file_name):
        self.comments = []

        f = open(file_name, 'r', encoding = 'utf8')
        line_num = 0

        for line in f:
            line_num += 1
            if 'TODO: PL:' in line: self.comments.append({'num': line_num, 'line': line})

        f.close()
