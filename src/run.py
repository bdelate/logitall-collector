# stdlib imports
import logging
import pathlib

# 3rd party imports
from sqlalchemy.orm.session import Session

# project imports
import model
import settings

# Setup logging to file
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler("logitall.log")
formatter = logging.Formatter("%(asctime)s: %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def process_directories(session: Session) -> None:
    """Call process_directory for each directory in the database"""
    directories = session.query(model.Directory).all()
    for directory in directories:
        process_directory(directory=directory, session=session)


def process_directory(directory: model.Directory, session: Session) -> None:
    """Call process_file for each file in the specified directory"""
    path = pathlib.Path(directory.path)
    if path.exists():
        for file in path.glob(pattern="*"):
            if file.is_file():
                process_file(directory=directory, file=file, session=session)
    else:
        logger.error(f"Invalid directory: {path}")


def process_file(
    directory: model.Directory, file: pathlib.Path, session: Session
) -> None:
    """
    If the file doesn't exist in the db, upload it and add it to the db.
    If the file exists in the db, upload any new content and update its size.
    """
    db_file = (
        session.query(model.File)
        .filter_by(directory_id=directory.id, name=file.name)
        .first()
    )
    if db_file is None:
        upload_logs(file=file, start_pos=0)
        new_db_file = model.File(
            name=file.name, size=file.stat().st_size, directory_id=directory.id
        )
        session.add(new_db_file)
        session.commit()
    elif file.stat().st_size > db_file.size:
        upload_logs(file=file, start_pos=db_file.size)
        db_file.size = file.stat().st_size
        session.add(db_file)
        session.commit()


def upload_logs(file: pathlib.Path, start_pos: int) -> None:
    """Upload file to the server from start_pos to the end of the file"""
    with open(file) as open_file:
        open_file.seek(start_pos)
        for line in open_file:
            entry = line.rstrip("\n")
            print(f"to upload: {entry}")


if __name__ == "__main__":
    session = model.get_db_session()
    process_directories(session=session)
    session.close()
