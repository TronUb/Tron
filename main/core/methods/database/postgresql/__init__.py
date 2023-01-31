import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


try:
    from main import Config
except ImportError:
    Config = None

database = "sqlite:///tron.db"

if Config is not None:
    database = getattr(Config, "DB_URI", database)


def start() -> scoped_session:
    engine = create_engine(database)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

