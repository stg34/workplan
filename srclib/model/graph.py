# encoding: utf-8

import copy
from srclib.model.comment import Comment


class Graph:
    def __init__(self):
        self.incoming_by_id = {}
        self.outgoing_by_id = {}
        self.comment_by_id = {}
        self.comments = []
        self.loops_ids = []
        self.nodes_in_loop = set()
        self.edges_in_loop = set()
        self.tree_edges = set()
        self.unknown_dependencies_by_id = {}
        self.orphans_by_id = {}
        self.not_uniq_ids = {}
        self.main_comment = None

    @property
    def loops(self):
        return [[self.comment(id) for id in ids] for ids in self.loops_ids]

    @property
    def has_error(self):
        return (not self.has_comments
                or self.has_loops
                or self.has_orphans
                or self.has_not_uniq_ids
                or not self.has_main_comment
                or self.has_unknown_dependencies)

    @property
    def has_comments(self):
        return bool(self.comments)

    @property
    def has_loops(self):
        return bool(self.loops_ids)

    @property
    def has_orphans(self):
        return bool(self.orphans_by_id)

    @property
    def has_not_uniq_ids(self):
        return bool(self.not_uniq_ids)

    @property
    def has_main_comment(self):
        return bool(self.main_comment)

    @property
    def has_unknown_dependencies(self):
        return bool(self.unknown_dependencies_by_id)

    def find_main_comment(self):
        if Comment.ID_MAIN in self.comment_by_id:
            self.main_comment = self.comment_by_id[Comment.ID_MAIN]

    def find_not_uniq_ids(self):
        comments_by_id = {}
        for comment in self.comments:
            if comment.id in comments_by_id:
                comments_by_id[comment.id].append(comment)
            else:
                comments_by_id[comment.id] = [comment]

        self.not_uniq_ids = {id: comments for id, comments in comments_by_id.items() if len(comments) > 1}

    def build_indices(self):
        for comment in self.comments:
            self.comment_by_id[comment.id] = comment
            self.incoming_by_id[comment.id] = []
            self.outgoing_by_id[comment.id] = []

        for comment in self.comments:
            for dep in comment.dependencies:
                if dep in self.comment_by_id:
                    self.outgoing_by_id[comment.id].append(dep)
                    self.incoming_by_id[dep].append(comment.id)
                else:
                    if comment.id in self.unknown_dependencies_by_id:
                        self.unknown_dependencies_by_id[comment.id].add(dep)
                    else:
                        self.unknown_dependencies_by_id[comment.id] = {dep}

    def build(self, comments):
        self.comments = comments
        for comment in self.comments:
            comment.graph = self

        self.find_not_uniq_ids()
        self.build_indices()
        self.find_main_comment()
        self.build_tree_edges()
        self.find_orphans()
        self.find_loops()
        self.find_blocked()

    def find_orphans(self):
        for comment in self.comments:
            if len(self.incoming(comment.id)) == 0 and not comment.is_main:
                self.orphans_by_id[comment.id] = comment

    def walk_through_tree(self, callback):
        visited = set()
        for comment in self.independent_comments:
            self.dfs(comment, None, callback, visited=visited)

    def build_tree_edges(self):
        self.walk_through_tree(lambda c, p, _lvl, _path: self.tree_edges.add(f'{p and p.id}->{c.id}'))

    def comment(self, id):
        return self.comment_by_id[id]

    def incoming(self, id):
        return [self.comment(ci) for ci in self.incoming_ids(id)]

    def incoming_ids(self, id):
        if id not in self.incoming_by_id:
            return []

        return self.incoming_by_id[id]

    def outgoing(self, id):
        return [self.comment(ci) for ci in self.outgoing_ids(id)]

    def outgoing_ids(self, id):
        if id not in self.outgoing_by_id:
            return []

        return self.outgoing_by_id[id]

    @property
    def semantic_comments(self):
        return [c for c in self.comments if not c.is_main]

    @property
    def independent_comment_ids(self):
        return list(filter(lambda id: len(self.incoming(id)) == 0, self.comment_by_id.keys()))

    @property
    def independent_comments(self):
        return [self.comment(ci) for ci in self.independent_comment_ids]

    @property
    def orphans(self):
        return self.orphans_by_id.values()

    def dfs(self, node, parent, callback, level=0, visited=None, path=None):
        visited = visited or set()
        path = path or []

        if node.id in visited:
            return

        callback(node, parent, level, path)
        visited.add(node.id)

        for comment in self.outgoing(node.id):
            new_path = copy.deepcopy(path)
            new_path.append(node.id)
            self.dfs(comment, node, callback, level + 1, visited, new_path)

    def loop_dfs(self, node, visited, loops, path=None):
        path = path or []

        if node.id in path:
            loop = path[path.index(node.id):]
            loops.append(loop)

            for i in range(len(loop)):
                self.nodes_in_loop.add(loop[i])
                self.edges_in_loop.add(f'{loop[i]}->{loop[(i+1)%len(loop)]}')

            return

        if node.id in visited:
            return

        visited.add(node.id)

        for comment in self.outgoing(node.id):
            new_path = copy.deepcopy(path)
            new_path.append(node.id)
            self.loop_dfs(comment, visited, loops, new_path)

    def find_loops(self):
        visited = set()
        loops = []

        for comment in self.comments:
            if comment.id in visited:
                continue

            self.loop_dfs(comment, visited, loops)

        self.loops_ids = loops

    def find_blocked(self):
        if self.loops_ids:
            return

        blockers = list(filter(lambda c: c.blocker, self.comments))
        for comment in blockers:
            self.mark_blocked_comments(comment)

    def mark_blocked_comments(self, comment):
        comment.blocked = True
        for incoming in self.incoming(comment.id):
            self.mark_blocked_comments(incoming)

    def is_comment_in_loop(self, comment):
        return comment.id in self.nodes_in_loop

    def is_edge_in_loop(self, src, dst):
        return f'{src.id}->{dst.id}' in self.edges_in_loop

    def is_edge_in_tree(self, src, dst):
        return f'{src.id}->{dst.id}' in self.tree_edges
