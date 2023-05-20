# encoding: utf-8

from srclib.utils import format_num
from srclib.model.estimate import Estimate
from srclib.utils import setup_i18n

_ = setup_i18n('..', 'messages')


class EstimatePresenter():
    ERROR_MAP = {
        Estimate.ERROR_WRONG_TIME_FORMAT: _('WRONG TIME FORMAT'),
        Estimate.ERROR_TIME_IS_NOT_DEFINED: _('TIME IS NOT DEFINED'),
        Estimate.ERROR_TIME_IS_ALREADY_DEFINED: _('TIME IS ALREADY DEFINED'),
        Estimate.ERROR_TIME_LE_0: _('TIME <= 0'),
        Estimate.ERROR_TIME_OPTIMISTIC_GT_MOST_LIKELY: _('OPTIMISTIC TIME > MOST LIKELY TIME'),
        Estimate.ERROR_TIME_MOST_LIKELY_GT_PESSIMISTIC: _('MOST LIKELY TIME > PESSIMISTIC TIME'),
    }

    def __init__(self, estimate, work_hours):
        self.estimate = estimate
        self.work_hours = work_hours

    def time_value_str(self, time):
        if self.work_hours:
            value = _('{time} H. / {days} D.').format(time=format_num(time), days=format_num(time / self.work_hours))
        else:
            value = _('{time} H.').format(time=format_num(time))

        return value

    @property
    def time_label(self):
        return _('TIME')

    @property
    def time_value(self):
        if self.estimate.has_errors:
            return '?'

        time = self.estimate.time_expected
        value = self.time_value_str(time)

        if not self.estimate.is_single_time:
            value += f' ({format_num(self.estimate.time_optimistic)}/{format_num(self.estimate.time_most_likely)}/{format_num(self.estimate.time_pessimistic)})'

        return value

    @property
    def remaining_time(self):
        return self.remaining_time_label + ': ' + self.time_value

    @property
    def time(self):
        return self.time_label + ': ' + self.time_value

    @property
    def remaining_time_label(self):
        return _('REMAINING TIME')

    @property
    def errors(self):
        return [self.ERROR_MAP[e] for e in self.estimate.errors]
