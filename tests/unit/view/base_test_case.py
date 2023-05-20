# encoding: utf-8

from tests.unit.base_test_case import BaseTestCase
from srclib.model.task import Task
from srclib.model.comment import Comment


class BaseViewTestCase(BaseTestCase):
    def get_selector_text(self, selector):
        return ' '.join(selector.css('::text').getall()).strip()

    def build_task_from_src(self, src_comments, scale=1, work_hours=None):
        comments = [Comment.parse(src_comment, scale, None) for src_comment in src_comments]
        task = Task(work_hours)
        task.build(comments)

        return task
