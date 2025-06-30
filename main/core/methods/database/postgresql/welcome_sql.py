# pylint: disable=no-member

import threading
from sqlalchemy import Column, String
from . import SESSION, BASE

class WELCOME(BASE):
    __tablename__ = "welcome"

    chat_id = Column(String, primary_key=True)
    file_id = Column(String)
    text = Column(String)

    def __init__(self, chat_id, file_id, text):
        self.chat_id = chat_id
        self.file_id = file_id
        self.text = text

# Create table if not exists
WELCOME.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


class WELCOMESQL:
    """Provides SQL operations for welcome settings"""

    def set_welcome(self, chat_id: str, file_id: str, text: str = None):
        with INSERTION_LOCK:
            try:
                existing = SESSION.query(WELCOME).get(chat_id)
                if existing:
                    SESSION.delete(existing)

                new_data = WELCOME(chat_id, file_id, text)
                SESSION.add(new_data)
                SESSION.commit()
                return {"chat_id": chat_id, "file_id": file_id, "text": text}
            finally:
                SESSION.close()

    def del_welcome(self, chat_id: str) -> bool:
        with INSERTION_LOCK:
            try:
                record = SESSION.query(WELCOME).get(chat_id)
                if record:
                    SESSION.delete(record)
                    SESSION.commit()
                    return True
                return False
            except Exception as e:
                print(f"Error deleting welcome: {e}")
                return False
            finally:
                SESSION.close()

    def get_welcome(self, chat_id: str) -> dict:
        try:
            record = SESSION.query(WELCOME).get(chat_id)
            return {
                "file_id": str(record.file_id) if record else None,
                "caption": record.text if record else None,
            }
        finally:
            SESSION.close()

    def get_welcome_ids(self) -> list[int]:
        try:
            all_welcomes = SESSION.query(WELCOME).distinct().all()
            return [
                int(entry.chat_id) for entry in all_welcomes if entry.chat_id.isdigit()
            ]
        finally:
            SESSION.close()
