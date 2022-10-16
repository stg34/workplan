import unittest
from dot_builder import DotBuilder
from comments_graph import CommentsGraph

class DotBuilderTest(unittest.TestCase):
    def test_parse_file_01(self):
        
        comments_graph = CommentsGraph()
        builder = DotBuilder(comments_graph, 'title')
        str = builder.fit_string('aaaaa dddddd bbbbbbb qqqqq wwwwwwww eeeeeeee rrrrrrrrr tttttt pppppp ooooooo iiiiiiii uuuuuuuu yyyyyyyy')
        print(str)

if __name__ == '__main__':
    unittest.main()
