# pylint: disable=no-member

import threading
from sqlalchemy import Column, String
from . import SESSION, BASE

# Lock for thread-safe operations
INSERTION_LOCK = threading.RLock()


class DVTABLE(BASE):
    """Table to store database variables."""
    __tablename__ = "database_vars"  # Avoid spaces in table names

    keys = Column(String, primary_key=True)
    values = Column(String)

    def __init__(self, keys, values):
        self.keys = keys
        self.values = values


# Create table if not exists
DVTABLE.__table__.create(checkfirst=True)


class DVSQL:
    """Database Var (DV) Storage Utility"""

    @staticmethod
    def setdv(keys: str, values: str) -> str:
        """Set or update a database variable."""
        with INSERTION_LOCK:
            try:
                existing = SESSION.query(DVTABLE).get(keys)
                if existing:
                    existing.values = values
                    SESSION.merge(existing)
                else:
                    new_entry = DVTABLE(keys, values)
                    SESSION.add(new_entry)
                SESSION.commit()
                return keys
            finally:
                SESSION.close()

    @staticmethod
    def deldv(keys: str) -> bool:
        """Delete a database variable by key."""
        with INSERTION_LOCK:
            try:
                existing = SESSION.query(DVTABLE).get(keys)
                if existing:
                    SESSION.delete(existing)
                    SESSION.commit()
                    return True
                return False
            finally:
                SESSION.close()

    @staticmethod
    def getdv(keys: str):
        """Get a database variable. Supports eval if value is a list/dict/tuple."""
        try:
            entry = SESSION.query(DVTABLE).get(keys)
            if entry:
                try:
                    return eval(entry.values)
                except Exception:
                    return entry.values
            return ""
        finally:
            SESSION.close()

    @staticmethod
    def getalldv() -> dict:
        """Return all key-value pairs."""
        try:
            entries = SESSION.query(DVTABLE).all()
            return {entry.keys: entry.values for entry in entries}
        finally:
            SESSION.close()
