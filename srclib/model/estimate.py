# encoding: utf-8

class Estimate:
    ERROR_WRONG_TIME_FORMAT = 'WRONG TIME FORMAT'
    ERROR_TIME_IS_NOT_DEFINED = 'TIME IS NOT DEFINED'
    ERROR_TIME_IS_ALREADY_DEFINED = 'TIME IS ALREADY DEFINED'
    ERROR_TIME_LE_0 = 'TIME <= 0'
    ERROR_TIME_OPTIMISTIC_GT_MOST_LIKELY = 'OPTIMISTIC TIME > MOST LIKELY TIME'
    ERROR_TIME_MOST_LIKELY_GT_PESSIMISTIC = 'MOST LIKELY TIME > PESSIMISTIC TIME'
    ERROR_CALC_ERROR = 'CALC ERROR'

    def __init__(self, scale, optimistic=0, most_likely=0, pessimistic=0):
        self.scale = scale
        self.raw_values = None
        self.time_optimistic = optimistic
        self.time_most_likely = most_likely
        self.time_pessimistic = pessimistic
        self.errors = []

    @classmethod
    def sum(cls, estimates):
        estimate = cls(1, 0, 0, 0)

        if len(estimates) == 0:
            estimate.add_error(cls.ERROR_CALC_ERROR)
            return estimate

        for e in estimates:
            estimate.time_optimistic += e.time_optimistic
            estimate.time_most_likely += e.time_most_likely
            estimate.time_pessimistic += e.time_pessimistic
            estimate.errors += e.errors

        return estimate

    @classmethod
    def calc_remaining(cls, estimate, progress):
        if estimate.has_errors or progress.has_errors:
            estimate = cls(1)
            estimate.add_error(Estimate.ERROR_CALC_ERROR)
            return estimate

        rest = (100 - progress.value) / 100

        time_optimistic = estimate.time_optimistic * rest
        time_most_likely = estimate.time_most_likely * rest
        time_pessimistic = estimate.time_pessimistic * rest
        return cls(1, time_optimistic, time_most_likely, time_pessimistic)

    @property
    def has_errors(self):
        return bool(self.errors)

    @property
    def time_expected(self):
        if self.has_errors:
            return None

        return (self.time_optimistic + 4 * self.time_most_likely + self.time_pessimistic)/6

    @property
    def is_single_time(self):
        return self.time_optimistic == self.time_most_likely and self.time_most_likely == self.time_pessimistic

    def parse_time_str(self, str):
        try:
            values = [float(s.strip()) for s in str.split('/')]
            if not (len(values) == 1 or len(values) == 3):
                self.add_error(self.ERROR_WRONG_TIME_FORMAT)
                return

            self.raw_values = values

        except ValueError:
            self.add_error(self.ERROR_WRONG_TIME_FORMAT)

    def parse_time(self, src_comment):
        if len(src_comment['estimate']) == 0:
            self.add_error(self.ERROR_TIME_IS_NOT_DEFINED)
        elif len(src_comment['estimate']) > 1:
            self.add_error(self.ERROR_TIME_IS_ALREADY_DEFINED)
        else:
            self.parse_time_str(src_comment['estimate'][0])

    @classmethod
    def parse(cls, scale, src_comment):
        estimate = cls(scale)
        estimate.parse_time(src_comment)

        if not estimate.has_errors:
            if len(estimate.raw_values) == 1:
                estimate.time_most_likely = float(estimate.raw_values[0]) * estimate.scale
                estimate.time_optimistic = estimate.time_most_likely
                estimate.time_pessimistic = estimate.time_most_likely
            else:
                estimate.time_optimistic = float(estimate.raw_values[0]) * estimate.scale
                estimate.time_most_likely = float(estimate.raw_values[1]) * estimate.scale
                estimate.time_pessimistic = float(estimate.raw_values[2]) * estimate.scale

            estimate.validate_time()

        return estimate

    def validate_time(self):
        if self.time_optimistic < 0:
            self.add_error(self.ERROR_TIME_LE_0)

        if self.time_optimistic > self.time_most_likely:
            self.add_error(self.ERROR_TIME_OPTIMISTIC_GT_MOST_LIKELY)

        if self.time_most_likely > self.time_pessimistic:
            self.add_error(self.ERROR_TIME_MOST_LIKELY_GT_PESSIMISTIC)

    def add_error(self, text):
        self.errors.append(text)
