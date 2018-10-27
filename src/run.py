# stdlib imports
import logging
import pathlib

# project imports
import settings

# Setup logging to file
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler('logitall.log')
formatter = logging.Formatter('%(asctime)s: %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def db_exists() -> bool:
    """Check if the monitoring db exists"""
    path = pathlib.Path(settings.DB_LOCATION)
    if path.exists():
        return True
    logger.error('Monitoring db does not exist. Please run configure.py')
    return False


if __name__ == '__main__':
    if db_exists():
        print('database exists')
