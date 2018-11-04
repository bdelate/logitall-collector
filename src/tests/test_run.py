# stdlib imports
import pathlib
import unittest
from unittest import mock

# 3rd party imports
from pyfakefs import fake_filesystem_unittest

# project imports
import model
import run
import settings


class Run(fake_filesystem_unittest.TestCase):
    def setUp(self):
        settings.DB_LOCATION = "sqlite:///:memory:"
        self.setUpPyfakefs()
        self.session = model.get_db_session()

        self.path_1 = "/home"
        self.directory_1 = model.Directory(path=self.path_1)
        self.session.add(self.directory_1)

        self.path_2 = "/var"
        self.directory_2 = model.Directory(path=self.path_2)
        self.session.add(self.directory_2)
        self.session.commit()

        self.file_1_name = "file_1"
        self.file_1_content = "test"
        self.fake_file_1 = self.fs.create_file(
            f"{self.path_1}/{self.file_1_name}", contents=self.file_1_content
        )

        self.db_file_1 = model.File(
            name=self.file_1_name,
            size=len(self.file_1_content),
            directory_id=self.directory_1.id,
        )
        self.session.add(self.db_file_1)

        self.file_2_name = "file_2"
        self.file_2_content = "test"
        self.fake_file_2 = self.fs.create_file(
            f"{self.path_1}/{self.file_2_name}"
        )
        self.db_file_2 = model.File(
            name=self.file_2_name,
            size=len(self.file_2_content),
            directory_id=self.directory_1.id,
        )

        self.session.commit()

    def tearDown(self):
        self.session.close()

    @mock.patch("run.process_directory")
    def test_process_directories(self, mock_process_directory):
        """Test that process_directory is called correctly for every directory"""
        run.process_directories(session=self.session)
        self.assertEqual(mock_process_directory.call_count, 2)
        mock_process_directory.assert_called_with(
            directory=self.directory_2, session=self.session
        )

    @mock.patch("run.process_file")
    def test_process_directory(self, mock_process_file):
        """Test that process file is called for each file in a directory"""
        run.process_directory(directory=self.directory_1, session=self.session)
        self.assertEqual(mock_process_file.call_count, 2)
        path = pathlib.Path(self.fake_file_2.path)
        mock_process_file.assert_called_with(
            directory=self.directory_1, file=path, session=self.session
        )

    @mock.patch("run.logger")
    @mock.patch("run.process_file")
    def test_process_invalid_directory(self, mock_process_file, mock_logger):
        """Test that an error is logged if an invalid directory is used"""
        with mock.patch("pathlib.Path.exists", return_value=False):
            run.process_directory(
                directory=self.directory_1, session=self.session
            )
            self.assertEqual(mock_process_file.call_count, 0)
            self.assertTrue(mock_logger.error.called)

    @mock.patch("run.upload_logs")
    def test_process_existing_file_unchanged(self, mock_upload_logs):
        """An existing unchanged file requires no action"""
        file = pathlib.Path(f"{self.path_1}/{self.file_1_name}")
        run.process_file(
            directory=self.directory_1, file=file, session=self.session
        )
        self.assertTrue(mock_upload_logs.not_called)
        db_file = self.session.query(model.File).first()
        self.assertEqual(db_file.size, len(self.file_1_content))

    @mock.patch("run.upload_logs")
    def test_process_existing_file_new_content(self, mock_upload_logs):
        """
        An existing file with new content calls upload_logs and updates db size
        """
        file = pathlib.Path(f"{self.path_1}/{self.file_1_name}")
        file.write_text(self.file_1_content * 2)
        run.process_file(
            directory=self.directory_1, file=file, session=self.session
        )
        self.assertTrue(mock_upload_logs.called)
        db_file = self.session.query(model.File).first()
        self.assertEqual(db_file.size, len(self.file_1_content) * 2)

    @mock.patch("run.upload_logs")
    def test_process_new_file(self, mock_upload_logs):
        """A new file that isn't in the db is added and calls upload_logs"""
        self.fs.create_file(f"{self.path_1}/new_fake_file")
        new_fake_file = pathlib.Path(f"{self.path_1}/new_fake_file")
        new_fake_file.write_text("testing")
        run.process_file(
            directory=self.directory_1,
            file=new_fake_file,
            session=self.session,
        )
        self.assertTrue(mock_upload_logs.called)
        db_file = (
            self.session.query(model.File)
            .filter_by(name=new_fake_file.name)
            .first()
        )
        self.assertEqual(db_file.size, new_fake_file.stat().st_size)

    @unittest.skip("to be implemented")
    def test_upload_logs(self):
        pass
