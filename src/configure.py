# stdlib imports
import sqlite3
from typing import Optional


class Manager:
    def __init__(self):
        self.conn = sqlite3.connect('./src/collector.sqlite')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM sqlite_master;")
        if len(self.cursor.fetchall()) > 0:
            print('tables exist')
        else:
            self.create_db_tables()
        self.conn.close()

    def create_db_tables(self) -> None:
        """Create initial database structure"""
        print('creating tables')


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

