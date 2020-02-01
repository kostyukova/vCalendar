import unittest
from datetime import date

import swagger_server.controllers.rules as rules
from swagger_server.orm import Employee_leave_days as LeaveDays


class TestRulesMethods (unittest . TestCase):

    def test_intersect(self):
        found = LeaveDays(start_date=date(2020, 1, 10),
                          end_date=date(2020, 1, 20))
        self.assertTrue(rules.intersect(
            found, date(2020, 1, 12), date(2020, 1, 15)))
        self.assertTrue(rules.intersect(
            found, date(2020, 1, 20), date(2020, 1, 25)))
        # open period
        self.assertFalse(rules.intersect(
            found, date(2020, 1, 8), date(2020, 1, 10)))
        self.assertTrue(rules.intersect(
            found, date(2020, 1, 15), date(2020, 1, 25)))
        self.assertTrue(rules.intersect(
            found, date(2020, 1, 5), date(2020, 1, 15)))
        self.assertTrue(rules.intersect(
            found, date(2020, 1, 10), date(2020, 1, 10)))
        self.assertTrue(rules.intersect(
            found, date(2020, 1, 20), date(2020, 1, 20)))

        self.assertFalse(rules.intersect(
            found, date(2020, 1, 25), date(2020, 1, 30)))
        self.assertFalse(rules.intersect(
            found, date(2020, 1, 5), date(2020, 1, 9)))

    def test_max_intersepts_two(self):
        found_list = [LeaveDays(start_date=date(2020, 1, 10),
                                end_date=date(2020, 1, 20)),
                      LeaveDays(start_date=date(2020, 1, 15),
                                end_date=date(2020, 1, 25)),
                      LeaveDays(start_date=date(2020, 1, 26),
                                end_date=date(2020, 1, 28))]
        self.assertEqual(2, len(rules.max_intersepts(found_list)))

    def test_max_intersepts_three(self):
        found_list = [LeaveDays(start_date=date(2020, 1, 10),
                                end_date=date(2020, 1, 20)),
                      LeaveDays(start_date=date(2020, 1, 15),
                                end_date=date(2020, 1, 25)),
                      LeaveDays(start_date=date(2020, 2, 1),
                                end_date=date(2020, 2, 28)),
                      LeaveDays(start_date=date(2020, 2, 10),
                                end_date=date(2020, 2, 20)),
                      LeaveDays(start_date=date(2020, 2, 5),
                                end_date=date(2020, 2, 15))]
        self.assertEqual(3, len(rules.max_intersepts(found_list)))

    def test_max_intersepts_10_12(self):
        found_list = [LeaveDays(start_date=date(2020, 1, 6),
                                end_date=date(2020, 1, 12)),
                      LeaveDays(start_date=date(2020, 1, 10),
                                end_date=date(2020, 1, 19)),
                      LeaveDays(start_date=date(2020, 1, 13),
                                end_date=date(2020, 1, 20))]
        self.assertEqual(2, len(rules.max_intersepts(found_list)))

    def test_max_intersepts_20(self):
        found_list = [LeaveDays(start_date=date(2020, 1, 20),
                                end_date=date(2020, 1, 20)),
                      LeaveDays(start_date=date(2020, 1, 10),
                                end_date=date(2020, 1, 13)),
                      LeaveDays(start_date=date(2020, 1, 19),
                                end_date=date(2020, 1, 20))]
        self.assertEqual(2, len(rules.max_intersepts(found_list)))

if __name__ == '__main__':
    unittest.main()
