# stdlib imports
import io
import sys
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
        _ = configure.Manager()
        assert mock_create_db_tables.called

    @mock.patch(
        'configure.Manager.db_location', new_callable=unittest.mock.PropertyMock
    )
    def test_output_monitored_directories_when_none(self, mock_db_location):
        """Test printing directories when none have been added"""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        mock_db_location.return_value = ':memory:'
        m = configure.Manager()
        m.output_monitored_directories()
        # sys.stdout = sys.__stdout__
        self.assertEqual(
            captured_output.getvalue(),
            '\nThere are currently no directories being monitored.\n',
        )

    @mock.patch(
        'configure.Manager.db_location', new_callable=unittest.mock.PropertyMock
    )
    def test_output_monitored_directories(self, mock_db_location):
        """Test printing monitored directories"""
        mock_db_location.return_value = ':memory:'
        m = configure.Manager()
        m.add_directory('/home')
        captured_output = io.StringIO()
        sys.stdout = captured_output
        m.output_monitored_directories()
        self.assertEqual(
            captured_output.getvalue(), '\nMonitored Directories:\n\n/home\n'
        )


if __name__ == "__main__":
    unittest.main()
