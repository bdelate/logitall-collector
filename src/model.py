# stdlib imports
from typing import Any

# 3rd party imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
from sqlalchemy.engine import Engine

# project imports
import settings


Base = declarative_base()  # type: Any


@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record) -> None:
    """Enforce foreign key constraints which sqlite does not do by default"""
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON')
    cursor.close()


class Directory(Base):

    __tablename__ = 'directory'
    id = Column(Integer, primary_key=True)
    path = Column(String, nullable=False, unique=True)


class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    directory_id = Column(Integer, ForeignKey('directory.id'))


def get_db_session() -> Session:
    """Create db if it doesn't already exist and return session"""
    engine = create_engine(settings.DB_LOCATION)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return session
