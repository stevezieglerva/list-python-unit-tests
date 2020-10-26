import os, sys, inspect, json

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir) + "/add_cw_log_error_metric"
sys.path.insert(0, parentdir)
print("Updated path:")
print(json.dumps(sys.path, indent=3))

import unittest
from add_cw_log_error_metric.filter_list_by_regexs import *


class FilterRegExUnitTests(unittest.TestCase):
    def test_filter_list_by_regex__given_empty_regexes__then_full_list_returned(self):
        # Arrange
        list = ["apple", "banana", "pear"]
        include_regex = ""
        exclude_regex = ""

        # Act
        results = filter_list_by_regexs(list, include_regex, exclude_regex)

        # Assert
        self.assertEqual(results, list)

    def test_filter_list_by_regex__given_only_exclude_regexe__then_partial_list_returned(
        self,
    ):
        # Arrange
        list = ["apple", "banana", "pear", "blueberry"]
        include_regex = ""
        exclude_regex = ".*a.*"

        # Act
        results = filter_list_by_regexs(list, include_regex, exclude_regex)

        # Assert
        self.assertEqual(results, ["blueberry"])

    def test_filter_list_by_regex__given_only_include_regexe__then_partial_list_returned(
        self,
    ):
        # Arrange
        list = ["apple", "banana", "pear", "blueberry"]
        include_regex = ".*rr.*"
        exclude_regex = ""

        # Act
        results = filter_list_by_regexs(list, include_regex, exclude_regex)

        # Assert
        self.assertEqual(results, ["blueberry"])

    def test_filter_list_by_regex__given_both_regexs__then_partial_list_returned(self):
        # Arrange
        list = ["apple", "banana", "pear", "blueberry"]
        include_regex = ".*rr.*"
        exclude_regex = ".*a.*"

        # Act
        results = filter_list_by_regexs(list, include_regex, exclude_regex)

        # Assert
        self.assertEqual(results, ["blueberry"])
