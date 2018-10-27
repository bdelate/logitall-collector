# stdlib imports
import io
import sys
import unittest
from unittest import mock

# project imports
import configure
from configure import get_menu_input
import settings


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
    def setUp(self):
        settings.DB_LOCATION = ':memory:'

    def test_create_db_tables(self):
        """Test that the database is created when Manager is instantiated"""
        m = configure.Manager()
        sql = 'SELECT name FROM sqlite_master WHERE type="table" order by name;'
        m.cursor.execute(sql)
        tables = [table[0] for table in m.cursor.fetchall()]
        self.assertEqual(tables, ['directory', 'file'])

    def test_output_monitored_directories_when_none(self):
        """Test printing directories when none have been added"""
        captured_output = io.StringIO()
        sys.stdout = captured_output
        m = configure.Manager()
        m.output_monitored_directories()
        self.assertEqual(
            captured_output.getvalue(),
            '\nThere are currently no directories being monitored.\n',
        )

    def test_output_monitored_directories(self):
        """Test printing monitored directories"""
        # settings.DB_LOCATION = ':memory:'
        m = configure.Manager()
        m.add_directory('/home')
        captured_output = io.StringIO()
        sys.stdout = captured_output
        m.output_monitored_directories()
        self.assertEqual(
            captured_output.getvalue(), '\nMonitored Directories:\n\n/home\n'
        )

    def test_adding_directory(self):
        """Test that a directory can be added"""
        m = configure.Manager()
        m.add_directory('/home')
        m.cursor.execute('select * from directory;')
        self.assertEqual(len(m.cursor.fetchall()), 1)

    def test_adding_invalid_directory(self):
        """Test that an invalid directory cannot be added"""
        m = configure.Manager()
        m.add_directory('/fake/directory/does/not/exist')
        m.cursor.execute('select * from directory;')
        self.assertEqual(len(m.cursor.fetchall()), 0)

    def test_adding_duplicate_directory(self):
        """Test that a duplicate directory cannot be added"""
        m = configure.Manager()
        m.add_directory('/home')
        m.cursor.execute('select * from directory;')
        self.assertEqual(len(m.cursor.fetchall()), 1)
        m.add_directory('/home')
        m.cursor.execute('select * from directory;')
        self.assertEqual(len(m.cursor.fetchall()), 1)
