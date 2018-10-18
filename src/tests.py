# stdlib imports
import unittest
from unittest import mock

# project imports
from configure import get_menu_input


class TestUserInput(unittest.TestCase):
    def test_menu_string_input(self):
        """Test string input to menu returns None"""
        with unittest.mock.patch('builtins.input', return_value='test'):
            option = get_menu_input()
        self.assertIsNone(option)

    def test_menu_invalid_integer_input(self):
        """Test integer outside of menu option range returns None"""
        with unittest.mock.patch('builtins.input', return_value=100):
            option = get_menu_input()
        self.assertIsNone(option)

    def test_valid_integer_input(self):
        """Test valid integer menu input returns the inputted integer"""
        with unittest.mock.patch('builtins.input', return_value=1):
            option = get_menu_input()
        self.assertEqual(1, option)


if __name__ == "__main__":
    unittest.main()
