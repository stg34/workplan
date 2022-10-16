from file_list import FileList
from file_list import FileListError
from plain_scanner import PlainScanner
from plain_comment import PlainComment
from plain_comment import PlainCommentParseException
from markdown_builder import MarkdownBuilder

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

def wrap_error(text):
    return Color.FAIL + text + Color.ENDC

def wrap_warning(text):
    return Color.WARNING + text + Color.ENDC

def main():
    try:
        file_list = FileList('main')
        file_names = file_list.list()

    except FileListError as error:
        print(wrap_error('=' * 80))
        print(wrap_error('Execute command error. Command: '))
        print(wrap_error(error.command))
        print()
        print(wrap_error('Error:'))
        print(wrap_error(error.error))
        print()
        print(wrap_error('=' * 80))

    scanner = PlainScanner()
    comments = []

    for file_name in file_names:
        try: 
            scanner.scan_file(file_name)
        except Exception as error:
            print(wrap_warning('Scan file error: %s' % file_name))
            continue

        for src_comment in scanner.comments:
            print(src_comment)
            try:
                comment = PlainComment()
                comment.parse(file_name, src_comment)
                print(comment.inspect())
                comments.append(comment)

            except PlainCommentParseException as error:
                print(wrap_error('=' * 80))
                print(wrap_error('Parse comment error: %s' % error.message))
                print()
                print(wrap_error(comment.inspect()))
                print(wrap_error('=' * 80))
                exit(1)

            except Exception as error:
                print(wrap_error('=' * 80))
                print(wrap_error('Unexpected error: %s' % error))
                print(wrap_error(comment.inspect()))
                print(wrap_error('=' * 80))
                exit(1)

    # markdown_builder = MarkdownBuilder(comments, 'title')
    # markdown_builder.build()

if __name__ == '__main__':
    main()
