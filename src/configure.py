# stdlib imports
import atexit
import sqlite3
from typing import Optional


class Manager:
    def __init__(self):
        self.conn = sqlite3.connect('./src/collector.sqlite')
        self.cursor = self.conn.cursor()
        sql = 'PRAGMA foreign_keys = 1'  # enforce foreign key constraints
        self.cursor.execute(sql)
        self.create_db_tables()

    def create_db_tables(self) -> None:
        """Create database tables if they don't already exist"""
        sql = '''
            CREATE TABLE IF NOT EXISTS directory
                (id INTEGER PRIMARY KEY,
                path TEXT not null unique);
        '''
        self.cursor.execute(sql)
        sql = '''
            CREATE TABLE IF NOT EXISTS file
                (id INTEGER PRIMARY KEY,
                name TEXT not null,
                size INTEGER not null,
                directory_id INTEGER not null,
                FOREIGN KEY (directory_id) REFERENCES directory(id))
        '''
        self.cursor.execute(sql)
        self.conn.commit()

    def close_db_connection(self) -> None:
        """Close database connection"""
        self.conn.close()

    def output_monitored_directories(self) -> None:
        """Print all directories being monitored"""
        sql = 'SELECT path FROM directory;'
        self.cursor.execute(sql)
        directories = self.cursor.fetchall()
        if len(directories) > 0:
            print('\nMonitored Directories:\n')
            for directory in directories:
                print(directory[0])
        else:
            print('\nThere are currently no directories being monitored')


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


if __name__ == "__main__":
    manager = Manager()
    atexit.register(manager.close_db_connection)  # close db connection on exit
    option = get_menu_input()
    while option is not None:
        if option == 1:
            manager.output_monitored_directories()
        option = get_menu_input()
