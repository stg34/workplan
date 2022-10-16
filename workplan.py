import subprocess
import re

class Comments:
    comments = []

    def add(self, comment):
        self.comments.append(comment)
        return

class Comment:
    def __init__(self):
        self._id = None
        self._dependencies = []
        self._description = ''
        self._header = None
        self._time_min = None
        self._time_expected = None
        self._time_max = None
        self._completeness = None
        self._order = None

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header):
        self._header = header

    @property
    def dependencies(self):
        return self._dependencies

    def add_dependency(self, dep):
        self._dependencies.append(dep)
        return

    @property
    def description(self):
        return self._description

    def add_description(self, desc):
        self._description += desc

    def set_time(self, t):
        if len(t) == 1:
            self._time_expected = t[0]
        else:
            self._time_min = t[0]
            self._time_expected = t[1]
            self._time_max = t[2]

    @property
    def time_min(self):
        return self._time_min

    @property
    def time_expected(self):
        return self._time_expected

    @property
    def time_max(self):
        return self._time_max

    @property
    def completeness(self):
        return self._completeness

    @completeness.setter
    def completeness(self, completeness):
        self._completeness = completeness

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, order):
        self._order = order

class CommentSrc:

class FileScanner:
    def __init__(self, file_name):
        self.file_name = file_name
        self.comments = []
        self.comment = None

    def extract_comment_attr(self, line, attr):
        return line.split('%% %s ' % attr)[1].strip()

    def extract_time_attr(self, line):
        # %% T 1|2|3
        # %% T 1
        time_str = line.split('T')[-1]
        time_val = list(map(lambda t: int(t), time_str.split('|')))
        if len(time_val) != 1 and len(time_val) != 3:
            raise ValueError('Expected time format: "T 1" or "T 1|2|3"')

        return time_val

    def line_marker(self, line):
        if '%% I ' in line: return 'id'
        if '%% D ' in line: return 'dependency'
        if '%% H ' in line: return 'header'
        if '%% T ' in line: return 'time'
        if '%% C ' in line: return 'completeness'
        if '%% O ' in line: return 'order'

        return None

    def scan_line(self, line):
        return

    def scan_file(self, file_name):
        html_comment_opening = re.compile('.*<!--.*%%.*')
        html_comment_ending = re.compile('.*%%.*-->.*')
        orig_line = ''

        try:
            f = open(file_name, 'r', encoding = 'utf8')
            for line in f:
                orig_line = line
                if '%%+++++++' in line:
                    comment = Comment()
                    comments.append(comment)
                    continue

                if '%%-------' in line:
                    comment = None
                    continue

                if comment:
                    if '%%' not in line:
                        comment = None
                        continue

                    if html_comment_opening.match(line):
                        line = line.replace('<!--', '')

                    if html_comment_ending.match(line):
                        line = line.replace('-->', '')

                    marker = line_marker(line)

                    if marker == 'id':
                        comment.id = extract_comment_attr(line, 'I')
                        continue

                    if marker == 'dependency':
                        comment.add_dependency(extract_comment_attr(line, 'D'))
                        continue

                    if marker == 'header':
                        comment.header = extract_comment_attr(line, 'H')
                        continue

                    if marker == 'time':
                        comment.set_time(extract_time_attr(line))
                        continue

                    if marker == 'completeness':
                        comment.completeness = int(extract_comment_attr(line, 'C'))
                        continue

                    if marker == 'order':
                        comment.order = int(extract_comment_attr(line, 'O'))
                        continue

                    comment.add_description(line.split('%%')[-1].strip() + "\n")

            f.close()
        except BaseException as error:
            print('#'*80)
            print()
            print(orig_line)
            print('#'*80)
            raise error

        return comments

def file_list(cmd, verbose = True):
    res = subprocess.run([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF8")

#    print("The exit code: %d" % res.returncode)
    file_names = res.stdout.splitlines()

    if res.returncode != 0:
        if verbose:
            print(cmd)
            print(res.stdout)
        return []

    if verbose:
        print(cmd)
        print("\n".join(map(lambda f: '    ' + f, file_names)))
        print()

    return file_names

def files_to_scan():
    file_names = file_list("git ls-files --modified")
    file_names += file_list("git ls-files --others --exclude-standard")
    file_names += file_list("git diff --name-only")
    file_names = list(set(file_names))
    file_names.sort()

    return file_names



def scan_files(file_names):
    return []

if __name__ == '__main__':
    print(files_to_scan())
