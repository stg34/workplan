# encoding: utf-8

from datetime import datetime
from srclib.model.graph import Graph
from srclib.model.developer import Developer
from srclib.model.estimate import Estimate
from srclib.model.progress import Progress


class Task():
    def __init__(self, work_hours):
        self.work_hours = work_hours
        self.graph = Graph()
        self.developer_by_name = {}
        self.built_at = None

    @property
    def developers(self):
        return [self.developer_by_name[dev] for dev in self.developer_by_name if dev]

    @property
    def estimate(self):
        return Estimate.sum([c.estimate for c in self.semantic_comments])

    @property
    def remaining_estimate(self):
        return Estimate.sum([c.remaining_estimate for c in self.semantic_comments])

    @property
    def progress(self):
        return Progress.calc(self.semantic_comments)

    @property
    def comments(self):
        return self.graph.comments

    @property
    def semantic_comments(self):
        return self.graph.semantic_comments

    @property
    def main_comment(self):
        return self.graph.main_comment

    def build(self, comments):
        self.graph.build(comments)
        self.build_developers()
        self.built_at = datetime.today()

    def build_developers(self):
        for comment in self.comments:
            if comment.developer_name not in self.developer_by_name:
                self.developer_by_name[comment.developer_name] = Developer(comment.developer_name)

            self.developer_by_name[comment.developer_name].add_comment(comment)
