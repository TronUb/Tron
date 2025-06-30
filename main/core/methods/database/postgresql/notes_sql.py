# pylint: disable=no-member

import threading
from sqlalchemy import Column, UnicodeText, Integer, String
from . import SESSION, BASE

# Thread lock
INSERTION_LOCK = threading.RLock()

# In-memory cache
SELF_NOTES = {}


class NOTES(BASE):
    """Notes table structure"""
    __tablename__ = "notes"

    user_id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, primary_key=True)
    value = Column(UnicodeText, nullable=False)
    msgtype = Column(Integer, default=0)
    file = Column(UnicodeText)
    file_ref = Column(UnicodeText)
    message_id = Column(Integer)

    def __init__(
        self, user_id, name, value, msgtype, file=None, file_ref=None, message_id=0
    ):
        self.user_id = user_id
        self.name = name
        self.value = value
        self.msgtype = msgtype
        self.file = file
        self.file_ref = file_ref
        self.message_id = message_id

    def __repr__(self):
        return f"<Note {self.name}>"


# Create table
NOTES.__table__.create(checkfirst=True)


class NOTESSQL:
    """Note management class"""

    @staticmethod
    def save_selfnote(
        user_id, note_name, note_data, msgtype, file=None, file_ref=None, message_id=0
    ):
        """Save or update a note"""
        global SELF_NOTES
        with INSERTION_LOCK:
            try:
                existing = SESSION.query(NOTES).get((user_id, note_name))
                if existing:
                    SESSION.delete(existing)
                new_note = NOTES(
                    user_id,
                    note_name,
                    note_data,
                    int(msgtype),
                    file,
                    file_ref,
                    message_id,
                )
                SESSION.add(new_note)
                SESSION.commit()

                if user_id not in SELF_NOTES:
                    SELF_NOTES[user_id] = {}
                SELF_NOTES[user_id][note_name] = {
                    "value": note_data,
                    "type": msgtype,
                    "file": file,
                    "file_ref": file_ref,
                    "message_id": message_id,
                }
            finally:
                SESSION.close()

    @staticmethod
    def get_selfnote(user_id, note_name):
        """Get a single saved note"""
        return SELF_NOTES.get(user_id, {}).get(note_name)

    @staticmethod
    def get_all_selfnotes(user_id):
        """Get all note names for a user (sorted)"""
        notes = SELF_NOTES.get(user_id)
        if not notes:
            return None
        return sorted(notes.keys())

    @staticmethod
    def get_all_selfnote_inline(user_id):
        """Get all notes with full content"""
        notes = SELF_NOTES.get(user_id)
        if not notes:
            return None
        return {name: notes[name] for name in sorted(notes)}

    @staticmethod
    def rm_selfnote(user_id, note_name):
        """Remove a note from both database and cache"""
        global SELF_NOTES
        with INSERTION_LOCK:
            try:
                note = SESSION.query(NOTES).get((user_id, note_name))
                if note:
                    SESSION.delete(note)
                    SESSION.commit()
                    SELF_NOTES.get(user_id, {}).pop(note_name, None)
                    return True
                return False
            finally:
                SESSION.close()

    @staticmethod
    def load_allnotes():
        """Load all notes from database into memory"""
        global SELF_NOTES
        try:
            notes = SESSION.query(NOTES).all()
            for n in notes:
                if n.user_id not in SELF_NOTES:
                    SELF_NOTES[n.user_id] = {}
                SELF_NOTES[n.user_id][n.name] = {
                    "value": n.value,
                    "type": n.msgtype,
                    "file": n.file,
                    "file_ref": n.file_ref,
                    "message_id": n.message_id,
                }
        finally:
            SESSION.close()


# Preload on boot
NOTESSQL.load_allnotes()
