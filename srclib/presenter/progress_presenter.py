# encoding: utf-8

import math
from srclib.utils import format_num
from srclib.model.progress import Progress
from srclib.utils import setup_i18n

_ = setup_i18n('..', 'messages')


class ProgressPresenter():
    ERROR_MAP = {
        Progress.ERROR_PROGRESS_IS_NOT_DEFINED: _('PROGRESS IS NOT DEFINED'),
        Progress.ERROR_PROGRESS_IS_ALREADY_DEFINED: _('PROGRESS IS ALREADY DEFINED'),
        Progress.ERROR_WRONG_PROGRESS_FORMAT: _('WRONG PROGRESS FORMAT'),
        Progress.ERROR_PROGRESS_LT_0: _('PROGRESS < 0'),
        Progress.ERROR_PROGRESS_GT_100: _('PROGRESS > 100')
    }

    def __init__(self, progress, work_hours):
        self.progress = progress
        self.work_hours = work_hours

    @property
    def label(self):
        return _('PROGRESS')

    @property
    def value(self):
        if self.progress.has_errors:
            return '?'

        return '{progress} %'.format(progress=format_num(math.floor(self.progress.value)))

    @property
    def label_value(self):
        return self.label + ': ' + self.value

    @property
    def errors(self):
        return [self.ERROR_MAP[e] for e in self.progress.errors]
