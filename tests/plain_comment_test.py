import unittest
from plain_comment import PlainComment
from plain_comment import PlainCommentParseException

class PlainCommentTest(unittest.TestCase):
    def test_parse_01(self):
        comment = PlainComment()
        comment.parse('file.name', {'num': 2, 'line': '<!-- TODO: PL: descr 123 1.5/2/3 -->'})

        self.assertEqual(comment.file_name, 'file.name')
        self.assertEqual(comment.description, 'descr 123')
        self.assertEqual(comment.time, 1.5)
        self.assertEqual(comment.completeness, 2)
        self.assertEqual(comment.order, 3)

    def test_parse_02(self):
        comment = PlainComment()
        src_line = {'num': 2, 'line': 'TODO: PL: descr 123 '}

        self.assertRaises(PlainCommentParseException, comment.parse, 'file.name', src_line)

if __name__ == '__main__':
    unittest.main()
