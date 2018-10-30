# stdlib imports
import atexit
import pathlib
import sqlite3
from typing import Optional

# 3rd party imports
from sqlalchemy.orm.session import Session

# project imports
import model
import settings


def get_menu_input() -> Optional[int]:
    """Main menu prompt with the available configuration options"""
    options = [
        '1: List directories being monitored',
        '2: Add directory to be monitored',
    ]
    print()
    print(*options, sep='\n')

    try:
        choice = int(input('> '))
        if choice not in range(1, len(options) + 1):
            raise ValueError
    except ValueError:
        print('Invalid choice.')
        return None
    else:
        return choice


def add_directory(directory: str, session: Session) -> None:
    """Add new directory to be monitored"""
    path = pathlib.Path(directory)
    if path.is_dir():
        path_str = str(path.resolve()).lower()
        directory_exists = (
            session.query(model.Directory).filter_by(path=path_str).count()
        )
        if directory_exists == 0:
            new_directory = model.Directory(path=path_str)
            session.add(new_directory)
            session.commit()
            print('\nDirectory Added.')
        else:
            print('\nDirectory is already being monitored.')
    else:
        print('\nInvalid directory.')


def print_monitored_directories(session: Session) -> None:
    """Print all directory paths in the database"""
    directories = session.query(model.Directory).all()
    if len(directories) > 0:
        print('\nMonitored Directories:\n')
        for directory in directories:
            print(directory.path)
    else:
        print('\nThere are currently no directories being monitored.')


if __name__ == "__main__":
    session = model.get_db_session()
    atexit.register(session.close)  # always close db connection on exit
    option = get_menu_input()
    while option is not None:
        if option == 1:
            print_monitored_directories(session)
        elif option == 2:
            directory = input('\nEnter full path (eg: /var/log/nginx)\n>')
            add_directory(directory=directory, session=session)
        option = get_menu_input()
