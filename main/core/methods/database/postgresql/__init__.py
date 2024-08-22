import sys
import atexit
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

def close_session():
    """Close the session to avoid database locks."""
    SESSION.remove()

atexit.register(close_session)

import signal

def handle_signal(signal_number, frame):
    close_session()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)
