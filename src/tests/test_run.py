# stdlib imports
import unittest
from unittest import mock

# project imports
import run


class TestStartUp(unittest.TestCase):
    @mock.patch('run.logger')
    def test_log_error_if_no_db(self, mock_logger):
        """Test that an error log is created if db does not exist"""
        db_exists = run.db_exists()
        self.assertTrue(mock_logger.error.called)
        self.assertFalse(db_exists)
