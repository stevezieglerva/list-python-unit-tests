import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from list_python_unit_tests import *


class UnitTests(unittest.TestCase):
    def test_format_output__given_two_files_in_results__then_correct_results_are_correct(
        self,
    ):
        # Arrange
        input = """test_1.py:class UnitTests(unittest.TestCase):
test_1.py:    def test_this_and_than(self):
test_2a.3.py:class IntegrationTests(unittest.TestCase):
test_2a.3.py:    def test_function_a__given_this__then_that(self):
test_2a.3.py:    def test_function_a__given_this_1__then_that_2(self):"""

        # Act
        results = format_output(input)
        print(results)

        # Assert
        expected = """test_1.py                                         | class UnitTests(unittest.TestCase)
test_1.py                                         |     def test_this_and_than
test_2a.3.py                                      | class IntegrationTests(unittest.TestCase)
test_2a.3.py                                      |     def test_function_a                 | given_this                              | then_that
test_2a.3.py                                      |     def test_function_a                 | given_this_1                            | then_that_2
"""
        self.maxDiff = None
        self.assertEqual(results, expected)

    def test_format_output__given_one_files_in_results__then_results_are_correct(self):
        # Arrange
        input = """class IntegrationTestsOneFile(unittest.TestCase):
    def test_function__given_this__then_that(self):"""

        # Act
        results = format_output(input)
        print(results)

        # Assert
        expected = """class IntegrationTestsOneFile(unittest.TestCase)
    def test_function                   | given_this                              | then_that
"""
        self.maxDiff = None
        self.assertEqual(results, expected)

    def test_format_output__given_line_wrapped_func_name__then_results_are_correct(
        self,
    ):
        # Arrange
        input = """class LineWrap(unittest.TestCase):
    def test_function__given_this__then_that("""

        # Act
        results = format_output(input)
        print(results)

        # Assert
        expected = """class LineWrap(unittest.TestCase)
    def test_function                   | given_this                              | then_that
"""
        self.maxDiff = None
        self.assertEqual(results, expected)


if __name__ == "__main__":
    unittest.main()

