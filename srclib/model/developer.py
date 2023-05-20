# encoding: utf-8

from srclib.model.estimate import Estimate
from srclib.model.progress import Progress


class Developer:
    def __init__(self, name):
        self.name = name
        self.comments = []

    def add_comment(self, comment):
        self.comments.append(comment)

    @property
    def progress(self):
        return Progress.calc(self.comments)

    @property
    def estimate(self):
        return Estimate.sum([c.estimate for c in self.comments])

    @property
    def remaining_estimate(self):
        return Estimate.sum([c.remaining_estimate for c in self.comments])
