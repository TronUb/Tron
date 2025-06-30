# pylint: disable=no-member

import threading
from sqlalchemy import Column, String, Integer
from . import SESSION, BASE

# Lock for thread-safe DB operations
INSERTION_LOCK = threading.RLock()

# ───────────────────────────
# Table Definitions
# ───────────────────────────

class PMTABLE(BASE):
    """Whitelist table"""
    __tablename__ = "approve"

    user_id = Column(Integer, primary_key=True)
    boolvalue = Column(String)

    def __init__(self, user_id, boolvalue):
        self.user_id = user_id
        self.boolvalue = boolvalue


class MSGID(BASE):
    """Warn message ID table"""
    __tablename__ = "pm_msg_id"

    user_id = Column(Integer, primary_key=True)
    msg_id = Column(Integer)

    def __init__(self, user_id, msg_id):
        self.user_id = user_id
        self.msg_id = msg_id


class DISAPPROVE(BASE):
    """Warning count table"""
    __tablename__ = "disapprove"

    user_id = Column(Integer, primary_key=True)
    warn_count = Column(Integer)

    def __init__(self, user_id, warn_count):
        self.user_id = user_id
        self.warn_count = warn_count


# Create tables
PMTABLE.__table__.create(checkfirst=True)
MSGID.__table__.create(checkfirst=True)
DISAPPROVE.__table__.create(checkfirst=True)

# ───────────────────────────
# Data Access Class
# ───────────────────────────


class PMPERMITSQL:
    """Database methods for PM permit logic"""

    @staticmethod
    def set_msgid(user_id: int, msg_id: int):
        """Save a user's warning message ID"""
        with INSERTION_LOCK:
            try:
                row = SESSION.query(MSGID).get(user_id)
                if not row:
                    row = MSGID(user_id, msg_id)
                else:
                    row.msg_id = msg_id
                SESSION.merge(row)
                SESSION.commit()
            finally:
                SESSION.close()

    @staticmethod
    def get_msgid(user_id: int) -> int:
        """Get stored message ID for a user"""
        try:
            row = SESSION.query(MSGID).get(user_id)
            return row.msg_id if row else None
        finally:
            SESSION.close()

    @staticmethod
    def set_whitelist(user_id: int, boolvalue: str):
        """Add a user to whitelist"""
        with INSERTION_LOCK:
            try:
                row = SESSION.query(PMTABLE).get(user_id)
                if not row:
                    row = PMTABLE(user_id, boolvalue)
                else:
                    row.boolvalue = str(boolvalue)
                SESSION.add(row)
                SESSION.commit()
                return user_id
            finally:
                SESSION.close()

    @staticmethod
    def del_whitelist(user_id: int) -> bool:
        """Remove user from whitelist"""
        with INSERTION_LOCK:
            try:
                row = SESSION.query(PMTABLE).get(user_id)
                if row:
                    SESSION.delete(row)
                    SESSION.commit()
                    return True
                return False
            finally:
                SESSION.close()

    @staticmethod
    def get_whitelist(user_id: int) -> str:
        """Check if a user is whitelisted"""
        try:
            row = SESSION.query(PMTABLE).get(user_id)
            return str(row.boolvalue) if row else ""
        finally:
            SESSION.close()

    @staticmethod
    def set_warn(user_id: int, warn_count: int):
        """Set warning count for a user"""
        with INSERTION_LOCK:
            try:
                row = SESSION.query(DISAPPROVE).get(user_id)
                if not row:
                    row = DISAPPROVE(user_id, warn_count)
                else:
                    row.warn_count = warn_count
                SESSION.merge(row)
                SESSION.commit()
            finally:
                SESSION.close()

    @staticmethod
    def get_warn(user_id: int) -> str:
        """Get user's warning count"""
        try:
            row = SESSION.query(DISAPPROVE).get(user_id)
            return str(row.warn_count) if row else ""
        finally:
            SESSION.close()

    @staticmethod
    def del_warn(user_id: int) -> bool:
        """Delete a user's warning record"""
        with INSERTION_LOCK:
            try:
                row = SESSION.query(DISAPPROVE).get(user_id)
                if row:
                    SESSION.delete(row)
                    SESSION.commit()
                    return True
                return False
            finally:
                SESSION.close()
