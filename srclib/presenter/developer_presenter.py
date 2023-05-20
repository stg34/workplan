# encoding: utf-8

from srclib.presenter.estimate_presenter import EstimatePresenter
from srclib.presenter.progress_presenter import ProgressPresenter
# from srclib.utils import setup_i18n

# _ = setup_i18n('..', 'messages')


class DeveloperPresenter():
    def __init__(self, developer, work_hours):
        self.developer = developer
        self.work_hours = work_hours
        self.estimate = EstimatePresenter(self.developer.estimate, work_hours)
        self.remaining_estimate = EstimatePresenter(self.developer.remaining_estimate, work_hours)
        self.progress = ProgressPresenter(self.developer.progress, work_hours)

    @property
    def name(self):
        return self.developer.name + ':'

    # @property
    # def value(self, developer_name):
    #     estimate_presenter = EstimatePresenter(self.graph.developer_by_name[developer_name].estimate, self.work_hours)
    #     return estimate_presenter.progress_value

    # def progress(self, developer_name):
    #     return self.label + ' ' + self.value(developer_name)
