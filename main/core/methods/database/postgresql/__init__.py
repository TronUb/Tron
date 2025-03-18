import sys
import atexit
import signal
import logging
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session as ScopedSession

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from main import Config
except ImportError:
    Config = None

# Default database URI
database = "sqlite:///tron.db"

# Override if Config is available
if Config is not None:
    database = getattr(Config, "DB_URI", database)

# Initialize SQLAlchemy base
BASE = declarative_base()


def start() -> ScopedSession:
    """Start a new database session."""
    try:
        engine = create_engine(database)
        BASE.metadata.bind = engine
        BASE.metadata.create_all(engine)  # Ensure tables are created
        return ScopedSession(
            sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        )
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


SESSION: Optional[ScopedSession] = start()

def close_session():
    """Close the session to avoid database locks."""
    if SESSION:
        SESSION.remove()
        logger.info("Database session closed.")

# Register cleanup on exit
atexit.register(close_session)

# Handle termination signals
def handle_signal(signal_number, frame):
    logger.info(f"Received signal {signal_number}. Shutting down...")
    close_session()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)
