import unittest
from comment import Comment
from comment import CommentParseException

class CommentTest(unittest.TestCase):
    def test_parse_01(self):
        comment = Comment()
        src_lines = [
            {'num': 1, 'line': '  # %%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'},
            {'num': 2, 'line': '  # %% I id'},
            {'num': 3, 'line': '  # %% D dep1'},
            {'num': 4, 'line': '  # %% D dep2'},
            {'num': 5, 'line': '  # %% H Header'},
            {'num': 6, 'line': '  # %% Description 1'},
            {'num': 7, 'line': '  # %% Description 2'},
            {'num': 8, 'line': '  # %% T 1|2|3'},
            {'num': 9, 'line': '  # %% C 5'},
            {'num': 10, 'line': '  # %% O 1'},
            {'num': 11, 'line': '  # %%-----------------------------------------------------------'}
        ]

        comment.parse('file.name', src_lines)

        self.assertEqual(comment.id, 'id')
        self.assertEqual(comment.dependencies, ['dep1', 'dep2'])
        self.assertEqual(comment.header, 'Header')
        self.assertEqual(comment.time_min, 1)
        self.assertEqual(comment.time_expected, 2)
        self.assertEqual(comment.time_max, 3)
        self.assertEqual(comment.completeness, 5)
        self.assertEqual(comment.order, 1)

    def test_parse_02(self):
        comment = Comment()
        src_lines = [
            {'num': 2, 'line': '  # %% I id'},
            {'num': 3, 'line': '  # %% I id'}
        ]

        self.assertRaises(CommentParseException, comment.parse, 'file.name', src_lines)

    def test_parse_03(self):
        comment = Comment()
        src_lines = [
            {'num': 2, 'line': '  # %% H header'},
            {'num': 3, 'line': '  # %% H header'}
        ]

        self.assertRaises(CommentParseException, comment.parse, 'file.name', src_lines)

    def test_parse_03(self):
        comment = Comment()
        src_lines = [
            {'num': 2, 'line': '  # %% T 1'},
            {'num': 3, 'line': '  # %% T 1'}
        ]

        self.assertRaises(CommentParseException, comment.parse, 'file.name', src_lines)

    def test_parse_03(self):
        comment = Comment()
        src_lines = [
            {'num': 2, 'line': '  # %% T 1'},
        ]

        comment.parse('file.name', src_lines)

        self.assertRaises(CommentParseException, comment.validate)

if __name__ == '__main__':
    unittest.main()

# assertRaises(exception, callable, *args, **kwds)
#
