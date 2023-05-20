# encoding: utf-8

class Progress:
    STATE_ERROR = 'ERROR'
    STATE_NOT_STARTED = 'NOT_STARTED'
    STATE_IN_PROGRESS = 'IN_PROGRESS'
    STATE_ALMOST_DONE = 'ALMOST_DONE'
    STATE_DONE = 'DONE'

    ERROR_PROGRESS_IS_NOT_DEFINED = 'PROGRESS IS NOT DEFINED'
    ERROR_PROGRESS_IS_ALREADY_DEFINED = 'PROGRESS IS ALREADY DEFINED'
    ERROR_WRONG_PROGRESS_FORMAT = 'WRONG PROGRESS FORMAT'
    ERROR_PROGRESS_LT_0 = 'PROGRESS < 0'
    ERROR_PROGRESS_GT_100 = 'PROGRESS > 100'
    ERROR_CALC_ERROR = 'CALC ERROR'

    def __init__(self):
        self.value = None
        self.errors = []

    @property
    def has_errors(self):
        return bool(self.errors)

    @property
    def is_not_started(self):
        return self.state == self.STATE_NOT_STARTED

    @property
    def is_in_progress(self):
        return self.state == self.STATE_IN_PROGRESS

    @property
    def is_almost_done(self):
        return self.state == self.STATE_ALMOST_DONE

    @property
    def is_done(self):
        return self.state == self.STATE_DONE

    @property
    def state(self):
        if self.has_errors:
            return self.STATE_ERROR

        if self.value == 0:
            return self.STATE_NOT_STARTED

        if self.value == 100:
            return self.STATE_DONE

        if self.value >= 90:
            return self.STATE_ALMOST_DONE

        return self.STATE_IN_PROGRESS

    @classmethod
    def parse(cls, src_comment):
        progress = cls()

        if len(src_comment['progress']) == 0:
            progress.add_error(progress.ERROR_PROGRESS_IS_NOT_DEFINED)
        elif len(src_comment['progress']) > 1:
            progress.add_error(progress.ERROR_PROGRESS_IS_ALREADY_DEFINED)
        else:
            try:
                progress.value = int(src_comment['progress'][0])
            except ValueError:
                progress.add_error(progress.ERROR_WRONG_PROGRESS_FORMAT)

        if not progress.has_errors:
            progress.validate()

        return progress

    @classmethod
    def calc(cls, comments):
        progress = cls()

        if len(comments) == 0:
            progress.add_error(cls.ERROR_CALC_ERROR)
            return progress

        time_expected = 0
        time_complete = 0

        for comment in comments:
            if comment.is_main:
                continue

            if comment.estimate.has_errors or comment.progress.has_errors:
                progress.add_error(cls.ERROR_CALC_ERROR)
                progress.value = None
                return progress

            time_expected += comment.estimate.time_expected
            time_complete += comment.estimate.time_expected * comment.progress.value / 100

            progress.value = time_complete / time_expected * 100

        return progress

    def validate(self):
        if self.value < 0:
            self.add_error(self.ERROR_PROGRESS_LT_0)

        if self.value > 100:
            self.add_error(self.ERROR_PROGRESS_GT_100)

    def add_error(self, text):
        self.errors.append(text)
