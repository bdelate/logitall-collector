# stdlib imports
import unittest

# project imports
import model
import settings


class TestStartUp(unittest.TestCase):
    def setUp(self):
        settings.DB_LOCATION = 'sqlite:///:memory:'

    def test_create_db_tables(self):
        """Test that the database is created when get_db_session"""
        session = model.get_db_session()
        self.assertEqual(session.query(model.Directory).count(), 0)
        self.assertEqual(session.query(model.File).count(), 0)
        session.close()

