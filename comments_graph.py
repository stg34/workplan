class CommentsUniqIdException(Exception):
    def __init__(self, comment1, comment2):
        self.comment1 = comment1
        self.comment2 = comment2

class UnknownDependencyException(Exception):
    def __init__(self, dependency, comment):
        self.dependency = dependency
        self.comment = comment

class GraphLoop(Exception):
    def __init__(self, ids):
        self.ids = ids

class CommentsGraph:
    def __init__(self):
        self.comments = []
        self.incoming_by_id = {}
        self.outgoing_by_id = {}
        self.comment_by_id = {}

    def add_comment(self, comment):
        self.comments.append(comment)

    def build_graph(self):
        for comment in self.comments:
            self.comment_by_id[comment.id] = comment
            self.incoming_by_id[comment.id] = []
            self.outgoing_by_id[comment.id] = []

        for comment in self.comments:
            for dep in comment.dependencies:
                self.outgoing_by_id[comment.id].append(dep)
                self.incoming_by_id[dep].append(comment.id)

    def comment(self, id):
        return self.comment_by_id[id]

    def incoming(self, id):
        return list(map(lambda cid: self.comment_by_id[cid], self.incoming_by_id[id]))
    
    def outgoing(self, id):
        return list(map(lambda cid: self.comment_by_id[cid], self.outgoing_by_id[id]))

    def validate(self):
        comment_by_id = {}

        for comment in self.comments:
            if comment.id in comment_by_id: raise CommentsUniqIdException(comment, comment_by_id[comment.id])

            comment_by_id[comment.id] = comment

        for comment in self.comments:
            for dep in comment.dependencies:
                if dep not in comment_by_id: raise UnknownDependencyException(dep, comment)

    def list_diff(self, list1, list2):
        s = set(list2)
        return [x for x in list1 if x not in s]

    def independent_comment_ids(self, reverse = True):
        ids = self.comment_by_id.keys()
        if reverse:
            independent = list(filter(lambda c: len(self.outgoing_by_id[c]) == 0, ids))
        else:
            independent = list(filter(lambda c: len(self.incoming_by_id[c]) == 0, ids))

        independent.sort(key = lambda id: self.comment_by_id[id].order)
        
        return independent

    def topological_sort(self):
        sorted = []
        unprocessed = list(self.comment_by_id.keys())

        while len(unprocessed):
            independent = list(filter(lambda c: len(self.list_diff(self.outgoing_by_id[c], sorted)) == 0, unprocessed))
            independent.sort(key = lambda id: self.comment_by_id[id].order)
            
            if len(independent) == 0: raise GraphLoop(unprocessed)

            sorted += independent
            unprocessed = self.list_diff(unprocessed, independent)

        return sorted

    def dfs(self, start_id, callback, level = 0, visited = set()):
        if start_id in visited: return

        callback(self.comment_by_id[start_id], level)

        visited.add(start_id)

        for id in self.outgoing_by_id[start_id]:
            self.dfs(id, callback, level + 1, visited)
