import unittest
from comment import Comment
from comment import CommentParseException
from comments_graph import CommentsGraph
from comments_graph import CommentsUniqIdException
from comments_graph import UnknownDependencyException
from dot_builder import DotBuilder

class CommentsTest(unittest.TestCase):
    def test_add_comment(self):
        comment_1 = Comment()
        comment_2 = Comment()
        comment_3 = Comment()
        comments = CommentsGraph()

        src_lines_1 = [
            {'num': 2, 'line': '%% I id1'},
            {'num': 3, 'line': '%% H H1'},
            {'num': 4, 'line': '%% D id2'},
            {'num': 5, 'line': '%% D id3'},
        ]

        src_lines_2 = [
            {'num': 1, 'line': '%% I id2'},
            {'num': 2, 'line': '%% H H2'},
        ]

        src_lines_3 = [
            {'num': 1, 'line': '%% I id3'},
            {'num': 2, 'line': '%% H H3'},
        ]

        comment_1.parse('file.name', src_lines_1)
        comment_2.parse('file.name', src_lines_2)
        comment_3.parse('file.name', src_lines_3)

        comments.add_comment(comment_1)
        comments.add_comment(comment_2)
        comments.add_comment(comment_3)

        self.assertEqual(len(comments.comments), 3)

    def test_validate_id_uniq(self):
        comment_1 = Comment()
        comment_2 = Comment()
        comments = CommentsGraph()

        src_lines_1 = [
            {'num': 2, 'line': '%% I id'},
            {'num': 3, 'line': '%% H H'},
        ]

        src_lines_2 = [
            {'num': 2, 'line': '%% I id'},
            {'num': 3, 'line': '%% H H'},
        ]

        comment_1.parse('file.name', src_lines_1)
        comment_2.parse('file.name', src_lines_2)

        comments.add_comment(comment_1)
        comments.add_comment(comment_2)

        try:
            comments.validate()
        except CommentsUniqIdException as error:
            self.assertEqual(error.comment1.id, 'id')
            self.assertEqual(error.comment2.id, 'id')

    def test_validate_deps(self):
        comment_1 = Comment()
        comment_2 = Comment()
        comments = CommentsGraph()

        src_lines_1 = [
            {'num': 2, 'line': '%% I id1'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D unknown'},
        ]

        src_lines_2 = [
            {'num': 2, 'line': '%% I id2'},
            {'num': 3, 'line': '%% H H'},
        ]

        comment_1.parse('file.name', src_lines_1)
        comment_2.parse('file.name', src_lines_2)

        comments.add_comment(comment_1)
        comments.add_comment(comment_2)

        try:
            comments.validate()
        except UnknownDependencyException as error:
            self.assertEqual(error.dependency, 'unknown')
            self.assertEqual(error.comment.id, 'id1')

    def test_build_graph(self):
        comment_1 = Comment()
        comment_2 = Comment()
        comment_3 = Comment()
        comment_4 = Comment()
        comments = CommentsGraph()

        src_lines_1 = [
            {'num': 2, 'line': '%% I id1'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id2'},
            {'num': 5, 'line': '%% D id3'},
        ]

        src_lines_2 = [
            {'num': 2, 'line': '%% I id2'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id4'},
        ]

        src_lines_3 = [
            {'num': 2, 'line': '%% I id3'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id4'},
        ]

        src_lines_4 = [
            {'num': 2, 'line': '%% I id4'},
            {'num': 3, 'line': '%% H H'},
        ]

        comment_1.parse('file.name', src_lines_1)
        comment_2.parse('file.name', src_lines_2)
        comment_3.parse('file.name', src_lines_3)
        comment_4.parse('file.name', src_lines_4)

        comments.add_comment(comment_1)
        comments.add_comment(comment_2)
        comments.add_comment(comment_3)
        comments.add_comment(comment_4)

        comments.validate()
        comments.build_graph()

        o1 = comments.outgoing('id1')
        self.assertEqual(len(o1), 2)
        self.assertEqual(o1[0].id, 'id2')
        self.assertEqual(o1[1].id, 'id3')

        i1 = comments.incoming('id1')
        self.assertEqual(len(i1), 0)

        o4 = comments.outgoing('id4')
        self.assertEqual(len(o4), 0)

        i4 = comments.incoming('id4')
        self.assertEqual(len(i4), 2)
        self.assertEqual(i4[0].id, 'id2')
        self.assertEqual(i4[1].id, 'id3')

    def test_topological_sort(self):
        comment_1 = Comment()
        comment_2 = Comment()
        comment_3 = Comment()
        comment_4 = Comment()
        comments = CommentsGraph()

        src_lines_1 = [
            {'num': 2, 'line': '%% I id1'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id2'},
            {'num': 5, 'line': '%% D id3'},
        ]

        src_lines_2 = [
            {'num': 2, 'line': '%% I id2'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id4'},
        ]

        src_lines_3 = [
            {'num': 2, 'line': '%% I id3'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id4'},
        ]

        src_lines_4 = [
            {'num': 2, 'line': '%% I id4'},
            {'num': 3, 'line': '%% H H'},
        ]

        comment_1.parse('file.name', src_lines_1)
        comment_2.parse('file.name', src_lines_2)
        comment_3.parse('file.name', src_lines_3)
        comment_4.parse('file.name', src_lines_4)

        comments.add_comment(comment_1)
        comments.add_comment(comment_3)
        comments.add_comment(comment_4)
        comments.add_comment(comment_2)

        comments.validate()
        comments.build_graph()
        
        # builder = DotBuilder(comments, 'title')
        # builder.build()

        self.assertEqual(comments.topological_sort(), ['id4', 'id3', 'id2', 'id1'])

    def test_independent_comment_ids(self):
        comment_1 = Comment()
        comment_2 = Comment()
        comment_3 = Comment()
        comment_4 = Comment()
        comment_5 = Comment()
        comment_6 = Comment()
        comments = CommentsGraph()

        src_lines_1 = [
            {'num': 2, 'line': '%% I id1'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id2'},
            {'num': 5, 'line': '%% D id3'},
        ]

        src_lines_2 = [
            {'num': 2, 'line': '%% I id2'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id4'},
        ]

        src_lines_3 = [
            {'num': 2, 'line': '%% I id3'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id4'},
        ]

        src_lines_4 = [
            {'num': 2, 'line': '%% I id4'},
            {'num': 3, 'line': '%% H H'},
        ]

        src_lines_5 = [
            {'num': 2, 'line': '%% I id5'},
            {'num': 3, 'line': '%% D id6'},
            {'num': 4, 'line': '%% H H'},
        ]

        src_lines_6 = [
            {'num': 2, 'line': '%% I id6'},
            {'num': 3, 'line': '%% H H'},
        ]

        comment_1.parse('file.name', src_lines_1)
        comment_2.parse('file.name', src_lines_2)
        comment_3.parse('file.name', src_lines_3)
        comment_4.parse('file.name', src_lines_4)
        comment_5.parse('file.name', src_lines_5)
        comment_6.parse('file.name', src_lines_6)

        comments.add_comment(comment_1)
        comments.add_comment(comment_3)
        comments.add_comment(comment_4)
        comments.add_comment(comment_2)
        comments.add_comment(comment_5)
        comments.add_comment(comment_6)

        comments.validate()
        comments.build_graph()
        
        builder = DotBuilder(comments, 'title')
        builder.build('dfs.dot')

        self.assertEqual(2, len(comments.independent_comment_ids()))
        self.assertIn('id4', comments.independent_comment_ids())
        self.assertIn('id6', comments.independent_comment_ids())

    def test_independent_dfs(self):
        comment_1 = Comment()
        comment_2 = Comment()
        comment_3 = Comment()
        comment_4 = Comment()
        comment_5 = Comment()
        comment_6 = Comment()
        comments = CommentsGraph()

        src_lines_1 = [
            {'num': 2, 'line': '%% I id1'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id2'},
            {'num': 5, 'line': '%% D id3'},
        ]

        src_lines_2 = [
            {'num': 2, 'line': '%% I id2'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id4'},
        ]

        src_lines_3 = [
            {'num': 2, 'line': '%% I id3'},
            {'num': 3, 'line': '%% H H'},
            {'num': 4, 'line': '%% D id4'},
        ]

        src_lines_4 = [
            {'num': 2, 'line': '%% I id4'},
            {'num': 3, 'line': '%% H H'},
        ]

        src_lines_5 = [
            {'num': 2, 'line': '%% I id5'},
            {'num': 3, 'line': '%% D id6'},
            {'num': 4, 'line': '%% H H'},
        ]

        src_lines_6 = [
            {'num': 2, 'line': '%% I id6'},
            {'num': 3, 'line': '%% H H'},
        ]

        comment_1.parse('file.name', src_lines_1)
        comment_2.parse('file.name', src_lines_2)
        comment_3.parse('file.name', src_lines_3)
        comment_4.parse('file.name', src_lines_4)
        comment_5.parse('file.name', src_lines_5)
        comment_6.parse('file.name', src_lines_6)

        comments.add_comment(comment_1)
        comments.add_comment(comment_3)
        comments.add_comment(comment_4)
        comments.add_comment(comment_2)
        comments.add_comment(comment_5)
        comments.add_comment(comment_6)

        comments.validate()
        comments.build_graph()
        
        builder = DotBuilder(comments, 'title')
        builder.build('dfs.dot')

        callback = lambda comment, level: print(comment.id, level)

        for id in comments.independent_comment_ids(reverse = False):
            print('---')
            comments.dfs(id, callback)
            pass

        # self.assertEqual(2, len(comments.independent_comment_ids()))
        # self.assertIn('id4', comments.independent_comment_ids())
        # self.assertIn('id6', comments.independent_comment_ids())

if __name__ == '__main__':
    unittest.main()
