# encoding: utf-8
from unittest import TestCase
from contextlib import contextmanager
from io import StringIO
import sys
import os
from srclib.model.graph import Graph
from srclib.model.comment import Comment

import glob

# Setup language
os.environ["LANGUAGE"] = 'en'

# Load all modules for coverage report
for p in glob.glob('srclib/**/*.py'):
    mod_name = '.'.join(p.replace('.py', '').split('/'))
    __import__(mod_name)


class BaseTestCase(TestCase):
    @contextmanager
    def captured_output(self):
        new_out, new_err = StringIO(), StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = new_out, new_err
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_out, old_err

    def src_comment(self, src):
        return {
            'src': [],
            'file_name': 'file.name',
            'line_num': 1,
            'header': ['Header'],
            'dependencies': [],
            'estimate': [],
            'progress': [],
            'developer_name': [],
            'blocker': [],
            'order': 1
        } | src

    def build_graph(self, src_comments, scale=1, work_hours=None):
        graph = Graph()
        comments = []

        for src_comment in src_comments:
            comments.append(Comment.parse(src_comment, scale, work_hours))

        graph.build(comments)

        return graph
