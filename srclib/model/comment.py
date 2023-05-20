# encoding: utf-8

from srclib.model.estimate import Estimate
from srclib.model.progress import Progress


class Comment:
    ID_MAIN = 'MAIN'

    ERROR_ID_IS_NOT_DEFINED = 'ID IS NOT DEFINED'
    ERROR_ID_IS_ALREADY_DEFINED = 'ID IS ALREADY DEFINED'
    ERROR_DEVELOPER_IS_ALREADY_DEFINED = 'DEVELOPER IS ALREADY DEFINED'
    ERROR_BLOCKER_IS_ALREADY_DEFINED = 'BLOCKER ATTRIBUTE IS ALREADY DEFINED'
    ERROR_HEADER_IS_NOT_DEFINED = 'HEADER IS NOT DEFINED'
    ERROR_HEADER_IS_ALREADY_DEFINED = 'HEADER IS ALREADY DEFINED'
    ERROR_REFERENCE_TO_MAIN = "COMMENT REFERENCES THE MAIN COMMENT"
    ERROR_EMPTY_DEPENDENCY = 'EMPTY DEPENDENCY'
    ERROR_ORDER_IS_NOT_DEFINED = 'ORDER IS NOT DEFINED'
    ERROR_ORPHAN = 'EMPTY ORPHAN'

    def __init__(self, scale, work_hours):
        self.graph = None
        self.estimate = None
        self.progress = None
        self.scale = scale
        self.work_hours = work_hours
        self.id = None
        self.dependencies = []
        self.header = None
        self.order = None
        self.developer_name = None
        self.blocker = False
        self.blocked = False
        self.blocker_comment = None
        self.src_lines = []
        self.file_name = None
        self.src_line_num = None
        self.errors = []
        # self.not_uniq_dependencies = []

    @property
    def remaining_estimate(self):
        return Estimate.calc_remaining(self.estimate, self.progress)

    @property
    def is_main(self):
        return self.id == self.ID_MAIN

    @property
    def has_errors(self):
        return bool(self.errors)

    @property
    def def_position(self):
        return f'{self.file_name}:{self.src_line_num}'

    def parse_id(self, src_comment):
        if len(src_comment['id']) == 0:
            self.add_error(self.ERROR_ID_IS_NOT_DEFINED)
        elif len(src_comment['id']) > 1:
            self.add_error(self.ERROR_ID_IS_ALREADY_DEFINED)
        else:
            self.id = src_comment['id'][0]

    def parse_developer(self, src_comment):
        if len(src_comment['developer_name']) > 1:
            self.add_error(self.ERROR_DEVELOPER_IS_ALREADY_DEFINED)
        elif len(src_comment['developer_name']) == 1:
            self.developer_name = src_comment['developer_name'][0]

    def parse_blocker(self, src_comment):
        if len(src_comment['blocker']) > 1:
            self.add_error(self.ERROR_BLOCKER_IS_ALREADY_DEFINED)
        elif len(src_comment['blocker']) == 1:
            self.blocker = True
            if src_comment['blocker'][0].strip():
                self.blocker_comment = src_comment['blocker'][0].strip()

    def parse_header(self, src_comment):
        if len(src_comment['header']) == 0:
            self.add_error(self.ERROR_HEADER_IS_NOT_DEFINED)
        elif len(src_comment['header']) > 1:
            self.add_error(self.ERROR_HEADER_IS_ALREADY_DEFINED)
            self.header = src_comment['header'][0]
        else:
            self.header = src_comment['header'][0]

    def parse_order(self, src_comment):
        if src_comment['order'] is None:
            self.add_error(self.ERROR_ORDER_IS_NOT_DEFINED)
            self.order = 0
        else:
            self.order = int(src_comment['order'])

    def parse_dependencies(self, src_comment):
        for dep in src_comment['dependencies']:
            if dep == Comment.ID_MAIN:
                self.add_error(self.ERROR_REFERENCE_TO_MAIN)

            if not dep.strip():
                self.add_error(self.ERROR_EMPTY_DEPENDENCY)

        for dep in filter(lambda d: d, src_comment['dependencies']):
            if dep not in self.dependencies:
                self.dependencies.append(dep.strip())

    @classmethod
    def parse(cls, src_comment, scale, work_hours):
        comment = cls(scale, work_hours)

        comment.file_name = src_comment['file_name']
        comment.src_lines = src_comment['src']
        comment.src_line_num = src_comment['line_num']

        comment.parse_id(src_comment)
        comment.parse_header(src_comment)
        comment.parse_dependencies(src_comment)
        comment.parse_developer(src_comment)
        comment.parse_blocker(src_comment)
        comment.parse_order(src_comment)

        if not comment.is_main:
            comment.estimate = Estimate.parse(scale, src_comment)
            comment.progress = Progress.parse(src_comment)
        else:
            comment.estimate = Estimate(scale)
            comment.progress = Progress()

        return comment

    def add_error(self, text):
        self.errors.append(text)
