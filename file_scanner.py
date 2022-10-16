class FileScanner:
    def __init__(self):
        self.comments = []

    def add_line(self, line, line_num, comment):
        comment.append({'num': line_num, 'line': line})

    def scan_file(self, file_name):
        self.comments = []
        comment = None

        f = open(file_name, 'r', encoding = 'utf8')
        line_num = 0

        for line in f:
            line_num += 1

            if '%%+++++++' in line:
                comment = []
                self.add_line(line, line_num, comment)
            elif '%% ' in line and comment:
                self.add_line(line, line_num, comment)
            elif '%%-------' in line and comment:
                self.add_line(line, line_num, comment)
                self.comments.append(comment)
                comment = None
            elif '%%' not in line:
                if comment:
                    self.comments.append(comment)
                comment = None

        if comment:
            self.comments.append(comment)

        f.close()
