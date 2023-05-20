# encoding: utf-8

from srclib.presenter.estimate_presenter import EstimatePresenter
from srclib.presenter.progress_presenter import ProgressPresenter
from srclib.presenter.developer_presenter import DeveloperPresenter
from srclib.utils import setup_i18n

_ = setup_i18n('..', 'messages')


class TaskPresenter():
    def __init__(self, task):
        self.task = task
        self.estimate = EstimatePresenter(self.task.estimate, self.task.work_hours)
        self.progress = ProgressPresenter(self.task.progress, self.task.work_hours)
        self.remaining_estimate = EstimatePresenter(self.task.remaining_estimate, self.task.work_hours)
        self.developers = [DeveloperPresenter(dev, self.task.work_hours) for dev in self.task.developers]

    @property
    def total_label(self):
        return _('TOTAL')

    @property
    def title(self):
        if not self.task.graph.main_comment:
            return _('UNTITLED')

        return self.task.graph.main_comment.header

    @property
    def built_at(self):
        return self.task.built_at.strftime('%Y.%m.%d %H:%M:%S')

    @property
    def work_hours(self):
        if self.task.work_hours:
            return _('WORK_HOURS') + f':{self.task.work_hours}'

        return ''

    @property
    def file(self):
        return self.task.graph.main_comment.def_position
