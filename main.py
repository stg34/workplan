from file_list import FileList
from file_list import FileListError
from file_scanner import FileScanner
from comment import Comment
from comment import CommentParseException
from comments_graph import CommentsGraph
from comments_graph import CommentsUniqIdException
from comments_graph import UnknownDependencyException
from dot_builder import DotBuilder
from markdown_builder import MarkdownBuilder

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_comment_definitions(comments_graph):
    print('\ncomment definitions:')
    for comment in comments_graph.comments:
        print(f'  {comment.file_name}:{comment.src_line_num}')

def wrap_error(text):
    return Color.FAIL + text + Color.ENDC

def wrap_warning(text):
    return Color.WARNING + text + Color.ENDC

if __name__ == '__main__':
    try:
        file_list = FileList()
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

    scanner = FileScanner()
    comments_graph = CommentsGraph()

    for file_name in file_names:
        try: 
            scanner.scan_file(file_name)
        except Exception as error:
            print(wrap_warning('Scan file error: %s' % file_name))
            continue

        for src_comment in scanner.comments:
            try:
                comment = Comment()
                comment.parse(file_name, src_comment)
                comment.validate()
                comments_graph.add_comment(comment)

            except CommentParseException as error:
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

    try:
        comments_graph.validate()
        comments_graph.build_graph()

    except CommentsUniqIdException as error:
        print(wrap_error('=' * 80))
        print(wrap_error('Not unique id: "%s"' % error.comment1.id))
        print()
        print(wrap_error(error.comment1.inspect()))
        print(wrap_error(error.comment2.inspect()))
        print(wrap_error('=' * 80))
        exit(1)

    except UnknownDependencyException as error:
        print(wrap_error('=' * 80))
        print(wrap_error('Unknown dependency id: %s' % error.dependency))
        print()
        print(wrap_error(error.comment.inspect()))
        print(wrap_error('=' * 80))
        exit(1)

    print_comment_definitions(comments_graph)

    dot_builder = DotBuilder(comments_graph, 'title')
    dot_builder.build()

    markdown_builder = MarkdownBuilder(comments_graph, 'title')
    markdown_builder.build()
    markdown_builder.build_plain()
    markdown_builder.build_tree()
