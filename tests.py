import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from list_python_unit_tests import *


class UnitTests(unittest.TestCase):
    def test_format_output__given_two_files_in_results__then_results_are_correct(self):
        # Arrange
        input = """test_1.py:class UnitTests(unittest.TestCase):
test_1.py:    def test_this_and_than(self):
test_2a.3.py:class IntegrationTests(unittest.TestCase):
test_2a.3.py:    def test_function__given_this__then__that(self):"""

        # Act
        results = format_output(input)
        print(results)

        # Assert
        expected = """test_1.py                               |class UnitTests(unittest.TestCase)
test_1.py                               |    def test_this_and_than(self)
test_2a.3.py                            |class IntegrationTests(unittest.TestCase)
test_2a.3.py                            |    def test_function__given_this__then__that(self)
"""
        self.maxDiff = None
        self.assertEqual(results, expected)


if __name__ == "__main__":
    unittest.main()

