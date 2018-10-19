# stdlib imports
import sqlite3
from typing import Optional


class Manager:
    def __init__(self):
        self.conn = sqlite3.connect('./src/collector.sqlite')
        self.cursor = self.conn.cursor()
        sql = 'PRAGMA foreign_keys = 1'  # enforce foreign key constraints
        self.cursor.execute(sql)
        self.create_db_tables()
        self.conn.close()

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


def get_menu_input() -> Optional[int]:
    """Main menu prompt with the available configuration options"""
    options = [
        '1: List directories being monitored',
        '2: Add directory to be monitored',
    ]
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
    option = get_menu_input()
    if option is not None:
        manager = Manager()

