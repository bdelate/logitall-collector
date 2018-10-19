# stdlib imports
import unittest
from unittest import mock

# project imports
import configure
from configure import get_menu_input


class TestMenuInput(unittest.TestCase):
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

    def test_valid_integer_input(self,):
        """Test valid integer menu input returns the inputted integer"""
        with unittest.mock.patch('builtins.input', return_value=1):
            option = get_menu_input()
        self.assertEqual(1, option)


class TestManager(unittest.TestCase):
    @mock.patch('sqlite3.connect')
    @mock.patch('configure.Manager.create_db_tables')
    def test_create_db_tables(self, mock_create_db_tables, mock_sql_connect):
        """Test that create_db_tables is called when Manager is instantiated"""
        manager = configure.Manager()
        assert mock_create_db_tables.called


if __name__ == "__main__":
    unittest.main()
