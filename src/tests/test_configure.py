# stdlib imports
import io
import sys
import unittest
from unittest import mock

# project imports
from configure import get_menu_input, print_monitored_directories, add_directory
import model
import settings


class MenuInputTestCase(unittest.TestCase):
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


class DirectoryManagementTestCase(unittest.TestCase):
    def setUp(self):
        settings.DB_LOCATION = 'sqlite:///:memory:'

    def test_adding_directory(self):
        """Test that a directory can be added"""
        session = model.get_db_session()
        add_directory(directory='/home', session=session)
        directory = session.query(model.Directory).first()
        self.assertEqual(directory.path, '/home')
        session.close()

    def test_adding_invalid_directory(self):
        """Test that an invalid directory cannot be added"""
        session = model.get_db_session()
        add_directory(directory='/directory/does/not/exist', session=session)
        dir_count = session.query(model.Directory).count()
        self.assertEqual(dir_count, 0)
        session.close()

    def test_adding_duplicate_directory(self):
        """Test that a duplicate directory cannot be added"""
        session = model.get_db_session()
        add_directory(directory='/home', session=session)
        dir_count_1 = session.query(model.Directory).count()
        self.assertEqual(dir_count_1, 1)
        add_directory(directory='/home', session=session)
        dir_count_2 = session.query(model.Directory).count()
        self.assertEqual(dir_count_2, 1)
        session.close()

    def test_print_monitored_directories_when_none(self):
        """Test printing directories when none have been added"""
        captured_output = io.StringIO()
        sys.stdout = captured_output  # redirect stdout
        session = model.get_db_session()
        print_monitored_directories(session)
        self.assertEqual(
            captured_output.getvalue(),
            '\nThere are currently no directories being monitored.\n',
        )
        session.close()
        sys.stdout = sys.__stdout__  # stop redirecting stdout

    def test_print_monitored_directories(self):
        """Test printing monitored directories"""
        session = model.get_db_session()
        add_directory(directory='/home', session=session)
        captured_output = io.StringIO()
        sys.stdout = captured_output  # redirect stdout
        print_monitored_directories(session=session)
        self.assertEqual(
            captured_output.getvalue(), '\nMonitored Directories:\n\n/home\n'
        )
        session.close()
        sys.stdout = sys.__stdout__  # stop redirecting stdout
