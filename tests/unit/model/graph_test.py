# encoding: utf-8

import unittest
from tests.unit.base_test_case import BaseTestCase


class GraphTest(BaseTestCase):
    def test_add_comment(self):
        src_1 = self.src_comment({'id': ['id1'], 'header': ['H1']})
        src_2 = self.src_comment({'id': ['id1'], 'header': ['H1']})

        graph = self.build_graph([src_1, src_2])
        self.assertEqual(len(graph.comments), 2)

    def test_has_error(self):
        src_1 = self.src_comment({'id': ['id']})
        src_2 = self.src_comment({'id': ['id']})

        graph = self.build_graph([src_1, src_2])
        self.assertTrue(graph.has_error)

    def test_has_not_uniq_ids(self):
        src_1 = self.src_comment({'id': ['id']})
        src_2 = self.src_comment({'id': ['id']})

        graph = self.build_graph([src_1, src_2])
        self.assertTrue(graph.has_not_uniq_ids)

        src_1 = self.src_comment({'id': ['id1']})
        src_2 = self.src_comment({'id': ['id2']})

        graph = self.build_graph([src_1, src_2])
        self.assertFalse(graph.has_not_uniq_ids)

    def test_has_unknown_dependencies(self):
        src_1 = self.src_comment({'id': ['id1'], 'dependencies': ['id2']})
        src_2 = self.src_comment({'id': ['id2'], 'dependencies': ['unknown1', 'unknown2']})

        graph = self.build_graph([src_1, src_2])
        self.assertTrue(graph.has_unknown_dependencies)
        self.assertDictEqual(graph.unknown_dependencies_by_id, {'id2': {'unknown1', 'unknown2'}})

        src_1 = self.src_comment({'id': ['id1'], 'dependencies': ['id2']})
        src_2 = self.src_comment({'id': ['id2'], 'dependencies': ['id1']})

        graph = self.build_graph([src_1, src_2])
        self.assertFalse(graph.has_unknown_dependencies)
        self.assertDictEqual(graph.unknown_dependencies_by_id, {})

    def test_has_comments(self):
        src_1 = self.src_comment({'id': ['id1'], 'dependencies': ['id2']})
        src_2 = self.src_comment({'id': ['id2'], 'dependencies': ['unknown']})

        graph = self.build_graph([src_1, src_2])
        self.assertTrue(graph.has_comments)

        graph = self.build_graph([])
        self.assertFalse(graph.has_comments)

    def test_has_main_comment(self):
        src_1 = self.src_comment({'id': ['MAIN']})
        src_2 = self.src_comment({'id': ['id2']})

        graph = self.build_graph([src_1, src_2])
        self.assertTrue(graph.has_main_comment)

        src_1 = self.src_comment({'id': ['id1']})
        src_2 = self.src_comment({'id': ['id2']})
        graph = self.build_graph([src_1, src_2])
        self.assertFalse(graph.has_main_comment)

    def test_orphans(self):
        src_1 = self.src_comment({'id': ['MAIN'], 'dependencies': ['id1']})
        src_2 = self.src_comment({'id': ['id1']})
        src_3 = self.src_comment({'id': ['id2']})

        graph = self.build_graph([src_1, src_2, src_3])

        self.assertTrue(graph.has_orphans)
        self.assertCountEqual([c.id for c in graph.orphans], ['id2'])

    def test_semantic_comments(self):
        src_1 = self.src_comment({'id': ['MAIN'], 'dependencies': ['id1']})
        src_2 = self.src_comment({'id': ['id1']})
        src_3 = self.src_comment({'id': ['id2']})

        graph = self.build_graph([src_1, src_2, src_3])

        self.assertCountEqual([c.id for c in graph.semantic_comments], ['id1', 'id2'])

    def test_walk_through_tree(self):
        src_1 = self.src_comment({'id': ['id1'], 'dependencies': ['id2', 'id3']})
        src_2 = self.src_comment({'id': ['id2']})
        src_3 = self.src_comment({'id': ['id3'], 'dependencies': ['id4']})
        src_4 = self.src_comment({'id': ['id4']})

        graph = self.build_graph([src_2, src_3, src_4, src_1])

        edges = []

        def callback(node, parent, _level, _path):
            edges.append(f'{parent and parent.id}->{node.id}')

        graph.walk_through_tree(callback)
        self.assertEqual(edges, ['None->id1', 'id1->id2', 'id1->id3', 'id3->id4'])

    def test_loops(self):
        src_1 = self.src_comment({'id': ['id1'], 'dependencies': ['id2']})
        src_2 = self.src_comment({'id': ['id2'], 'dependencies': ['id3']})
        src_3 = self.src_comment({'id': ['id3'], 'dependencies': ['id4']})
        src_4 = self.src_comment({'id': ['id4'], 'dependencies': ['id2']})

        graph = self.build_graph([src_2, src_3, src_4, src_1])

        self.assertEqual(graph.loops_ids, [['id2', 'id3', 'id4']])
        self.assertEqual(1, len(graph.loops))
        loop = graph.loops[0]
        self.assertEqual([c.id for c in loop], ['id2', 'id3', 'id4'])
        self.assertTrue(graph.is_comment_in_loop(graph.comment('id2')))
        self.assertFalse(graph.is_comment_in_loop(graph.comment('id1')))
        self.assertTrue(graph.is_edge_in_loop(graph.comment('id2'), graph.comment('id3')))
        self.assertTrue(graph.has_loops)

    def test_is_edge_in_tree(self):
        src_1 = self.src_comment({'id': ['id1'], 'dependencies': ['id2', 'id3']})
        src_2 = self.src_comment({'id': ['id2'], 'dependencies': ['id4']})
        src_3 = self.src_comment({'id': ['id3'], 'dependencies': ['id4']})
        src_4 = self.src_comment({'id': ['id4']})

        graph = self.build_graph([src_2, src_3, src_4, src_1])

        self.assertTrue(graph.is_edge_in_tree(graph.comment('id2'), graph.comment('id4')))
        self.assertFalse(graph.is_edge_in_tree(graph.comment('id3'), graph.comment('id4')))

    def test_incoming(self):
        src_1 = self.src_comment({'id': ['id1']})
        graph = self.build_graph([src_1], 2)

        self.assertEqual([], graph.incoming('id1'))
        self.assertEqual([], graph.incoming('UNKNOWN'))

    def test_outgoing(self):
        src_1 = self.src_comment({'id': ['id1']})
        graph = self.build_graph([src_1], 2)

        self.assertEqual([], graph.outgoing('id1'))
        self.assertEqual([], graph.outgoing('UNKNOWN'))

    def test_independent_comment_ids(self):
        src_1 = self.src_comment({'id': ['id1']})
        graph = self.build_graph([src_1], 2)

        self.assertEqual(['id1'], graph.independent_comment_ids)

    def test_blocked_comments(self):
        src_1 = self.src_comment({'id': ['MAIN'], 'dependencies': ['id1']})
        src_2 = self.src_comment({'id': ['id1'], 'dependencies': ['id2']})
        src_3 = self.src_comment({'id': ['id2'], 'dependencies': ['id3'], 'blocker': ['Blocked']})
        src_4 = self.src_comment({'id': ['id3']})

        graph = self.build_graph([src_1, src_2, src_3, src_4])

        self.assertCountEqual([[c.id, c.blocked] for c in graph.comments], [['MAIN', True], ['id1', True], ['id2', True], ['id3', False]])


if __name__ == '__main__':
    unittest.main()
