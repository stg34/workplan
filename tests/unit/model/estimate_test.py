# encoding: utf-8

import unittest
from tests.unit.base_test_case import BaseTestCase
from srclib.model.estimate import Estimate
from srclib.model.progress import Progress


class EstimateTest(BaseTestCase):
    def test_parse_01(self):
        scale = 2
        estimate = Estimate.parse(scale, {'estimate': ['6/12/24']})

        self.assertEqual(estimate.time_optimistic, 6 * scale)
        self.assertEqual(estimate.time_most_likely, 12 * scale)
        self.assertEqual(estimate.time_pessimistic, 24 * scale)
        self.assertEqual(estimate.time_expected, 26)

    def test_parse_02(self):
        scale = 2
        estimate = Estimate.parse(scale, {'estimate': ['2']})

        self.assertEqual(estimate.time_optimistic, 2 * scale)
        self.assertEqual(estimate.time_most_likely, 2 * scale)
        self.assertEqual(estimate.time_pessimistic, 2 * scale)
        self.assertEqual(estimate.time_expected, 2 * scale)

    def test_parse_03(self):
        estimate = Estimate.parse(1, {'estimate': ['A']})

        self.assertTrue(estimate.has_errors)
        self.assertCountEqual([Estimate.ERROR_WRONG_TIME_FORMAT], estimate.errors)
        self.assertIsNone(estimate.time_expected)

    def test_parse_04(self):
        src_comment = {
            'completeness': ['50'],
            'estimate': ['1/2'],
        }

        estimate = Estimate.parse(1, src_comment)

        self.assertTrue(estimate.has_errors)
        self.assertCountEqual([Estimate.ERROR_WRONG_TIME_FORMAT], estimate.errors)

    def test_parse_05(self):
        estimate = Estimate.parse(1, {'estimate': ['1/2', '1']})

        self.assertCountEqual([Estimate.ERROR_TIME_IS_ALREADY_DEFINED], estimate.errors)

    def test_parse_06(self):
        estimate = Estimate.parse(1, {'estimate': []})

        self.assertCountEqual([Estimate.ERROR_TIME_IS_NOT_DEFINED], estimate.errors)

    def test_parse_07(self):
        estimate = Estimate.parse(1, {'estimate': ['-10']})

        self.assertCountEqual([Estimate.ERROR_TIME_LE_0], estimate.errors)

    def test_parse_08(self):
        estimate = Estimate.parse(1, {'estimate': ['4/3/2']})

        self.assertCountEqual([Estimate.ERROR_TIME_OPTIMISTIC_GT_MOST_LIKELY, Estimate.ERROR_TIME_MOST_LIKELY_GT_PESSIMISTIC], estimate.errors)

    def test_single_time(self):
        estimate = Estimate.parse(1, {'estimate': ['1']})
        self.assertTrue(estimate.is_single_time)

        estimate = Estimate.parse(1, {'estimate': ['1/2/3']})
        self.assertFalse(estimate.is_single_time)

    def test_sum(self):
        e1 = Estimate.parse(1, {'estimate': ['1']})
        e2 = Estimate.parse(1, {'estimate': ['2']})

        esum = Estimate.sum([e1, e2])
        self.assertEqual(esum.time_expected, 3)

        esum = Estimate.sum([])
        self.assertCountEqual([Estimate.ERROR_CALC_ERROR], esum.errors)

    def test_calc_remaining(self):
        estimate = Estimate.parse(1, {'estimate': ['2']})
        progress = Progress.parse({'progress': ['75']})

        esum = Estimate.calc_remaining(estimate, progress)
        self.assertEqual(esum.time_expected, 0.5)

        progress = Progress.parse({'progress': ['ERROR']})

        esum = Estimate.calc_remaining(estimate, progress)
        self.assertIsNone(esum.time_expected)


if __name__ == '__main__':
    unittest.main()
